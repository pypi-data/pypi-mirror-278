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

import flet as ft
from paracopy import __version__
from .installation import CheckInstallationDialog

COPYRIGHT_TEXT = """
# ParaCopy
**{version}** [Notes de version & Code source](https://gitlab.com/paracopy/paracopy/-/releases/{version})

Copyright (c) 2024 Pierre-Yves Genest.
"""

LICENSE_TEXT = """
ParaCopy est sous licence Affero GNU General Public License version 3.

> ParaCopy est un logiciel libre : vous pouvez le redistribuer et/ou le modifier selon les termes de la Affero GNU General Public License telle que publiée par la Free Software Foundation, version 3 de la Licence.
> 
> ParaCopy est distribué dans l'espoir qu'il sera utile, mais SANS AUCUNE GARANTIE ; sans même la garantie implicite de VALEUR COMMERCIALE ou d'ADAPTATION A UN USAGE PARTICULIER. Voir la Affero GNU General Public License pour plus de détails.
> 
> Vous devriez avoir reçu une copie de la Affero GNU General Public License avec ParaCopy. Si ce n'est pas le cas, voir [https://www.gnu.org/licenses/]().

*Tous droits réservés sur le nom ParaCopy et le logo ParaCopy.*
"""


class AboutView(ft.Container):
    """Main view for about"""

    def __init__(self):
        super().__init__(expand=True)

        # Model / Services
        # State: "startup", "checking", "checked"
        self.state: str = "startup"

        # View
        self.content = ft.Column(
            controls=[
                ft.Text(
                    "À propos",
                    theme_style=ft.TextThemeStyle.TITLE_LARGE,
                ),
                ft.Row(
                    [
                        ft.Image(src="/paracopy.svg", width=96),
                        ft.Markdown(
                            COPYRIGHT_TEXT.format(version=__version__),
                            selectable=False,
                            on_tap_link=lambda e: self.page.launch_url(e.data),
                            expand=True,
                        ),
                    ]
                ),
                ft.Markdown(
                    LICENSE_TEXT,
                    selectable=False,
                    on_tap_link=lambda e: self.page.launch_url(e.data),
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
        )

    def change_state(self, new_state: str):
        """Change view state
        Args:
            new_state (str): new state
        """
        match self.state:
            case "checking":
                self.page.enable_rail(True)

        self.state = new_state

        match self.state:
            case "checking":
                self.page.enable_rail(False)

    def start_installation_check(self):
        """Start ParaCopy installation check"""
        self.change_state("checking")
        dialog = CheckInstallationDialog(self.on_installation_check_successful)
        dialog.open = True
        self.page.dialog = dialog
        self.page.update()

    def on_installation_check_successful(self):
        """When installation check is successful"""
        self.change_state("checked")
        self.page.dialog.open = False
        self.page.update()
        self.page.dialog = None

    def did_mount(self):
        # Check program only at startup
        if self.page.starting:
            self.start_installation_check()
            self.page.starting = False
