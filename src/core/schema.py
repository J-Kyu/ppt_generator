from pydantic import BaseModel, Field, model_validator
from typing import List, Optional

class ShapeSchema(BaseModel):
    shape_name: str
    shape_id: Optional[str] = None
    shape_type: str = "TEXT"
    default_text: str = ""
    user_input: Optional[str] = None
    is_required: bool = False

class LayoutSchema(BaseModel):
    layout_name: str
    layout_index: int
    shapes: List[ShapeSchema]

class SlideSchema(BaseModel):
    target_layout_index: int
    shapes: List[ShapeSchema]

    @model_validator(mode='after')
    def check_required_fields(self):
        for shape in self.shapes:
            if shape.is_required and not shape.user_input:
                raise ValueError(f"Required field '{shape.shape_name}' is empty.")
        return self

class UserPptData(BaseModel):
    constructed_slides: List[SlideSchema] = Field(default_factory=list)
