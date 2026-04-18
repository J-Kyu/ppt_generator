import flet as ft
from src.state.app_state import app_state
from src.core.engine import generate_ppt
import os
import threading

class ExportView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/export")
        self._page = page
        
        self.title_text = ft.Text("Export Presentation", size=32, weight=ft.FontWeight.BOLD)
        self.desc_text = ft.Text(f"Ready to generate {len(app_state.user_deck)} slides.")
        
        self.status_text = ft.Text("")
        self.progress = ft.ProgressBar(visible=False, width=300)
        
        self.generate_btn = ft.ElevatedButton(
            "Generate & Save PPT",
            icon=ft.Icons.DOWNLOAD,
            on_click=self.on_generate
        )
        
        self.open_btn = ft.ElevatedButton(
            "Open Generated File",
            icon=ft.Icons.FOLDER_OPEN,
            visible=False,
            on_click=self.on_open_file
        )
        
        self.home_btn = ft.TextButton(
            "Start Over",
            icon=ft.Icons.RESTART_ALT,
            visible=False,
            on_click=self.on_start_over
        )
        
        self.output_path = os.path.join(os.path.expanduser("~"), "Desktop", "output_presentation.pptx")
        
        self.controls.extend([
            ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: self._page.go("/layout_picker"))]),
            ft.Container(
                content=ft.Column(
                    [
                        self.title_text,
                        self.desc_text,
                        ft.Container(height=20),
                        self.generate_btn,
                        ft.Container(height=20),
                        self.progress,
                        self.status_text,
                        ft.Container(height=20),
                        ft.Row([self.open_btn, self.home_btn], alignment=ft.MainAxisAlignment.CENTER)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.Alignment(0, 0),
                expand=True
            )
        ])

    def on_generate(self, e):
        if not app_state.user_deck:
            self.status_text.value = "Deck is empty! Go back and add slides."
            self.status_text.color = ft.Colors.RED
            self._page.update()
            return
            
        self.generate_btn.disabled = True
        self.progress.visible = True
        self.status_text.value = "Generating PPT, please wait..."
        self.status_text.color = ft.Colors.BLACK
        self._page.update()
        
        def run_gen():
            try:
                generate_ppt(app_state.original_template_path, app_state.user_deck, self.output_path)
                self.status_text.value = "Success! Saved to Desktop/output_presentation.pptx"
                self.status_text.color = ft.Colors.GREEN
                self.progress.visible = False
                self.open_btn.visible = True
                self.home_btn.visible = True
            except Exception as ex:
                self.status_text.value = f"Error: {str(ex)}"
                self.status_text.color = ft.Colors.RED
                self.progress.visible = False
                self.generate_btn.disabled = False
                
            self.page.update()
            
        threading.Thread(target=run_gen).start()

    def on_open_file(self, e):
        if os.path.exists(self.output_path):
            import subprocess
            if os.name == 'mac' or os.uname().sysname == 'Darwin':
                subprocess.call(('open', self.output_path))
            elif os.name == 'nt':
                os.startfile(self.output_path)
            elif os.name == 'posix':
                subprocess.call(('xdg-open', self.output_path))

    def on_start_over(self, e):
        app_state.reset()
        self.page.go("/")
