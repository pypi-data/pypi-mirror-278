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
from pathvalidate import ValidationError, validate_filename
from ..utils.banners import success_banner, error_banner
from ..utils.progress import TimerProgressBar
from ...services.source import (
    SourceService,
    DeviceSectorService,
    ComputeFat32SourceSizeWorker,
    CreateSourceImageWorker,
)


class SourceCreationView(ft.Column):
    """View to create source"""

    def __init__(self):
        super().__init__(alignment=ft.MainAxisAlignment.START)

        # Model
        self.source_path: str = None
        self.cluster_size: int = 4096
        self.sector_size: int = 512
        self.last_sector_size: int = -1
        self.source_image_name: str = ""
        self.source_size: int = 0  # Source size in MiB
        self.additional_mb: int = 0  # Additional MiB to add to source

        # States: "idle", "source_chosen", "computing_size", "size_computed",
        # "copying"
        self.state: str = "idle"

        # Services
        self.source_service = SourceService()
        self.device_sector_size_service = DeviceSectorService(self.set_last_sector_size)

        # View
        self.pick_source_path_dialog = None
        self.source_image_name_field = ft.TextField(
            label="Nom de la source", on_change=self.on_change_source_image_name
        )

        self.choose_source_path_button = ft.IconButton(
            icon=ft.icons.FOLDER_SHARP,
            tooltip="Choisir la source",
            on_click=self.on_click_choose_source,
        )
        self.source_path_field = ft.TextField(
            label="Dossier à utiliser pour la source", read_only=True
        )
        self.last_sector_size_text = ft.Text("0 (pas de disque branché)")

        self.compute_size_button = ft.ElevatedButton(
            text="Calculer la taille de la source",
            icon=ft.icons.DATA_USAGE,
            on_click=self.on_start_computing_size,
        )
        self.source_size_text = ft.Text("0")
        self.additional_mb_field = ft.TextField(
            value="0", on_change=self.on_change_additional_mb, width=200
        )
        self.total_size_text = ft.Text("0")

        self.create_source_button = ft.ElevatedButton(
            text="Créer la source",
            icon=ft.icons.CREATE,
            on_click=self.on_start_creating_source,
        )

        self.progress_bar = TimerProgressBar(visible=False)

        self.controls.extend(
            [
                ft.Row(
                    [
                        self.source_image_name_field,
                    ]
                ),
                ft.Row(
                    [
                        self.source_path_field,
                        self.choose_source_path_button,
                        ft.IconButton(
                            icon=ft.icons.INFO,
                            icon_color="black",
                            tooltip="Les dossiers à l'intérieur du dossier sélectionné"
                            " seront copiés. Le nom du dossier sélectionné ne le sera"
                            " pas.\nAttention : Les dossiers et noms de fichiers ne"
                            " doivent pas comporter d'accents ou de caractères"
                            " spéciaux !",
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.Dropdown(
                            label="Choisir la taille de bloc",
                            options=[
                                ft.dropdown.Option(key="2048", text="2048 (2 Kio)"),
                                ft.dropdown.Option(key="4096", text="4096 (4 Kio)"),
                                ft.dropdown.Option(key="8192", text="8192 (8 Kio)"),
                                ft.dropdown.Option(key="16384", text="16384 (16 Kio)"),
                            ],
                            value=str(self.cluster_size),
                            on_change=self.on_dropdown_cluster_size,
                            width=200,
                        ),
                        ft.IconButton(
                            icon=ft.icons.INFO,
                            icon_color="black",
                            tooltip="Comme règle empirique :\n"
                            "- 2 Kio = taille de la source < 512 Mio\n"
                            "- 4 Kio = 512 Mio-8 Gio\n"
                            "- 8 Kio = 8-16 Gio\n"
                            "- 16 Kio = 16-32 Gio",
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.Dropdown(
                            label="Choisir la taille de secteur",
                            options=[
                                ft.dropdown.Option(key="512", text="512 (512 o)"),
                                ft.dropdown.Option(key="4096", text="4096 (4 Kio)"),
                            ],
                            value=str(self.sector_size),
                            on_change=self.on_dropdown_sector_size,
                            width=200,
                        ),
                        ft.IconButton(
                            icon=ft.icons.INFO,
                            icon_color="black",
                            tooltip="Vérifier la taille de secteur pour la carte SD ou"
                            " clé USB cible. Une bonne valeur par défaut est 512 o.",
                        ),
                        ft.Text("Taille de secteur du dernier disque branché"),
                        self.last_sector_size_text,
                    ],
                    wrap=True,
                ),
                self.compute_size_button,
                ft.Row(
                    [
                        ft.Text("Taille de la source :"),
                        self.source_size_text,
                        ft.Text("+"),
                        self.additional_mb_field,
                        ft.Text("Mio = "),
                        self.total_size_text,
                        ft.Text("Mio"),
                    ],
                    wrap=True,
                ),
                ft.Row([self.create_source_button]),
                self.progress_bar,
            ]
        )

    def did_mount(self):
        super().did_mount()

        self.change_state("idle")

    def change_state(self, new_state: str):
        """Change state
        Args:
            new_state (str): new state
        """
        # Close previous state
        match self.state:
            case "computing_size":
                self.page.enable_rail(True)
                self.page.confirm_exit = None
                self.progress_bar.visible = False
                self.progress_bar.value = None
                self.update()
            case "copying":
                self.page.enable_rail(True)
                self.page.confirm_exit = None
                self.progress_bar.visible = False
                self.progress_bar.value = None
                self.update()
            case _:
                pass

        self.state = new_state

        # Initialize new state
        match self.state:
            case "idle":
                self.enable_choose_source_path(True)
                self.enable_create_source_image(False)
                self.enable_compute_size(False)
            case "source_chosen":
                self.enable_compute_size(True)
                self.enable_create_source_image(False)
            case "computing_size":
                self.page.enable_rail(False)
                self.page.confirm_exit = (
                    "Le calcul de la taille de la source est en cours."
                )
                self.enable_choose_source_path(False)
                self.enable_create_source_image(False)
                self.enable_compute_size(False)
                self.progress_bar.visible = True
                self.progress_bar.value = None
                self.update()
            case "size_computed":
                self.enable_choose_source_path(True)
                self.enable_create_source_image(True)
                self.enable_compute_size(True)
            case "copying":
                self.page.enable_rail(False)
                self.page.confirm_exit = "La source est en train d'être créée."
                self.enable_choose_source_path(False)
                self.enable_create_source_image(False)
                self.enable_compute_size(False)
                self.progress_bar.visible = True
                self.progress_bar.value = 0
                self.update()
            case _:
                pass

    def on_start_creating_source(self, _: ft.ControlEvent):
        """Start creating source
        Args:
            _ (ft.ControlEvent): event
        """
        # Check if source has correct name
        if self.source_image_name == "":
            self.source_image_name_field.error_text = "Ne peut pas être vide"
            self.update()
            return

        if self.source_service.exists(self.source_image_name):
            return

        self.change_state("copying")
        total_size = self.source_size + self.additional_mb
        source_image_path = self.source_service.abspath(self.source_image_name)
        worker = CreateSourceImageWorker(
            self.source_path,
            self.cluster_size,
            self.sector_size,
            total_size,
            source_image_path,
            self.source_image_name,
            self.set_progress,
            self.on_end_creating_source,
        )
        self.page.run_task(worker.run)

    def on_end_creating_source(self, error: Optional[str] = None):
        """When copy is finished
        Args:
            error (str): optional error
        """
        page = self.page
        self.change_state("size_computed")

        def close_banner():
            page.banner.open = False
            page.update()

        if error is not None:
            page.banner = error_banner(
                "La création de la source a échoué. " + error, close_banner
            )
        else:
            page.banner = success_banner("Source créée !", close_banner)
        page.banner.open = True
        page.update()

    def on_start_computing_size(self, _: ft.ControlEvent):
        """Start computing size
        Args:
            _ (ft.ControlEvent): event
        """
        self.change_state("computing_size")
        worker = ComputeFat32SourceSizeWorker(
            self.source_path,
            self.cluster_size,
            self.sector_size,
            2,
            self.on_end_computing_size,
        )
        self.page.run_task(worker.run)

    def on_end_computing_size(self, source_size: int):
        """Callback when computing size has finished
        Args:
            source_size (int): source size
        """
        self.change_state("size_computed")
        self.set_source_size(source_size)

    def on_change_additional_mb(self, event: ft.ControlEvent):
        """When additional mb value has changed
        Args:
            event (ft.ControlEvent): event
        """
        additional_mb = event.data

        if str.isdigit(additional_mb) and int(additional_mb) >= 0:
            self.set_additional_mb(int(additional_mb))
            self.additional_mb_field.error_text = None
            self.update()
        else:
            self.set_additional_mb(0)
            self.additional_mb_field.error_text = "Taille invalide"
            self.update()

    def on_dropdown_cluster_size(self, event: ft.ControlEvent):
        """When cluster size has changed
        Args:
            event (ft.ControlEvent): event
        """
        cluster_size = event.data
        if cluster_size is not None and str.isdigit(cluster_size):
            self.set_cluster_size(int(cluster_size))

    def on_dropdown_sector_size(self, event: ft.ControlEvent):
        """When sector size has changed
        Args:
            event (ft.ControlEvent): event
        """
        sector_size = event.data
        if sector_size is not None and str.isdigit(sector_size):
            self.set_sector_size(int(sector_size))

    def on_click_choose_source(self, _: ft.ControlEvent):
        """Choose source path"""
        if self.pick_source_path_dialog is None:

            def pick_source_path_result(event: ft.FilePickerResultEvent):
                source_path = event.path
                if source_path is not None:
                    self.set_source_path(source_path)
                    self.change_state("source_chosen")

            self.pick_source_path_dialog = ft.FilePicker(
                on_result=pick_source_path_result
            )
            self.page.overlay.append(self.pick_source_path_dialog)
            self.page.update()

        self.pick_source_path_dialog.get_directory_path(
            dialog_title="Choisissez le dossier à utiliser pour la source"
        )

    def on_change_source_image_name(self, event: ft.ControlEvent):
        """When source image name has changed
        Args:
            event (ft.ControlEvent): event
        """
        source_image_name = event.data
        error = False
        error_text = ""

        # Check source image name is a valid file name
        try:
            validate_filename(source_image_name)
        except ValidationError:
            error = True
            error_text = "Nom de dossier invalide"

        # Check if a source exists with this name
        if self.source_service.exists(source_image_name):
            error = True
            error_text = "Une source avec le même nom existe déjà"

        if error:
            self.source_image_name_field.error_text = error_text
            self.update()
            self.set_source_image_name("")
        else:
            self.source_image_name_field.error_text = None
            self.update()
            self.set_source_image_name(source_image_name)

    def enable_choose_source_path(self, enabled: bool):
        """Enable/Disable compute size button
        Args:
            enabled (bool): enabled
        """
        self.choose_source_path_button.disabled = not enabled
        self.update()

    def enable_compute_size(self, enabled: bool):
        """Enable/Disable compute size button
        Args:
            enabled (bool): enabled
        """
        self.compute_size_button.disabled = not enabled
        self.update()

    def enable_create_source_image(self, enabled: bool):
        """Enable/Disable create source button
        Args:
            enabled (bool): enabled
        """
        self.create_source_button.disabled = not enabled
        self.update()

    def set_progress(self, progress: float):
        """Change progressbar progress
        Args:
            progress (float): progress
        """
        self.progress_bar.value = progress
        self.update()

    def set_source_image_name(self, source_image_name: str):
        """Change source image name

        Args:
            source_image_name (str): source image name
        """
        self.source_image_name = source_image_name

    def set_source_size(self, source_size: int):
        """Set source size
        Args:
            source_size (int): source size
        """
        self.source_size = source_size
        self.source_size_text.value = self.source_size
        self.total_size_text.value = self.source_size + self.additional_mb
        self.update()

    def set_additional_mb(self, additional_mb: int):
        """Set additional mb
        Args:
            additional_mb (int): additional mb
        """
        self.additional_mb = additional_mb
        self.total_size_text.value = self.source_size + self.additional_mb
        self.update()

    def set_source_path(self, source_path: str):
        """Set source path
        Args:
            source_path (str): set source path
        """
        self.source_path = source_path
        self.source_path_field.value = source_path
        self.update()

    def set_cluster_size(self, cluster_size: int):
        """Set cluster size
        Args:
            cluster_size (int): cluster size
        """
        self.cluster_size = cluster_size

    def set_sector_size(self, sector_size: int):
        """Set sector size
        Args:
            sector_size (int): sector size
        """
        self.sector_size = sector_size

    def set_last_sector_size(self, sector_size: int):
        """Set sector size of last plugged device
        Args:
            sector_size (int): sector size
        """
        self.last_sector_size = sector_size

        sector_size_text = ""
        match self.last_sector_size:
            case 512:
                sector_size_text = "512 o"
            case 4096:
                sector_size_text = "4 Kio"
            case _:
                sector_size_text = f"{self.last_sector_size} o"

        self.last_sector_size_text.value = sector_size_text
        self.update()
