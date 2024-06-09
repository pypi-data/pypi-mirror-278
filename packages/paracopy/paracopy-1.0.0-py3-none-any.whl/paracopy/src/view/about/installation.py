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

from typing import Callable, Optional
import flet as ft
from ...services.installation import InstallationWorker


class CheckInstallationDialog(ft.AlertDialog):
    """View dedicated to check ParaCopy installation"""

    def __init__(self, successfull_check_callback: Callable[[None], None]):
        """Constructor
        Args:
            successfull_check_callback (Callable[[None], None]): function to
                call if check installation is successfull
        """
        super().__init__(modal=True)
        self.successfull_check_callback = successfull_check_callback
        self.installation_worker = InstallationWorker(self.on_finish_installation)

        # View
        self.title = ft.Text("Vérification de l'installation")
        self.actions_alignment = ft.MainAxisAlignment.END

        self.progress_ring = ft.ProgressRing(height=100, width=100)
        self.check_markdown = ft.Markdown(
            "ParaCopy vérifie que l'installation est correcte (système d'exploitation, librairies, packages, ...)",
            selectable=True,
        )
        self.content = ft.Container(
            ft.Column(
                [self.progress_ring, self.check_markdown],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=300,
            height=200,
        )

    def did_mount(self):
        self.page.run_task(self.installation_worker.run)

    def on_finish_installation(self, error: Optional[str] = None):
        """When installation ends
        Args:
            error (str): optional error (if None=no error)
        """
        if error is not None:
            self.progress_ring.value = 1
            self.progress_ring.color = ft.colors.RED
            self.check_markdown.value = error

            def yes_click(self):
                self.page.window_destroy()

            self.actions.append(ft.TextButton("Quitter", on_click=yes_click))
            self.update()
        else:
            self.successfull_check_callback()
