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
from ..model.destination import Destinations, Hub
from .storage import StorageService


class DestinationsService:
    """Service for destinations"""

    def __init__(self):
        self.storage_service = StorageService()

    def get_hubs(self) -> List[Hub]:
        """Get hubs
        Returns:
            List[Hub]: hubs
        """
        with open(
            self.storage_service.destinations_file, "r", encoding="utf-8"
        ) as file:
            try:
                return Destinations.model_validate_json(file.read()).hubs
            except ValueError:
                return []

    def save_hubs(self, hubs: List[Hub]):
        """Save hubs
        Args:
            hubs (List[Hub]): hubs
        """
        with open(
            self.storage_service.destinations_file, "w", encoding="utf-8"
        ) as file:
            file.write(Destinations(hubs=hubs).model_dump_json())
