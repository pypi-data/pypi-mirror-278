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
from ...services.settings import SettingsService
from ..utils.banners import success_banner


class SettingsView(ft.Container):
    """Main view for settings"""

    def __init__(self):
        super().__init__(expand=True)

        # Model/Services
        self.settings_service = SettingsService()
        self.settings = self.settings_service.load()

        # View
        self.copy_num_destinations_per_process_field = ft.TextField(
            label="Nombre de destinations par processus de copie",
            value=str(self.settings.copy_num_destinations_per_process),
            on_change=self.on_copy_num_destinations_per_process_change,
        )
        self.content = ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.Text(
                            "Paramètres",
                            theme_style=ft.TextThemeStyle.TITLE_LARGE,
                            expand=True,
                        ),
                        ft.FilledButton(
                            icon=ft.icons.SAVE,
                            text="Sauvegarder",
                            on_click=self.on_click_save,
                        ),
                    ]
                ),
                ft.Text(
                    "Paramètres de la copie", theme_style=ft.TextThemeStyle.TITLE_MEDIUM
                ),
                ft.Row(
                    [
                        self.copy_num_destinations_per_process_field,
                        ft.IconButton(
                            icon=ft.icons.INFO,
                            icon_color="black",
                            tooltip="Nombre de destinations par processus de copie :\n"
                            "- 0 : un seul processus pour toutes les destinations,\n"
                            "- 1 (2, 3, …) : 1 (2, 3, …) destinations par processus de copie.\n"
                            "Plus de destinations par processus augmente la vitesse de copie"
                            ", mais s'il y a des destinations défecteuses, cela "
                            "peut causer des erreurs.",
                        ),
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
        )

    def on_click_save(self, _: ft.ControlEvent):
        """When user clicks on the save button
        Args:
            _ (ft.ControlEvent): ignored
        """
        page = self.page
        self.settings_service.save(self.settings)

        def close_banner():
            page.banner.open = False
            page.update()

        page.banner = success_banner("Les paramètres ont été sauvegardés", close_banner)
        page.banner.open = True
        page.update()

    def on_copy_num_destinations_per_process_change(self, event: ft.ControlEvent):
        """When user changes num_destinations_per_process
        Args:
            event (ft.ControlEvent): event
        """
        copy_num_destinations_per_process = event.data

        if (
            str.isdigit(copy_num_destinations_per_process)
            and int(copy_num_destinations_per_process) >= 0
        ):
            self.settings.copy_num_destinations_per_process = int(
                copy_num_destinations_per_process
            )
            self.copy_num_destinations_per_process_field.error_text = None
        else:
            self.copy_num_destinations_per_process_field.error_text = (
                "Doit être égal ou supérieur à 0"
            )
        self.update()
