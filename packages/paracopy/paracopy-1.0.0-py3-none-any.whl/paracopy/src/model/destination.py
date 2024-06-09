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

from typing import List, Literal
from pydantic import BaseModel

DeviceState = Literal["idle", "occupied", "success", "error"]


class Device(BaseModel):
    """Model for a usb device with storage (e.g. usb drives, sd cards, ...)"""

    # Id of device (= path in hierarchy of usb devices, e.g. 2.1.4)
    id: str = ""

    # Block id (name of block device e.g., sda, sdb, ...)
    block_id: str = ""

    # Occupied/Total space of device (in Bytes)
    occupied_space: int = -1
    total_space: int = 0

    # If device is connected
    is_connected: bool = False

    # State of Device
    state: DeviceState = "idle"


class Hub(BaseModel):
    """Hub"""

    # Number of rows/columns of hub
    num_rows: int
    num_columns: int

    # Ports. Iterate row by row
    ports: List[str]


class Destinations(BaseModel):
    """Model for destinations"""

    hubs: List[Hub]
