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

from .storage import StorageService
from ..model.settings import Settings


class SettingsService:
    """Service to manage settings"""

    def __init__(self):
        self.storage_service = StorageService()

    def load(self) -> Settings:
        """Load settings"""
        with open(self.storage_service.settings_file, "r", encoding="utf-8") as file:
            try:
                return Settings.model_validate_json(file.read())
            except ValueError:
                return Settings()

    def save(self, settings: Settings):
        """Save settings

        Args:
            settings (Settings): settings
        """
        with open(self.storage_service.settings_file, "w", encoding="utf-8") as file:
            file.write(settings.model_dump_json())
