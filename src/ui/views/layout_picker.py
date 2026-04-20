import flet as ft
from state.app_state import app_state

class LayoutPickerView(ft.View):
    def __init__(self, page: ft.Page):
        print("LayoutPickerView")
        super().__init__(route="/layout_picker")
        self._page = page
        self.scroll = ft.ScrollMode.AUTO
        
        title = ft.Text("Available Layouts", size=28, weight=ft.FontWeight.BOLD)
        desc = ft.Text("Select a layout to build your next slide.")
        
        grid = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=250,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10,
        )
        
        for idx, layout in enumerate(app_state.available_layouts):
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.DASHBOARD, size=40),
                            ft.Text(layout.layout_name, weight=ft.FontWeight.BOLD, size=16, text_align=ft.TextAlign.CENTER),
                            ft.Text(f"Editable Shapes: {len(layout.shapes)}", size=12, color=ft.Colors.GREY_700),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=10,
                    on_click=self.create_on_click_handler(idx),
                    ink=True
                )
            )
            grid.controls.append(card)
            
        bottom_row = ft.Row(
            [
                ft.ElevatedButton(
                    f"View Deck ({len(app_state.user_deck)} slides) / Export", 
                    on_click=lambda _: self._page.go("/export"), 
                    icon=ft.Icons.SAVE
                ),
            ],
            alignment=ft.MainAxisAlignment.END
        )

        self.controls.extend([
            ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: self._page.go("/"))]),
            title,
            desc,
            ft.Container(content=grid, expand=True),
            bottom_row
        ])

    def create_on_click_handler(self, layout_index: int):
        def on_click(e):
            app_state.current_selected_layout_index = layout_index
            self._page.go("/slide_builder")
        return on_click
