import flet as ft

class SlideBuilderView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/slide_builder")
        self._page = page
        
        self.controls.extend([
            ft.Text("Slide Builder View (Dummy)", size=30),
            ft.ElevatedButton("Go to Export", on_click=lambda _: self._page.go("/export")),
            ft.ElevatedButton("Back to Layout Picker", on_click=lambda _: self._page.go("/layout_picker"))
        ])
