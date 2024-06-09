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

from typing import Callable
import asyncio
import platform
import os
import distro
from .utils import ensure_root, async_subprocess_check_call


class InstallationWorker:
    """Worker to check Operating system and install required packages"""

    def __init__(self, callback: Callable[[str], None]):
        """Constructor
        Args:
            callback (Callable[[str], None]): callback to call after installation check
        """
        self.callback = callback

        self.linux_distro = ""

    async def check_1_operating_system(self) -> bool:
        """Check operating system
        Returns:
            bool: if check is successfull
        """
        operating_system = platform.system()
        if operating_system == "Linux":
            return True

        self.callback("ParaCopy ne fonctionne qu'avec Linux.")
        return False

    async def check_2_distribution(self) -> bool:
        """Check Linux distribution
        Returns:
            bool: if check is successfull
        """
        self.linux_distro = distro.id()
        try:
            distro_version = int(distro.major_version())
        except ValueError:
            distro_version = -1

        if self.linux_distro == "fedora" and distro_version >= 40:
            return True

        self.callback(
            "ParaCopy ne supporte pas la distribution : '{distro} {version}'.".format(
                distro=self.linux_distro, version=distro_version
            )
        )
        return False

    async def check_3_pkexec_fedora(self) -> bool:
        """Check if pkexec is available (Fedora)
        Returns:
            bool: if pkexec is available
        """
        if os.path.isfile("/usr/bin/pkexec"):
            return True
        self.callback(
            """L'utilitaire pkexec n'est pas disponible.
Veuillez installer le package `polkit`.

Vous pouvez utiliser la commande: `sudo dnf install polkit`."""
        )
        return False

    async def check_3_pkexec(self) -> bool:
        """Check if pkexec is available
        Returns:
            bool: if pkexec is available
        """
        match self.linux_distro:
            case "fedora":
                return await self.check_3_pkexec_fedora()
            case _:
                self.callback("Erreur inconnue.")
                return False

    async def check_4_packages_fedora(self) -> bool:
        """Check and install the missing packages (Fedora)
        Returns:
            bool: if all packages are installed
        """
        distro_dependencies = [
            "coreutils",
            "dcfldd",
            "polkit",
            "rsync",
            "systemd-udev",
            "util-linux",
            "util-linux-core",
            "xclip",
            "zenity",
        ]
        try:
            # Check that all needed packages are available
            await async_subprocess_check_call(
                "/usr/bin/rpm",
                "-q",
                *distro_dependencies,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            return True
        except Exception:
            pass

        # Install missing packages
        try:
            await async_subprocess_check_call(
                *ensure_root(["/usr/bin/dnf", "install", "-y", *distro_dependencies]),
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            return True
        except Exception:
            pass

        self.callback(
            "Impossible d'installer les packages requis: `{packages}`".format(
                packages=", ".join(distro_dependencies)
            )
        )
        return False

    async def check_4_packages(self) -> bool:
        """Check and install the missing packages
        Returns:
            bool: if all packages are installed
        """
        match self.linux_distro:
            case "fedora":
                return await self.check_4_packages_fedora()
            case _:
                self.callback("Erreur inconnue.")
                return False

    async def run(self):
        """Main routine to check installation"""
        if not await self.check_1_operating_system():
            return
        await asyncio.sleep(0)

        if not await self.check_2_distribution():
            return
        await asyncio.sleep(0)

        if not await self.check_3_pkexec():
            return
        await asyncio.sleep(0)

        if not await self.check_4_packages():
            return
        await asyncio.sleep(0)

        # Everything was ok
        self.callback()
