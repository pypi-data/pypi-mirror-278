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


def success_banner(text: str, on_close: Callable[[None], None]) -> ft.Banner:
    """Create success banner
    Args:
        text (str): text to display
        on_close (Callable[[None], None]): when on close button is clicked
    Returns:
        ft.Banner: banner
    """
    return ft.Banner(
        bgcolor=ft.colors.GREEN_100,
        leading=ft.Icon(ft.icons.CHECK, color=ft.colors.GREEN, size=40),
        content=ft.Text(text),
        actions=[ft.TextButton("Fermer", on_click=lambda _: on_close())],
    )


def warning_banner(text: str, on_close: Callable[[None], None]) -> ft.Banner:
    """Create warning banner
    Args:
        text (str): text to display
        on_close (Callable[[None], None]): when on close button is clicked
    Returns:
        ft.Banner: banner
    """
    return ft.Banner(
        bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(ft.icons.WARNING, color=ft.colors.AMBER, size=40),
        content=ft.Text(text),
        actions=[ft.TextButton("Fermer", on_click=lambda _: on_close())],
    )


def error_banner(text: str, on_close: Callable[[None], None]) -> ft.Banner:
    """Create error banner
    Args:
        text (str): text to display
        on_close (Callable[[None], None]): when on close button is clicked
    Returns:
        ft.Banner: banner
    """
    return ft.Banner(
        bgcolor=ft.colors.RED_100,
        leading=ft.Icon(ft.icons.ERROR, color=ft.colors.RED, size=40),
        content=ft.Text(text),
        actions=[ft.TextButton("Fermer", on_click=lambda _: on_close())],
    )
