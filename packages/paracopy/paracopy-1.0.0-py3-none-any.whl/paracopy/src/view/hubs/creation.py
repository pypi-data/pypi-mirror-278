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


class CreateHubDialog(ft.AlertDialog):
    """Dialog to create hub"""

    def __init__(self, on_success: Callable[[int, int], None]):
        super().__init__(
            modal=True,
            title=ft.Text("Créer un hub"),
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.on_success_callback = on_success

        # View
        self.num_rows_slider = ft.Slider(
            label="{value}",
            value=1,
            divisions=9,
            min=1,
            max=10,
        )
        self.num_columns_slider = ft.Slider(
            label="{value}",
            value=1,
            divisions=9,
            min=1,
            max=10,
        )
        self.content = ft.Column(
            [
                ft.Text("Nombre de lignes"),
                self.num_rows_slider,
                ft.Text("Nombre de colonnes"),
                self.num_columns_slider,
            ],
            height=200,
        )
        self.actions.extend(
            [
                ft.TextButton("Annuler", on_click=self.on_click_cancel),
                ft.TextButton("Créer le hub", on_click=self.on_click_create),
            ]
        )

    def on_click_create(self, _: ft.ControlEvent):
        """Handle hub creation"""
        self.open = False
        self.update()

        num_rows = int(self.num_rows_slider.value)
        num_columns = int(self.num_columns_slider.value)
        self.on_success_callback(num_rows, num_columns)

    def on_click_cancel(self, _: ft.ControlEvent):
        """Handles dialog cancel"""
        self.open = False
        self.update()
