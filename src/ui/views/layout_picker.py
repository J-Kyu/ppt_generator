import flet as ft

class LayoutPickerView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/layout_picker")
        self._page = page
        
        self.controls.extend([
            ft.Text("Layout Picker View (Dummy)", size=30),
            ft.ElevatedButton("Go to Slide Builder", on_click=lambda _: self._page.go("/slide_builder")),
            ft.ElevatedButton("Go to Export", on_click=lambda _: self._page.go("/export")),
            ft.ElevatedButton("Back", on_click=lambda _: self._page.go("/"))
        ])
