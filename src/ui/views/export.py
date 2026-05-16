import flet as ft

class ExportView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/export")
        self._page = page
        
        self.controls.extend([
            ft.Text("Export View (Dummy)", size=30),
            ft.ElevatedButton("Restart (Back to Onboarding)", on_click=lambda _: self._page.go("/"))
        ])
