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
import subprocess
import flet as ft
from ...services.source import SourceService, Source


class SourceView(ft.DataRow):
    """Display source"""

    def __init__(self, source: Source, on_delete: Callable[["SourceView"], None]):
        super().__init__()
        self.source = source
        self.on_delete_callback = on_delete

        self.cells.extend(
            [
                ft.DataCell(ft.Text(self.source.name)),
                ft.DataCell(ft.Text(self.source.size)),
                ft.DataCell(ft.Text(self.source.cluster_size)),
                ft.DataCell(ft.Text(self.source.sector_size)),
                ft.DataCell(
                    ft.Text(self.source.creation_date.strftime("%d/%m/%Y %H:%M"))
                ),
                ft.DataCell(
                    ft.IconButton(
                        ft.icons.DELETE,
                        tooltip="Supprimer la source",
                        on_click=self.on_click_delete,
                    )
                ),
            ]
        )

    def on_click_delete(self, _: ft.ControlEvent):
        """When user click to delete source
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
            title=ft.Text(f'Suppression de "{self.source.name}"'),
            content=ft.Text(f'Voulez-vous supprimer la source "{self.source.name}" ?'),
            actions=[
                ft.TextButton("Annuler", on_click=cancel_modal),
                ft.TextButton("Supprimer définitivement", on_click=confirm_delete),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()


class SourceListView(ft.Column):
    """Display and manage the list of sources"""

    def __init__(self):
        super().__init__(alignment=ft.MainAxisAlignment.START)

        # Model & Services
        self.source_service = SourceService()
        self.sources = self.source_service.get_sources()

        # View
        self.sources_view = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nom")),
                ft.DataColumn(ft.Text("Taille (Mio)"), numeric=True),
                ft.DataColumn(ft.Text("Taille de bloc (o)"), numeric=True),
                ft.DataColumn(ft.Text("Taille de secteur (o)"), numeric=True),
                ft.DataColumn(ft.Text("Date de création")),
                ft.DataColumn(ft.Text()),
            ],
            rows=[
                SourceView(source, self.on_click_delete_source)
                for source in self.sources
            ],
        )
        self.controls.extend(
            [
                ft.Row(
                    [
                        ft.Text("Dossier où sont stockées vos sources"),
                        ft.IconButton(
                            ft.icons.DRIVE_FOLDER_UPLOAD,
                            tooltip="Ouvrir le dossier",
                            on_click=self.on_click_open_sources_folder,
                        ),
                    ]
                ),
                ft.Row([self.sources_view], scroll=ft.ScrollMode.AUTO),
            ]
        )

    def on_click_delete_source(self, source_view: SourceView):
        """Handle delete source
        Args:
            source_view (SourceView): source
        """
        source = source_view.source
        self.source_service.delete(source.name)
        self.sources.remove(source)
        self.sources_view.rows.remove(source_view)
        self.update()

    def on_click_open_sources_folder(self, _: ft.ControlEvent):
        """Handles click event to open source folder
        Args:
            _ (ft.ControlEvent): event
        """
        subprocess.Popen(["/usr/bin/xdg-open", self.source_service.sources_folder])
