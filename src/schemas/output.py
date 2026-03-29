from pydantic import BaseModel, Field
from typing import Dict


class ScriptOutput(BaseModel):
    word: str
    script: Dict[str, str] = Field(
        description="Section-wise script: hook, etymology, context, memory_anchor, closing"
    )
    full_script: str = Field(description="Complete merged script text")
    estimated_duration_sec: int = Field(description="Estimated reading duration in seconds")
    quality_score: float = Field(ge=0.0, le=1.0, description="Quality score 0.0-1.0")
    quality_passed: bool = Field(description="Whether script passed quality checks")
