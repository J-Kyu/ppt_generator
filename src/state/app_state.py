class AppState:
    def __init__(self):
        self.template_path = None
        self.available_layouts = []
        self.current_selected_layout_index = None
        self.user_deck = []
        
    def initialize_session(self, template_path, layouts):
        self.template_path = template_path
        self.available_layouts = layouts
        
    def add_slide_to_deck(self, slide):
        self.user_deck.append(slide)
        
    def remove_slide_from_deck(self, index):
        if 0 <= index < len(self.user_deck):
            del self.user_deck[index]
            
    def reset(self):
        self.template_path = None
        self.available_layouts = []
        self.current_selected_layout_index = None
        self.user_deck = []

# 전역 싱글톤 객체 생성
app_state = AppState()
