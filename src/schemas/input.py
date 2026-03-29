from pydantic import BaseModel, Field


class ScriptInput(BaseModel):
    word: str = Field(..., min_length=1, description="English word")
    korean_meaning: str = Field(..., min_length=1, description="Korean meaning")
    etymology_explanation: str = Field(
        ...,
        min_length=30,
        description="Etymology and background explanation (minimum 30 characters)",
    )
