import flet as ft
from core.engine import analyze_ppt, PPTAnalyzeError
from state.app_state import app_state

class OnboardingView(ft.View):
    def __init__(self, page: ft.Page, file_picker: ft.FilePicker):
        print("OnboardingView")
        super().__init__(route="/")
        self._page = page
        self.file_picker = file_picker
        self.file_picker.on_result = self.on_picker_result
        
        self.title_text = ft.Text("PPT Layout Builder", size=32, weight=ft.FontWeight.BOLD)
        self.desc_text = ft.Text("Select a template PPTX file to analyze its master layouts.", size=16)
        
        # elavated button
        # self.select_btn = ft.ElevatedButton(
        #     "Select Template PPTX",
        #     icon=ft.Icons.UPLOAD_FILE,
        #     on_click=self.on_file_selected
        # )

        self.select_btn = ft.Button(
            content="Pick test",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=self.on_file_selected
        )
        
        self.status_text = ft.Text("")
        self.spinner = ft.ProgressRing(visible=False)
        
        self.controls.extend([
            ft.Container(
                content=ft.Column(
                    [
                        self.title_text,
                        self.desc_text,
                        ft.Container(height=40),
                        self.select_btn,
                        ft.Container(height=20),
                        self.spinner,
                        self.status_text
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.Alignment(0, 0),
                expand=True
            )
        ])

    async def on_file_selected(self, e):
        # Open the file picker dialog
        try:
            await self.file_picker.pick_files(
                allowed_extensions=["pptx"],
                file_type=ft.FilePickerFileType.CUSTOM
            )
        except Exception as ex:
            print(f"DEBUG: Error calling pick_files: {ex}")


    def on_picker_result(self, e):
        files = e.files
        print(f"files: {files}")

        if files and len(files) > 0:
            file_path = files[0].path
            self.spinner.visible = True
            self.status_text.value = f"Analyzing {files[0].name}..."
            self.status_text.color = ft.Colors.BLACK
            self._page.update()
            
            try:
                layouts = analyze_ppt(file_path)
                app_state.initialize_session(file_path, layouts)
                
                self.spinner.visible = False
                self._page.update()
                
                # Navigate to layout picker
                self._page.go("/layout_picker")
                
            except PPTAnalyzeError as err:
                self.spinner.visible = False
                self.status_text.value = f"Error: {str(err)}"
                self.status_text.color = ft.Colors.RED
                self._page.update()
            except Exception as ex:
                self.spinner.visible = False
                self.status_text.value = f"Unexpected Error: {str(ex)}"
                self.status_text.color = ft.Colors.RED
                self._page.update()
        else:
            self.status_text.value = "File selection cancelled."
            self._page.update()
