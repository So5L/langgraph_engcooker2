from typing import TypedDict


class ScriptState(TypedDict, total=False):
    # Input fields
    word: str
    korean_meaning: str
    etymology_explanation: str

    # Intermediate state
    draft_script: dict[str, str]  # {"hook": ..., "etymology": ..., etc.}
    retry_count: int
    quality_passed: bool
    review_feedback: str

    # Final output
    full_script: str
    estimated_duration_sec: int
    quality_score: float
