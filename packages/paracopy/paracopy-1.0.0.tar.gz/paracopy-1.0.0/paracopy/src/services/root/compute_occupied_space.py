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

from typing import List
import argparse
import os
import sys
import tempfile
from ...model.script import ErrorMessage, SuccessMessage, DeviceOccupiedSpaceMessage
from ..usb import UsbSizeService
from .utils import (
    exit_with_error,
    send_progress,
    exit_with_success,
    send_device_occupied_space_message,
)


def main(args: dict) -> int:
    """Main entrypoint of script
    Args:
        args (dict): args
    """
    block_ids: List[str] = args.block_id

    # Ensure user is root
    if os.geteuid() != 0:
        return exit_with_error(
            ErrorMessage(
                message="Permissions insuffisantes pour calculer l'espace occupé par les disques"
            )
        )

    # Compute occupied space of provided block ids
    usb_size_service = UsbSizeService()
    for i, block_id in enumerate(block_ids):
        send_progress(i / len(block_ids))
        occupied_space = usb_size_service.compute_occupied_space(block_id)
        send_device_occupied_space_message(
            DeviceOccupiedSpaceMessage(block_id=block_id, occupied_space=occupied_space)
        )
    send_progress(1)

    return exit_with_success(SuccessMessage())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ParaCopy Compute Occupied Space",
        description="Root script of ParaCopy to compute occupied space",
    )
    parser.add_argument(
        "--block-id",
        help="Destination of copy (e.g., sda, sdb)",
        action="append",
        type=str,
        required=True,
    )
    parser_args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname)
        return_code = main(parser_args)
    sys.exit(return_code)
