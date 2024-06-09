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
import flet as ft
from ...model.destination import Hub


class PortView(ft.TextField):
    """View to display and modify port"""

    def __init__(
        self, index: int, value: str, change_callback: Callable[[int, str], None]
    ):
        super().__init__(
            value=value,
            on_change=lambda _: change_callback(index, self.value),
            width=150,
            label="Adresse",
        )


class HubView(ft.Tab):
    """Hub view"""

    def __init__(self, hub: Hub, on_delete: Callable[["HubView"], None]):
        super().__init__(text="Hub")
        self.hub = hub
        self.on_delete_callback = on_delete

        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            f"{self.hub.num_rows} lignes x {self.hub.num_columns} colonnes"
                        ),
                        ft.ElevatedButton(
                            "Supprimer ce hub",
                            icon=ft.icons.DELETE,
                            on_click=self.on_click_delete,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        PortView(
                                            i * self.hub.num_columns + j,
                                            self.hub.ports[
                                                i * self.hub.num_columns + j
                                            ],
                                            self.on_port_change,
                                        )
                                        for j in range(self.hub.num_columns)
                                    ]
                                )
                                for i in range(self.hub.num_rows)
                            ],
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def on_click_delete(self, _: ft.ControlEvent):
        """When user click on delete button
        Args:
            _ (ft.ControlEvent): ignored
        """

        def cancel_modal(_: ft.ControlEvent):
            dialog.open = False
            self.page.update()

        def confirm_delete(_: ft.ControlEvent):
            dialog.open = False
            self.page.update()
            self.on_delete_callback(self)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Suppression du hub"),
            content=ft.Text("Voulez-vous supprimer le hub ?"),
            actions=[
                ft.TextButton("Annuler", on_click=cancel_modal),
                ft.TextButton("Supprimer définitivement", on_click=confirm_delete),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def on_port_change(self, index: int, value: str):
        """Update port
        Args:
            index (int): index of port
            value (str): value of port
        """
        self.hub.ports[index] = value
