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

from typing import Callable, Optional, List
import os
import sys
import shutil
import re
import math
import asyncio
import pyudev
from .storage import StorageService
from .utils import ensure_root
from ..model.source import Source
from .root.utils import parse_message, ErrorMessage

PERCENTAGE_EXTRACTOR = re.compile(" ([0-9]+)%")
NEWLINE_EXTRACTOR = re.compile("[\r\n]+")


class SourceService:
    """Service to handle sources"""

    def __init__(self):
        self.storage_service = StorageService()
        self.sources_folder = self.storage_service.sources_folder

    def get_sources(self) -> List[Source]:
        """Get list of current sources
        Returns:
            List[Source]: sources
        """
        sources: List[Source] = []
        for name in os.listdir(self.sources_folder):
            path = self.abspath(name)
            if os.path.isdir(path):
                with open(f"{path}/metadata.json", "r", encoding="utf-8") as file:
                    source = Source.model_validate_json(file.read())
                sources.append(source)
        return sources

    def delete(self, name: str):
        """Delete a source
        Args:
            name (str): name of source
        """
        shutil.rmtree(self.abspath(name), ignore_errors=True)

    def exists(self, name: str) -> bool:
        """Check if a source image exists with this name
        Args:
            name (str): source image
        Returns:
            bool: if source image name exists
        """
        return os.path.exists(f"{self.sources_folder}/{name}")

    def abspath(self, name: str) -> str:
        """Return path of source image
        Args:
            name (str): source image
        Returns:
            str: absolute path to source image
        """
        return os.path.abspath(f"{self.sources_folder}/{name}")


class DeviceSectorService:
    """Find sector size of last plugged drive"""

    def __init__(self, callback: Callable[[int], None]):
        self.context = pyudev.Context()
        self.callback = callback

        monitor = pyudev.Monitor.from_netlink(self.context)
        monitor.filter_by(subsystem="scsi", device_type="scsi_device")
        self.device_observer = pyudev.MonitorObserver(
            monitor, self._handle_monitor_event
        )

        self.device_observer.start()

    def _handle_monitor_event(self, action: str, udev_device: pyudev.Device):
        """Receive a device event
        Args:
            action (str): action
            device (pyudev.Device): device
        """
        if action != "bind":
            return

        # sda, sdb, ...
        block_id = DeviceSectorService._find_block_id(udev_device.sys_path)

        sector_size_path = f"/sys/block/{block_id}/queue/hw_sector_size"
        if os.path.exists(sector_size_path) and os.path.isfile(sector_size_path):
            with open(sector_size_path, "r", encoding="utf-8") as f:
                try:
                    sector_size = int(f.read())
                    self.callback(sector_size)
                except ValueError:
                    pass

    @classmethod
    def _find_block_id(cls, sys_name: str) -> str:
        block_folder = f"{sys_name}/block"
        assert os.path.exists(block_folder) and os.path.isdir(block_folder)
        subdirectories = os.listdir(block_folder)
        assert len(subdirectories) == 1
        return subdirectories[0]


