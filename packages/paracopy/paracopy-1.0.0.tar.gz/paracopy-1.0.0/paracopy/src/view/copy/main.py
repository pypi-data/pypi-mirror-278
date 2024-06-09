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

from typing import Dict, List, Optional
import flet as ft
from .device import DeviceView
from ...services.settings import SettingsService
from ...services.destination import DestinationsService
from ...services.source import SourceService
from ...services.usb import (
    UsbMonitorService,
    UsbSizeService,
    ComputeOccupiedSpaceWorker,
)
from ...services.copy import CopyPartitionWorker
from ...model.destination import Hub, Device
from ...model.source import Source
from ..utils.banners import error_banner, success_banner
from ..utils.progress import TimerProgressBar


class CopyView(ft.Container):
    """Main view for copy"""

    def __init__(self):
        super().__init__(expand=True)

        # Model & Services
        self.destinations_service = DestinationsService()
        self.hubs = self.destinations_service.get_hubs()

        self.source_service = SourceService()
        self.sources = self.source_service.get_sources()
        self.source_index = -1
        if len(self.sources) > 0:
            self.source_index = 0

        self.devices: Dict[str, DeviceView] = {}

        self.usb_monitor_service = UsbMonitorService(self.on_usb_monitor_event)
        self.usb_size_service = UsbSizeService()

        self.settings_service = SettingsService()
        self.settings = self.settings_service.load()

        # States: idle, copying, computing_occupied_space
        self.state = "idle"

        # View
        self.copy_button = ft.FilledButton(
            icon=ft.icons.PLAY_ARROW,
            text="Lancer la copie",
            on_click=self.on_click_start_copy,
        )
        self.occupied_space_button = ft.ElevatedButton(
            icon=ft.icons.SIGNAL_WIFI_STATUSBAR_4_BAR,
            text="Calculer l'espace occupé",
            tooltip="Calcule l'espace occupé pour chaque destination actuellement connectée.",
            on_click=self.on_click_compute_occupied_space,
        )

        self.progress = TimerProgressBar(visible=False)
        self.content = ft.Column(
            [
                ft.Text("Source", style=ft.TextThemeStyle.TITLE_LARGE),
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option(
                            key=str(i),
                            text=f"{source.name} "
                            f"{source.creation_date.strftime('%d/%m/%Y %H:%M')} "
                            f"({source.size} Mio)",
                        )
                        for i, source in enumerate(self.sources)
                    ],
                    value=str(self.source_index),
                    on_change=self.on_dropdown_source,
                ),
                ft.Text("Destinations", style=ft.TextThemeStyle.TITLE_LARGE),
                ft.Column([self.display_hub(hub) for hub in self.hubs]),
                ft.Row([self.occupied_space_button, self.copy_button]),
                self.progress,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def did_mount(self):
        # Initialize devices
        connected_devices = self.usb_monitor_service.enumerate_devices()
        for device in connected_devices:
            if device.id in self.devices:
                self.devices[device.id].set_device(device)
                self.page.run_task(self.compute_total_space, device)
        self.usb_monitor_service.start()

    def will_unmount(self):
        self.usb_monitor_service.stop()

    def change_state(self, new_state: str):
        """Change application state
        Args:
            new_state (str): state
        """
        match self.state:
            case "copying":
                self.progress.visible = False
                self.progress.value = None
                self.enable_copy(True)
                self.enable_occupied(True)
                self.page.enable_rail(True)
                self.page.confirm_exit = None
                self.update()
            case "computing_occupied_space":
                self.progress.visible = False
                self.progress.value = None
                self.enable_copy(True)
                self.enable_occupied(True)
                self.page.enable_rail(True)
                self.page.confirm_exit = None
                self.update()

        self.state = new_state

        match self.state:
            case "copying":
                self.progress.visible = True
                self.enable_copy(False)
                self.enable_occupied(False)
                self.page.enable_rail(False)
                self.page.confirm_exit = "Une copie est en cours."
                self.update()
            case "computing_occupied_space":
                self.progress.visible = True
                self.enable_copy(False)
                self.enable_occupied(False)
                self.page.enable_rail(False)
                self.page.confirm_exit = "Le calcul de l'espace occupé est en cours."
                self.update()

    def display_hub(self, hub: Hub) -> ft.Control:
        """Display a hub
        Args:
            hub (Hub): hub
        Returns:
            ft.Control: view to display
        """
        devices = [DeviceView(port_id) for port_id in hub.ports]
        for device in devices:
            self.devices[device.port_id] = device

        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Row(
                            [
                                devices[i * hub.num_columns + j]
                                for j in range(hub.num_columns)
                            ]
                        )
                        for i in range(hub.num_rows)
                    ],
                )
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def on_click_start_copy(self, _: ft.ControlEvent):
        """When user click to start copy
        Args:
            _ (ft.ControlEvent): ignored
        """
        page = self.page

        def close_banner():
            page.banner.open = False
            page.update()

        # Check if there is a source
        source = None
        if self.source_index >= 0 and self.source_index < len(self.sources):
            source = self.sources[self.source_index]
        if source is None:
            page.banner = error_banner(
                "La copie n'a pas pu être lancée : il n'y a pas de source sélectionnée.",
                close_banner,
            )
            page.banner.open = True
            page.update()
            return

        # Check if there are destinations
        destinations = []
        for view in self.devices.values():
            device = view.device
            if device is not None and device.is_connected:
                destinations.append(view.device)
        if len(destinations) == 0:
            page.banner = error_banner(
                "La copie n'a pas pu être lancée : il n'y a pas de destinations.",
                close_banner,
            )
            page.banner.open = True
            page.update()
            return

        # Display confirmation
        def cancel_modal(_: ft.ControlEvent):
            dialog.open = False
            self.page.update()

        def start_copy(_: ft.ControlEvent):
            dialog.open = False
            self.page.update()
            self.on_validate_start_copy(source, destinations)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Lancer la copie"),
            content=ft.Text(
                f"""Vous vous apprêter à la lancer une copie
Source: {source.name}
Destinations: {', '.join([destination.block_id for destination in destinations])}
            """
            ),
            actions=[
                ft.TextButton("Annuler", on_click=cancel_modal),
                ft.TextButton("Copier", icon=ft.icons.PLAY_ARROW, on_click=start_copy),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def on_click_compute_occupied_space(self, _: ft.ControlEvent):
        """When user click to start computing occupied space"""
        page = self.page

        def close_banner():
            page.banner.open = False
            page.update()

        # Check if there are devices
        devices = []
        for view in self.devices.values():
            if view.device is not None and view.device.is_connected:
                devices.append(view.device)
        if len(devices) == 0:
            page.banner = error_banner(
                "Il n'y a pas de destination actuellement connectée.",
                close_banner,
            )
            page.banner.open = True
            page.update()
            return

        # Launch task
        self.change_state("computing_occupied_space")
        self.progress.value = 0

        for device in devices:
            view = self.devices.get(device.id, None)
            if view is not None:
                view.set_state("occupied")

        worker = ComputeOccupiedSpaceWorker(
            devices,
            self.on_progress_change,
            self.on_device_occupied_finished,
            self.on_occupied_finished,
        )
        self.page.run_task(worker.run)

    def on_progress_change(self, value: float):
        """When progress has changed
        Args:
            value (float): value
        """
        self.progress.value = value

    def on_device_copy_finished(
        self, device: Device, success: bool, occupied_space: int
    ):
        """When copy is finished for a device

        Args:
            device (Device): device
            success (bool): success
            occupied_space (int): occupied space
        """
        view = self.devices.get(device.id, None)
        if view is not None:
            view.set_state("success" if success else "error")
            view.set_occupied_space(occupied_space)

    def on_device_occupied_finished(self, device: Device, occupied_space: int):
        """When compute occupied space is finished for a device

        Args:
            device (Device): device
            occupied_space (int): occupied space
        """
        view = self.devices.get(device.id, None)
        if view is not None:
            view.set_state("idle")
            view.set_occupied_space(occupied_space)

    def on_validate_start_copy(self, source: Source, destinations: List[Device]):
        """When user has validated copy
        Args:
            source (Source): source of copy
            destinations (List[Device]): destinations
        """
        self.change_state("copying")
        self.progress.value = 0

        for destination in destinations:
            view = self.devices.get(destination.id, None)
            if view is not None:
                view.set_state("occupied")

        worker = CopyPartitionWorker(
            source,
            destinations,
            self.settings.copy_num_destinations_per_process,
            self.on_progress_change,
            self.on_device_copy_finished,
            self.on_copy_finished,
        )
        self.page.run_task(worker.run)

    def on_copy_finished(self, error: Optional[str] = None):
        """When copy is finished
        Args:
            error (str): optional error
        """
        page = self.page
        self.change_state("idle")

        def close_banner():
            page.banner.open = False
            page.update()

        if error is not None:
            page.banner = error_banner("La copie a échoué. " + error, close_banner)
        else:
            page.banner = success_banner("Copie terminée !", close_banner)
        page.banner.open = True
        page.update()

    def on_occupied_finished(self, error: Optional[str] = None):
        """When compute occupied is finished
        Args:
            error (str): optional error
        """
        page = self.page
        self.change_state("idle")

        def close_banner():
            page.banner.open = False
            page.update()

        if error is not None:
            page.banner = error_banner(
                "Le calcul de l'espace occupé a échoué. " + error, close_banner
            )
        else:
            page.banner = success_banner("Calcul terminé !", close_banner)
        page.banner.open = True
        page.update()

    def on_dropdown_source(self, event: ft.ControlEvent):
        """When use changes source
        Args:
            event (ft.ControlEvent): event
        """
        source_index = event.data
        if source_index.isdigit():
            self.source_index = int(source_index)

    async def compute_total_space(self, device: Device):
        """Compute device total space
        Args:
            device (Device): device
        """
        total_space = await self.usb_size_service.async_compute_total_space(
            device.block_id
        )
        if device.id in self.devices:
            self.devices[device.id].set_total_space(total_space)

    def on_usb_monitor_event(self, device: Device):
        """When usb monitor events
        Args:
            device (Device): device
        """
        if device.id in self.devices:
            view = self.devices[device.id]
            found_device = view.device

            if found_device is not None:
                view.set_is_connected(device.is_connected)
                view.set_block_id(device.block_id)
            else:
                view.set_device(device)

            if device.is_connected:
                self.page.run_task(self.compute_total_space, device)

    def enable_copy(self, enabled: bool):
        """Enable/Disable copy
        Args:
            enabled (bool): enabled
        """
        self.copy_button.disabled = not enabled
        self.update()

    def enable_occupied(self, enabled: bool):
        """Enable/Disable occupied space compute
        Args:
            enabled (bool): enabled
        """
        self.occupied_space_button.disabled = not enabled
        self.update()
