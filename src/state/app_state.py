from typing import List, Optional
from src.core.schema import LayoutSchema, SlideSchema

class AppState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance.reset()
        return cls._instance

    def reset(self):
        self.original_template_path: Optional[str] = None
        self.available_layouts: List[LayoutSchema] = []
        self.user_deck: List[SlideSchema] = []
        self.current_selected_layout_index: Optional[int] = None

    def initialize_session(self, file_path: str, layouts: List[LayoutSchema]):
        self.original_template_path = file_path
        self.available_layouts = layouts

    def add_slide_to_deck(self, slide_data: SlideSchema):
        self.user_deck.append(slide_data)

    def remove_slide_from_deck(self, index: int):
        if 0 <= index < len(self.user_deck):
            self.user_deck.pop(index)

# Flet 전역에서 import할 공용 인스턴스
app_state = AppState()
