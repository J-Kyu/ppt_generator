"""
This module defines the SlideBuilderView, where the user can customize
and build individual slides for their presentation.
"""
import flet as ft
from loguru import logger

class SlideBuilderView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/slide_builder")
        logger.info("SlideBuilderView instance created")
        self._page = page
        
        self.controls.extend([
            ft.Text("Slide Builder View (Dummy)", size=30),
            ft.ElevatedButton("Go to Export", on_click=lambda _: self._page.go("/export")),
            ft.ElevatedButton("Back to Layout Picker", on_click=lambda _: self._page.go("/layout_picker"))
        ])
