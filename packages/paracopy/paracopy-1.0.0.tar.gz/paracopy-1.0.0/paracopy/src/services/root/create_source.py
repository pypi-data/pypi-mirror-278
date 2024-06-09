"""
Copyright (c) 2024 Pierre-Yves Genest.

This file is part of ParaCopy.

ParaCopy is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, version 3 of the
License.

ParaCopy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with ParaCopy. If not, see <https://www.gnu.org/licenses/>.
"""

import re
import tempfile
import argparse
from datetime import datetime
import subprocess
from subprocess import CalledProcessError, PIPE, DEVNULL
import os
import sys
from ...model.script import ErrorMessage, SuccessMessage
from ...model.source import Source
from .utils import exit_with_error, send_progress, exit_with_success


PROGRESS_EXTRACTOR = re.compile(" ([0-9]+)%")


def unmount_loop_device(loop_device: str) -> int:
    """Unmount loop device
    Args:
        loop_device (str): name of loop device
    """
    try:
        subprocess.check_output(
            [
                "/usr/sbin/losetup",
                "-d",
                loop_device,
            ],
        )
    except CalledProcessError:
        return exit_with_error(
            ErrorMessage(message="Impossible de démonter le périphérique interne.")
        )


def unmount_partition(mount_path: str) -> int:
    """Unmount partition
    Args:
        mount_path (str): path to mounted partition
    """
    try:
        subprocess.check_output(
            ["/usr/bin/umount", mount_path],
        )
    except CalledProcessError:
        return exit_with_error(
            ErrorMessage(message="Impossible de démonter la partition FAT32.")
        )


def proc_stdin(proc: subprocess.Popen, text: str):
    """Write proc stdin
    Args:
        proc (subprocess.Popen): proc
        text (str): input to write
    """
    proc.stdin.write(text.encode(encoding="utf-8"))


