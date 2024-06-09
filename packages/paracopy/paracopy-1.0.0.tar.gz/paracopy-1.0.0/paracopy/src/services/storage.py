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

import os


class StorageService:
    """Storage service"""

    def __init__(self):
        self.data_folder = os.path.expanduser("~") + "/.paracopy"
        self.ensure_folder_exists(self.data_folder)

    def ensure_folder_exists(self, path: str):
        """Ensure folder exists
        Args:
            path (str): path to folder
        """
        os.makedirs(path, exist_ok=True)

    def ensure_file_exists(self, path: str):
        """Ensure folder exists
        Args:
            path (str): path to file
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            os.mknod(path)

    @property
    def destinations_file(self) -> str:
        """File to store destinations

        Returns:
            str: destination file
        """
        destinations_file = self.data_folder + "/destinations.json"
        self.ensure_file_exists(destinations_file)
        return destinations_file

    @property
    def settings_file(self) -> str:
        """File to store settings

        Returns:
            str: settings file
        """
        settings_file = self.data_folder + "/settings.json"
        self.ensure_file_exists(settings_file)
        return settings_file

    @property
    def sources_folder(self) -> str:
        """Folder to store application sources
        Returns:
            str: sources
        """
        sources_folder = self.data_folder + "/sources"
        self.ensure_folder_exists(sources_folder)
        return sources_folder

    @property
    def root_folder(self) -> str:
        """Get root folder for ParaCopy application
        Returns:
            str: root folder
        """
        return os.path.realpath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../..")
        )

    @property
    def assets_folder(self) -> str:
        return f"{self.root_folder}/paracopy/assets"
