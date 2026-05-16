"""
This module defines the ExportView, which handles the final steps of
the workflow, allowing the user to export and save their presentation.
"""
import flet as ft
from loguru import logger

class ExportView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/export")
        logger.info("ExportView instance created")
        self._page = page
        
        self.controls.extend([
            ft.Text("Export View (Dummy)", size=30),
            ft.ElevatedButton("Restart (Back to Onboarding)", on_click=lambda _: self._page.go("/"))
        ])