def main(args: dict) -> int:
    """Main entrypoint of script
    Args:
        args (dict): args
    """
    uid: int = args.uid
    source_name: str = args.source_name
    source_path: str = args.source_path
    output_path: str = args.output_path
    source_image_path = f"{output_path}/source.img"
    source_metadata_path = f"{output_path}/metadata.json"
    source_size: int = args.source_size
    sector_size: int = args.sector_size
    cluster_size: int = args.cluster_size
    sectors_per_cluster = int(cluster_size / sector_size)
    loop_device = "/dev/loop101"
    mount_path = "mount"

    # Ensure user is root
    if os.geteuid() != 0:
        return exit_with_error(
            ErrorMessage(
                message="Permissions insuffisantes pour lancer la création de la source"
            )
        )

    # Create output path if needed
    os.makedirs(output_path, exist_ok=True)

    # Create image file
    try:
        subprocess.check_output(
            [
                "/usr/bin/dd",
                "if=/dev/zero",
                f"of={source_image_path}",
                f"seek={source_size-1}",
                "bs=1M",
                "count=1",
            ],
        )
    except CalledProcessError:
        return exit_with_error(
            ErrorMessage(message="Impossible de créer le fichier image.")
        )
    send_progress(0.01)

    # Create MBR + partition
    with subprocess.Popen(
        ["/usr/sbin/fdisk", source_image_path, f"--sector-size={sector_size}"],
        stdin=PIPE,
        stdout=DEVNULL,
    ) as proc:
        proc_stdin(proc, "o\n")  # Create a new empty DOS partition table
        proc_stdin(proc, "n\n")  # Add a new partition
        proc_stdin(proc, "p\n")  # Primary partition
        proc_stdin(proc, "1\n")  # Partition number
        proc_stdin(proc, "\n")  # First sector (Accept default: 1MB)
        proc_stdin(proc, "\n")  # Last sector (Accept default: all space)
        proc_stdin(proc, "t\n")  # Change partition type
        proc_stdin(proc, "0c\n")  # Choose FAT32 partition
        proc_stdin(proc, "w\n")  # Write changes
        proc.communicate()

        # Parse error code
        if proc.returncode != 0:
            return exit_with_error(
                ErrorMessage(
                    message="Impossible d'initialiser les partitions du fichier image."
                )
            )
    send_progress(0.02)

    # Mount image to loop device
    try:
        subprocess.check_output(
            [
                "/usr/sbin/losetup",
                f"--sector-size={sector_size}",
                "-P",
                loop_device,
                source_image_path,
            ],
        )
    except CalledProcessError:
        return exit_with_error(
            ErrorMessage(
                message="Impossible de monter l'image vers un périphérique interne."
            )
        )
    send_progress(0.03)

    # Create FAT32 partition
    try:
        subprocess.check_output(
            [
                "/usr/sbin/mkfs.fat",
                "-f",
                "2",
                "-F",
                "32",
                "-S",
                str(sector_size),
                "-s",
                str(sectors_per_cluster),
                "-v",
                f"{loop_device}p1",
            ],
        )
    except CalledProcessError:
        unmount_loop_device(loop_device)
        return exit_with_error(
            ErrorMessage(message="Impossible de créer la partition FAT32.")
        )
    send_progress(0.04)

    # Mount FAT32 partition
    os.makedirs("mount", exist_ok=True)
    try:
        subprocess.check_output(
            ["/usr/bin/mount", f"{loop_device}p1", mount_path],
        )
    except CalledProcessError:
        unmount_loop_device(loop_device)
        return exit_with_error(
            ErrorMessage(message="Impossible de monter la partition FAT32.")
        )
    send_progress(0.05)

    # Copy data
    with subprocess.Popen(
        [
            "/usr/bin/rsync",
            "-rLt",
            "--info=progress2",
            f"{source_path}/",
            mount_path,
        ],
        stdout=PIPE,
        universal_newlines=True,
    ) as proc:
        # Parse progress
        last_progress = 0.05
        for line in iter(proc.stdout.readline, ""):
            if "%" in line:
                progress = PROGRESS_EXTRACTOR.search(line)
                if progress:
                    progress = int(progress.group(1)) / 100
                    if progress - last_progress >= 0.01:
                        send_progress(0.05 + progress * 0.45)
                        last_progress = progress
        proc.communicate()

        # Parse error code
        if proc.returncode != 0:
            unmount_loop_device(loop_device)
            unmount_partition(mount_path)
            return exit_with_error(
                ErrorMessage(message="Une erreur est survenue pendant la copie.")
            )
    send_progress(0.5)

    # Check data was correctly copied
    with subprocess.Popen(
        [
            "/usr/bin/rsync",
            "-crLt",
            "--info=progress2",
            f"{source_path}/",
            mount_path,
        ],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    ) as proc:
        # Parse progress
        last_progress = 0.5
        for line in iter(proc.stdout.readline, ""):
            if "%" in line:
                progress = PROGRESS_EXTRACTOR.search(line)
                if progress:
                    progress = int(progress.group(1)) / 100
                    if progress - last_progress >= 0.01:
                        send_progress(0.5 + progress * 0.47)
                        last_progress = progress
        proc.communicate()

        # Parse error code
        if proc.returncode != 0:
            unmount_loop_device(loop_device)
            unmount_partition(mount_path)
            return exit_with_error(
                ErrorMessage(
                    message="Une erreur est survenue pendant la vérification de la copie."
                )
            )
    send_progress(0.97)

    # Unmount image
    unmount_partition(mount_path)
    unmount_loop_device(loop_device)
    send_progress(0.98)

    # Write metadata file
    with open(source_metadata_path, "w", encoding="utf-8") as file:
        source = Source(
            name=source_name,
            path=output_path,
            creation_date=datetime.now(),
            cluster_size=cluster_size,
            sector_size=sector_size,
            size=source_size,
        )
        file.write(source.model_dump_json())
    send_progress(0.99)

    # Set proper permissions
    try:
        subprocess.check_output(
            ["/usr/bin/chmod", "-R", "775", output_path],
        )
        subprocess.check_output(
            ["/usr/bin/chown", "-R", str(uid), output_path],
        )
    except CalledProcessError:
        unmount_loop_device(loop_device)
        return exit_with_error(
            ErrorMessage(
                message="Impossible de changer l'utilisateur et les permissions."
            )
        )
    send_progress(1)

    return exit_with_success(SuccessMessage())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ParaCopy Create Source",
        description="Root script of ParaCopy to create a source",
    )
    parser.add_argument(
        "--source-path",
        help="Path to folder that will be used as the source",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--source-name",
        help="Name of source",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--source-size", help="Source size (in MiB)", type=int, required=True
    )
    parser.add_argument(
        "--output-path",
        help="Path to folder to write the source",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--cluster-size", help="Cluster size (in B)", type=int, required=True
    )
    parser.add_argument(
        "--sector-size", help="Sector size (in B)", type=int, required=True
    )
    parser.add_argument("--uid", help="User id", type=int, required=True)
    parser_args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname)
        return_code = main(parser_args)

    sys.exit(return_code)
