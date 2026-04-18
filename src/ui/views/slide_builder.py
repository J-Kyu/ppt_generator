import flet as ft
from src.state.app_state import app_state
from src.core.schema import SlideSchema
import copy

class SlideBuilderView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/slide_builder")
        self._page = page
        self.scroll = ft.ScrollMode.AUTO
        
        if app_state.current_selected_layout_index is None:
            self.controls.extend([
                ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: self._page.go("/layout_picker"))]),
                ft.Text("No layout selected", color=ft.Colors.RED)
            ])
            return
            
        self.layout_schema = app_state.available_layouts[app_state.current_selected_layout_index]
        self.cloned_shapes = copy.deepcopy(self.layout_schema.shapes)
        
        # Left Panel - Form Area
        self.form_column = ft.Column(spacing=15, expand=1)
        
        self.text_fields = []
        for idx, shape in enumerate(self.cloned_shapes):
            tf = ft.TextField(
                label=shape.shape_name,
                hint_text=f"Default: {shape.default_text}" if shape.default_text else "",
                multiline=True,
                min_lines=1,
                max_lines=5
            )
            self.text_fields.append((idx, tf))
            self.form_column.controls.append(tf)
            
        self.error_text = ft.Text("", color=ft.Colors.RED)
            
        add_btn = ft.ElevatedButton("Add Slide to Deck", on_click=self.on_add_slide, icon=ft.Icons.ADD)
        
        left_panel = ft.Container(
            content=ft.Column([
                ft.Text(f"Build: {self.layout_schema.layout_name}", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                self.form_column,
                self.error_text,
                add_btn
            ], scroll=ft.ScrollMode.AUTO),
            expand=1,
            padding=10
        )
        
        # Right Panel - Deck Area
        self.deck_listview = ft.ListView(expand=1, spacing=10)
        
        right_panel = ft.Container(
            content=ft.Column([
                ft.Text("Your Slide Deck", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                self.deck_listview
            ]),
            expand=1,
            padding=10,
            border=ft.border.only(left=ft.border.BorderSide(1, ft.Colors.GREY_300))
        )
        
        self.controls.extend([
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: self._page.go("/layout_picker")),
                ft.Text("Back to Layouts")
            ]),
            ft.Row([left_panel, right_panel], expand=True, vertical_alignment=ft.CrossAxisAlignment.START)
        ])
        
        # manually populate to prevent none error on hot reload
        self.refresh_deck_view(skip_update=True)

    def refresh_deck_view(self, skip_update=False):
        self.deck_listview.controls.clear()
        if not app_state.user_deck:
            self.deck_listview.controls.append(ft.Text("Your deck is empty.", color=ft.Colors.GREY))
        else:
            for i, slide in enumerate(app_state.user_deck):
                layout_name = app_state.available_layouts[slide.target_layout_index].layout_name
                self.deck_listview.controls.append(
                    ft.ListTile(
                        leading=ft.CircleAvatar(content=ft.Text(str(i+1))),
                        title=ft.Text(f"Slide {i+1}: {layout_name}"),
                        subtitle=ft.Text(f"{len([s for s in slide.shapes if s.user_input])} inputs"),
                        trailing=ft.IconButton(ft.Icons.DELETE, on_click=self.create_delete_handler(i), icon_color=ft.Colors.RED),
                    )
                )
        if not skip_update:
            self._page.update()

    def create_delete_handler(self, index: int):
        def on_delete(e):
            app_state.remove_slide_from_deck(index)
            self.refresh_deck_view()
        return on_delete

    def on_add_slide(self, e):
        # Gather inputs
        for idx, tf in self.text_fields:
            if tf.value.strip():
                self.cloned_shapes[idx].user_input = tf.value
            else:
                self.cloned_shapes[idx].user_input = None

        new_slide = SlideSchema(
            target_layout_index=self.layout_schema.layout_index,
            shapes=self.cloned_shapes
        )
        
        try:
            new_slide.check_required_fields()
        except ValueError as err:
            self.error_text.value = str(err)
            self._page.update()
            return
            
        self.error_text.value = ""
        app_state.add_slide_to_deck(new_slide)
        
        # Clear fields
        for idx, tf in self.text_fields:
            tf.value = ""
            
        self.cloned_shapes = copy.deepcopy(self.layout_schema.shapes)
        self.refresh_deck_view()
