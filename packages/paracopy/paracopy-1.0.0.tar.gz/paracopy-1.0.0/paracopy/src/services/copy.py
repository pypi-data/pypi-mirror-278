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

import sys
from typing import List, Callable
import asyncio
from ..model.destination import Device
from ..model.source import Source
from .utils import ensure_root
from .storage import StorageService
from .root.utils import parse_message, ErrorMessage


class CopyPartitionWorker:
    """Service to manage partition copy"""

    def __init__(
        self,
        source: Source,
        destinations: List[Device],
        num_destinations_per_process: int,
        progress_callback: Callable[[float], None],
        end_device_callback: Callable[[Device, bool, int], None],
        end_callback: Callable[[str], None],
    ):
        self.source = source
        self.destinations = destinations
        self.num_destinations_per_process = num_destinations_per_process
        self.progress_callback = progress_callback
        self.end_callback = end_callback
        self.end_device_callback = end_device_callback

        self.storage_service = StorageService()

    async def run(self):
        """Run copy"""
        proc = await asyncio.create_subprocess_exec(
            *ensure_root(
                [
                    sys.executable,
                    "-m",
                    "paracopy.src.services.root.copy_partition",
                    f"--source-path={self.source.path}",
                    *[
                        f"--destination-block-id={dest.block_id}"
                        for dest in self.destinations
                    ],
                    f"--num-destinations-per-process={self.num_destinations_per_process}",
                ],
                cwd=self.storage_service.root_folder,
            ),
            stdout=asyncio.subprocess.PIPE,
        )

        destinations_by_block_id = {dest.block_id: dest for dest in self.destinations}

        error_message: ErrorMessage = None
        while (line := await proc.stdout.readline()) != b"":
            try:
                message = parse_message(line)
                match message.type:
                    case "progress":
                        self.progress_callback(message.value)
                    case "error":
                        error_message = message
                    case "device_copy":
                        self.end_device_callback(
                            destinations_by_block_id[message.block_id],
                            message.success,
                            message.occupied_space,
                        )
            except ValueError:
                pass
        await proc.communicate()

        if proc.returncode != 0:
            if error_message is not None:
                self.end_callback(error_message.message)
            else:
                self.end_callback("Erreur inconnue.")
        else:
            self.end_callback()
