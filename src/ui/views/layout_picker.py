"""
This module defines the LayoutPickerView, allowing the user to select
a template or layout structure for their presentation.
"""
import flet as ft
from loguru import logger

class LayoutPickerView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/layout_picker")
        logger.info("LayoutPickerView instance created")
        self._page = page
        
        self.controls.extend([
            ft.Text("Layout Picker View (Dummy)", size=30),
            ft.ElevatedButton("Go to Slide Builder", on_click=lambda _: self._page.go("/slide_builder")),
            ft.ElevatedButton("Go to Export", on_click=lambda _: self._page.go("/export")),
            ft.ElevatedButton("Back", on_click=lambda _: self._page.go("/"))
        ])
