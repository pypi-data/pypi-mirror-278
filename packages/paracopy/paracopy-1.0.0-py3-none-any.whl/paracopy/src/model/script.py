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

from typing import Union, Literal, Optional
from pydantic import BaseModel, Field


class ProgressMessage(BaseModel):
    """Progress of script"""

    type: Literal["progress"] = "progress"
    value: float = Field(None, ge=0, le=1)


class SuccessMessage(BaseModel):
    """Success of script"""

    type: Literal["success"] = "success"
    message: Optional[str] = None


class ErrorMessage(BaseModel):
    """Error of script"""

    type: Literal["error"] = "error"
    message: str


class DeviceCopyMessage(BaseModel):
    """device copy success/error"""

    type: Literal["device_copy"] = "device_copy"
    block_id: str
    success: bool
    occupied_space: int  # Occupied space in Bytes


class DeviceOccupiedSpaceMessage(BaseModel):
    """device occupied space message"""

    type: Literal["device_occupied_space"] = "device_occupied_space"
    block_id: str
    occupied_space: int  # Occupied space in Bytes


Messages = Union[
    ProgressMessage,
    SuccessMessage,
    ErrorMessage,
    DeviceCopyMessage,
    DeviceOccupiedSpaceMessage,
]


class MessageWrapper(BaseModel):
    """Wrapper for messages"""

    message: Messages = Field(..., discriminator="type")
