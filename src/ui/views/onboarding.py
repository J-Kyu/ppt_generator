"""
This module defines the OnboardingView, which is the initial screen shown to the user.
It handles welcoming the user and initiating the PPT generation workflow.
"""
import flet as ft
from loguru import logger

class OnboardingView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/")
        logger.info("OnboardingView instance created")
        self._page = page
        
        self.controls.extend([
            ft.Text("Onboarding View (Dummy)", size=30),
            ft.ElevatedButton("Go to Layout Picker", on_click=lambda _: self._page.go("/layout_picker"))
        ])
