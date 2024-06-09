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
from datetime import datetime
import math


class TimerProgressBar(ft.Column):
    """Progress bar that display an estimated time left"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.progress = ft.ProgressBar()
        self.progress_text = ft.Text(
            None, width=200, theme_style=ft.TextThemeStyle.LABEL_MEDIUM
        )
        self.controls = [
            self.progress_text,
            self.progress,
        ]

        self.start = None

    @property
    def value(self) -> float:
        """Get value of progress bar
        Returns:
            float: value
        """
        return self.progress.value

    @value.setter
    def value(self, value: float = None):
        """Set value of progress bar
        Args:
            value (float, optional): value. Defaults to .0.
        """

        if value is None:
            self.start = None
            self.progress.value = None
            self.progress_text.value = None
            self.update()
            return

        value = max(0.0, min(1.0, value))
        if value == 0.0:
            self.start = datetime.now()
            self.progress.value = 0
            self.progress_text.value = "Temps restant : indéterminé"
        else:
            self.progress.value = value

            if self.start is not None:
                elapsed_time = datetime.now() - self.start
                estimated_time_left_seconds = math.ceil(
                    ((1 - value) / value * elapsed_time.total_seconds())
                )
                estimated_time_left_minutes = estimated_time_left_seconds // 60
                estimated_time_left_seconds = (
                    estimated_time_left_seconds - estimated_time_left_minutes * 60
                )
                self.progress_text.value = f"Temps restant : {estimated_time_left_minutes:02d}:{estimated_time_left_seconds:02d}"
        self.update()
