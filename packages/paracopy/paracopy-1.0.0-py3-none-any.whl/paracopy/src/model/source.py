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

from datetime import datetime
from pydantic import BaseModel


class Source(BaseModel):
    """Source"""

    # Name and absolute path to source
    name: str
    path: str

    # Date of creation
    creation_date: datetime

    # Cluster and sector sizes (in Bytes)
    cluster_size: int
    sector_size: int

    # Size of source (in MiB)
    size: int
