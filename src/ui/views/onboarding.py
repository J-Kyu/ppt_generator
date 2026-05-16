import flet as ft

class OnboardingView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/")
        self._page = page
        
        self.controls.extend([
            ft.Text("Onboarding View (Dummy)", size=30),
            ft.ElevatedButton("Go to Layout Picker", on_click=lambda _: self._page.go("/layout_picker"))
        ])
