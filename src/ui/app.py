import flet as ft
import os
import sys

# Append the project root to sys.path so that 'src' is importable.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.ui.views.onboarding import OnboardingView
from src.ui.views.layout_picker import LayoutPickerView
from src.ui.views.slide_builder import SlideBuilderView
from src.ui.views.export import ExportView

def main_routing(page: ft.Page):
    page.title = "PPT Generator App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(OnboardingView(page))
        elif page.route == "/layout_picker":
            page.views.append(LayoutPickerView(page))
        elif page.route == "/slide_builder":
            page.views.append(SlideBuilderView(page))
        elif page.route == "/export":
            page.views.append(ExportView(page))
            
        page.update()

    def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Flet >= 0.80 에서는 최초 루트값이 같으면 route_change가 동작하지 않으므로 강제 호출합니다.
    route_change(None)