class ComputeFat32SourceSizeWorker:
    """Compute source size"""

    def __init__(
        self,
        source_path: str,
        cluster_size: int,
        sector_size: int,
        num_fat_tables: int,
        callback: Callable[[int], None],
    ):
        """Compute source size
        Args:
            source_path (str): absolute path to source
            cluster_size (int): cluster size in byte
            sector_size (int): sector size in byte
            num_fat_tables (int): number of fat tables (usually 2)
            callback (Callable[[int], None]): callback to call after compute
        """
        super().__init__()
        self.source_path = source_path
        self.cluster_size = cluster_size
        self.sector_size = sector_size
        self.callback = callback
        self.num_fat_tables = num_fat_tables

    async def compute_size_file(self, file_path: str) -> int:
        """Compute size of file
        Args:
            file_path (str): absolute path to file
        Returns:
            int: size in block of block_size
        """
        return math.ceil(os.path.getsize(file_path) / self.cluster_size)

    async def compute_size_directory(self, directory_path: str) -> int:
        """Compute size of directory
        Args:
            directory_path (str): absolute path to directory
        Returns:
            int: size in block of block_size
        """
        total_size = 0
        num_files = 0
        for file in os.listdir(directory_path):
            num_files += 1 + math.ceil(max(len(file) - 6, 0) / 13)
            file_path = os.path.join(directory_path, file)
            total_size += await self.compute_size(file_path)

        total_size += math.ceil((1 + num_files) * 32 / self.cluster_size)
        return total_size

    async def compute_size(self, path: str) -> int:
        """Compute size of file or directory
        Args:
            path (str): absolute path to file or directory
        Returns:
            int: size in block of block_size
        """
        if os.path.isdir(path):
            return await self.compute_size_directory(path)
        elif os.path.exists(path):
            return await self.compute_size_file(path)
        else:
            return 0

    async def run(self):
        """Run task"""
        # Compute data region clusters
        data_region_clusters = await self.compute_size(self.source_path)

        # Compute fat table size
        fat_entries_per_cluster = self.cluster_size / 4
        fat_region_clusters = math.ceil(
            (data_region_clusters + 2) / fat_entries_per_cluster
        )

        # Total size (in clusters)
        sectors_per_cluster = int(self.cluster_size / self.sector_size)
        total_clusters = (
            data_region_clusters
            + self.num_fat_tables * fat_region_clusters
            + math.ceil((32 + 1) / sectors_per_cluster)
        )
        total_clusters = math.ceil(total_clusters / 32) * 32

        # Convert to MiB (+ alignment)
        total_size = 1 + math.ceil(total_clusters * self.cluster_size / (1024 * 1024))

        self.callback(total_size)


class CreateSourceImageWorker:
    """Service to create source image"""

    def __init__(
        self,
        source_path: str,
        cluster_size: int,
        sector_size: int,
        total_size: int,
        source_image_path: str,
        source_image_name: str,
        progress_callback: Callable[[int], None],
        callback: Callable[[Optional[str]], None],
    ):
        """Constructor
        Args:
            callback (Callable[Optional[str], None]): callback to call after compute
            progress_callback (Callable[[int], None]): callback to update progress
        """
        super().__init__()
        self.source_path = source_path
        self.source_image_path = source_image_path
        self.source_image_name = source_image_name
        self.sector_size = sector_size
        self.cluster_size = cluster_size
        self.total_size = total_size
        self.callback = callback
        self.progress_callback = progress_callback
        self.storage_service = StorageService()

    async def run(self):
        """Copy and monitor progress
        Returns:
            Optional[str]: error if any
        """

        # Create source image
        proc = await asyncio.create_subprocess_exec(
            *ensure_root(
                [
                    sys.executable,
                    "-m",
                    "paracopy.src.services.root.create_source",
                    f"--source-path={self.source_path}",
                    f"--source-name={self.source_image_name}",
                    f"--source-size={self.total_size}",
                    f"--output-path={self.source_image_path}",
                    f"--cluster-size={self.cluster_size}",
                    f"--sector-size={self.sector_size}",
                    f"--uid={os.geteuid()}",
                ],
                cwd=self.storage_service.root_folder,
            ),
            stdout=asyncio.subprocess.PIPE,
        )

        error_message: ErrorMessage = None
        while (line := await proc.stdout.readline()) != b"":
            try:
                message = parse_message(line)
                match message.type:
                    case "progress":
                        self.progress_callback(message.value)
                    case "error":
                        error_message = message
            except ValueError:
                pass
        await proc.communicate()

        if proc.returncode != 0:
            shutil.rmtree(self.source_image_path, ignore_errors=True)

            if error_message is not None:
                self.callback(error_message.message)
            else:
                self.callback("Erreur inconnue.")
        else:
            self.callback()
