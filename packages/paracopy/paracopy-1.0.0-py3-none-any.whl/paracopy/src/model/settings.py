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

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Settings"""

    ########## Copy settings ##########
    # Number of destinations to copy in parallel per dcfldd process.
    # 0: all destinations in a single process
    # >0: num destinations per process
    copy_num_destinations_per_process: int = Field(0, ge=0)
