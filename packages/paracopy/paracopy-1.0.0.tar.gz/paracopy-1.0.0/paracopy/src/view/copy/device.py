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

from typing import Optional
import flet as ft
from ...model.destination import Device, DeviceState


UNITS = ["o", "kio", "Mio", "Gio"]


class DeviceView(ft.Card):
    """View for a port and a device"""

    def __init__(self, port_id: str):
        super().__init__(width=150, color=ft.colors.WHITE)

        # Model
        self.port_id = port_id
        self.device: Optional[Device] = None

        # View
        self.is_connected_icon = ft.Icon(
            name=ft.icons.USB_OFF, color=ft.colors.GREY, size=20, tooltip="Déconnecté"
        )
        self.block_id_text = ft.Text(expand=True)
        self.space_progress = ft.ProgressBar(value=0, bar_height=20)
        self.space_text = ft.Text()
        self.content = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [self.block_id_text, self.is_connected_icon],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Stack(
                        [
                            self.space_progress,
                            ft.Row(
                                [self.space_text],
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ],
                    ),
                ]
            ),
            padding=5,
        )

    def display_space(self):
        """Display space"""
        total_space = self.device.total_space
        occupied_space = self.device.occupied_space

        if total_space > 0:
            self.space_progress.value = max(0, occupied_space) / total_space
        else:
            self.space_progress.value = 0

        def format_occupied():
            if occupied_space < 0:
                return "…"
            else:
                return f"{occupied_space:.1f}"

        if total_space < 1024:
            self.space_text.value = f"{format_occupied()} - {total_space:.1f} o"

        occupied_space /= 1024
        total_space /= 1024
        if total_space < 1024:
            self.space_text.value = f"{format_occupied()} - {total_space:.1f} kio"

        occupied_space /= 1024
        total_space /= 1024
        if total_space < 1024:
            self.space_text.value = f"{format_occupied()} - {total_space:.1f} Mio"

        occupied_space /= 1024
        total_space /= 1024
        self.space_text.value = f"{format_occupied()} - {total_space:.1f} Gio"

        self.update()

    def set_is_connected(self, is_connected: bool):
        """Update connection state
        Args:
            is_connected (bool): is connected
        """
        if self.device is not None:
            self.device.is_connected = is_connected

            if is_connected:
                self.is_connected_icon.name = ft.icons.USB
                self.is_connected_icon.color = ft.colors.GREEN
                self.is_connected_icon.tooltip = "Connecté"
            else:
                self.is_connected_icon.name = ft.icons.USB_OFF
                self.is_connected_icon.color = ft.colors.GREY
                self.is_connected_icon.tooltip = "Déconnecté"
            self.update()

    def set_occupied_space(self, occupied_space: int):
        """Set occupied space
        Args:
            occupied_space (int): occupied space
        """
        if self.device is not None:
            self.device.occupied_space = occupied_space
            self.display_space()

    def set_total_space(self, total_space: int):
        """Set total space
        Args:
            total_space (int): total space
        """
        if self.device is not None:
            self.device.total_space = total_space
            self.display_space()

    def set_block_id(self, block_id: str):
        """Set device block id
        Args:
            block_id (str): block id
        """
        if self.device is not None:
            self.device.block_id = block_id

            self.block_id_text.value = block_id
            self.update()

    def set_state(self, state: DeviceState):
        """Set device state
        Args:
            state (DeviceState): state
        """
        if self.device is not None:
            self.device.state = state

            match self.device.state:
                case "idle":
                    self.color = ft.colors.WHITE
                case "occupied":
                    self.color = ft.colors.BLUE_100
                case "success":
                    self.color = ft.colors.GREEN_100
                case "error":
                    self.color = ft.colors.RED_100
            self.update()

    def set_device(self, device: str):
        """Set device
        Args:
            device (str): device
        """
        self.device = device

        if self.device is not None:
            self.set_is_connected(self.device.is_connected)
            self.set_state(self.device.state)
            self.set_total_space(self.device.total_space)
            self.set_block_id(self.device.block_id)
