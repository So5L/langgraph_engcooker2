from pydantic import ValidationError
from src.schemas.state import ScriptState
from src.schemas.input import ScriptInput


def input_validator(state: ScriptState) -> ScriptState:
    """LangGraph node: validates input fields using ScriptInput Pydantic model."""

    try:
        ScriptInput(
            word=state.get("word", ""),
            korean_meaning=state.get("korean_meaning", ""),
            etymology_explanation=state.get("etymology_explanation", ""),
        )
    except ValidationError as e:
        raise ValueError(f"입력 검증 실패: {e}")

    return {
        **state,
        "retry_count": state.get("retry_count", 0),
        "quality_passed": state.get("quality_passed", False),
    }
