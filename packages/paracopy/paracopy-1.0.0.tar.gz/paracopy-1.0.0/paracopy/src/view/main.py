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

from concurrent.futures import ThreadPoolExecutor
import flet as ft
from .source.main import SourcesView
from .hubs.main import HubsView
from .copy.main import CopyView
from .settings.main import SettingsView
from .about.main import AboutView


class MainView:
    """Main ParaCopy view"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.set_title("ParaCopy")
        self.page.window_min_height = 600
        self.page.window_min_width = 700

        # Navigation rail
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            group_alignment=0,
            leading=ft.Image(src="/paracopy.svg", width=40),
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.DOWNLOAD_OUTLINED,
                    selected_icon=ft.icons.DOWNLOAD,
                    label="Copie",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.USB_OUTLINED,
                    selected_icon=ft.icons.USB,
                    label="Hubs",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.DRIVE_FOLDER_UPLOAD_OUTLINED,
                    selected_icon=ft.icons.DRIVE_FOLDER_UPLOAD_SHARP,
                    label="Sources",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon=ft.icons.SETTINGS,
                    label="Paramètres",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.INFO_OUTLINED,
                    selected_icon=ft.icons.INFO,
                    label="À propos",
                ),
            ],
            on_change=self.on_navigation_rail_change,
        )

        self.main = ft.Container(expand=True)
        self.page.add(
            ft.Row(
                [self.rail, ft.VerticalDivider(width=1), self.main],
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        )
        self.page.update()

        # Startup
        self.page.starting = True
        self.page.on_route_change = self.on_route_change
        self.rail.selected_index = 4
        self.page.go("/about")

        # Enable/Disable rail
        self.page.enable_rail = self.enable_rail

        # When user wants to leave application
        self.page.window_prevent_close = True
        self.page.on_window_event = self.on_window_event
        self.page.confirm_exit: str = None

        # Add thread execution
        self.page.thread_pool = ThreadPoolExecutor()
        self.page.run_thread_custom = self.page.thread_pool.submit

    def on_window_event(self, event: ft.ControlEvent):
        """Handles window event
        Args:
            event (ft.ControlEvent): event
        """
        if event.data == "close":
            if self.page.confirm_exit is None:
                self.page.window_destroy()
            else:
                # Ask user for confirmation before closing
                def no_click(self):
                    confirm_dialog.open = False
                    self.page.update()

                def yes_click(self):
                    self.page.window_destroy()

                confirm_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Quitter ParaCopy"),
                    content=ft.Text(
                        f"Voulez-vous vraiment quitter ParaCopy ? {self.page.confirm_exit}"
                    ),
                    actions=[
                        ft.TextButton("Annuler", on_click=no_click),
                        ft.TextButton("Quitter", on_click=yes_click),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                self.page.dialog = confirm_dialog
                confirm_dialog.open = True
                self.page.update()

    def on_route_change(self, event: ft.RouteChangeEvent):
        """Handle route change
        Args:
            event (ft.RouteChangeEvent): event
        """
        if self.main.content is not None:
            self.main.content.clean()
        self.page.overlay.clear()
        self.page.update()

        route = event.route
        match (route):
            case "/copy":
                self.route_copy()
            case "/hubs":
                self.route_hubs()
            case "/sources":
                self.route_sources()
            case "/settings":
                self.route_settings()
            case "/about":
                self.route_about()

    def on_navigation_rail_change(self, event: ft.ControlEvent):
        """Handles click on navigation rail
        Args:
            event (ft.ControlEvent): event
        """
        rail_index = int(event.data)
        match (rail_index):
            case 0:  # Copy table
                self.page.go("/copy")
            case 1:  # Hub management
                self.page.go("/hubs")
            case 2:  # Source management
                self.page.go("/sources")
            case 3:  # Settings
                self.page.go("/settings")
            case 4:  # About
                self.page.go("/about")

    def enable_rail(self, enabled: bool):
        """Enable/Disable navigation rail
        Args:
            enabled (bool): enabled state
        """
        self.rail.disabled = not enabled
        self.page.update()

    def route_copy(self):
        """Copy view"""
        self.set_title("ParaCopy – Table de copie")
        self.main.content = CopyView()
        self.page.update()

    def route_sources(self):
        """Sources route"""
        self.set_title("ParaCopy – Gestion des sources")
        self.main.content = SourcesView()
        self.page.update()

    def route_hubs(self):
        """Hub route"""
        self.set_title("ParaCopy – Gestion des hubs")
        self.main.content = HubsView()
        self.page.update()

    def route_settings(self):
        """Settings route"""
        self.set_title("ParaCopy – Paramètres")
        self.main.content = SettingsView()
        self.page.update()

    def route_about(self):
        """Settings route"""
        self.set_title("ParaCopy – À propos")
        self.main.content = AboutView()
        self.page.update()

    def set_title(self, title: str):
        """Update application title

        Args:
            title (str): title
        """
        self.page.title = title
        self.page.update()
