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
import pyperclip
from ...services.destination import DestinationsService
from ...services.usb import UsbMonitorService
from ...model.destination import Hub, Device
from .creation import CreateHubDialog
from .hub import HubView
from ..utils.banners import success_banner


class HubsView(ft.Container):
    """Main view for hub management"""

    def __init__(self):
        super().__init__(expand=True)

        # Model & Services
        self.destinations_service = DestinationsService()
        self.hubs = self.destinations_service.get_hubs()

        self.usb_monitor_service = UsbMonitorService(self.on_event_device_connection)

        # View
        self.hub_tabs = ft.Tabs(
            animation_duration=300,
            selected_index=0,
            tabs=[HubView(hub, self.on_click_delete_hub) for hub in self.hubs],
            expand=True,
            expand_loose=True,
        )
        self.last_device_field = ft.TextField(value="aucun", read_only=True, width=200)
        self.last_device_button = ft.IconButton(
            icon=ft.icons.CONTENT_COPY,
            tooltip="Copier l'adresse du disque",
            disabled=True,
            on_click=self.on_click_copy_disk,
        )
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Vos hubs", theme_style=ft.TextThemeStyle.TITLE_LARGE),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Ajouter un hub",
                                    icon=ft.icons.ADD,
                                    on_click=self.on_click_add_hub,
                                ),
                                ft.FilledButton(
                                    "Sauvegarder",
                                    icon=ft.icons.SAVE,
                                    on_click=self.on_click_save,
                                ),
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Text("Adresse du dernier disque branché"),
                        self.last_device_field,
                        self.last_device_button,
                    ]
                ),
                self.hub_tabs,
            ],
        )

    def did_mount(self):
        self.usb_monitor_service.start()

    def will_unmount(self):
        self.usb_monitor_service.stop()

    def on_click_delete_hub(self, hub_view: HubView):
        """When user wants to delete hub
        Args:
            hub_view (HubView): hub to delete
        """
        hub = hub_view.hub
        self.hubs.remove(hub)

        self.hub_tabs.tabs.remove(hub_view)
        self.update()

    def on_click_save(self, _: ft.ControlEvent):
        """Save hubs
        Args:
            _ (ft.ControlEvent): ignored
        """
        self.destinations_service.save_hubs(self.hubs)

        page = self.page

        def close_banner():
            page.banner.open = False
            page.update()

        page.banner = success_banner("Les hubs ont été sauvegardés", close_banner)
        page.banner.open = True
        page.update()

    def on_click_add_hub(self, _: ft.ControlEvent):
        """When user click on button to add hub
        Args:
            _ (ft.ControlEvent): ignored
        """
        dialog = CreateHubDialog(self.on_create_hub)
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def on_create_hub(self, num_rows: int, num_columns: int):
        """When user has validated modal
        Args:
            num_rows (int): number of rows of hub
            num_columns (int): number of columns of hub
        """
        hub = Hub(
            num_columns=num_columns,
            num_rows=num_rows,
            ports=[""] * (num_rows * num_columns),
        )
        self.hubs.append(hub)
        self.hub_tabs.tabs.append(HubView(hub, self.on_click_delete_hub))
        self.update()

    def on_event_device_connection(self, device: Device):
        """When a device is connected/disconnected
        Args:
            device (Device): device
        """
        self.last_device_field.value = device.id
        self.last_device_button.disabled = False
        self.update()

    def on_click_copy_disk(self, _: ft.ControlEvent):
        """When user copy disk address
        Args:
            _ (ft.ControlEvent): ignored
        """
        pyperclip.copy(self.last_device_field.value)
