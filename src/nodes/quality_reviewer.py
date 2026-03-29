from src.schemas.state import ScriptState
from src.config.settings import settings


def quality_reviewer(state: ScriptState) -> ScriptState:
    """LangGraph node: validates draft script quality with a checklist."""

    draft_script = state.get("draft_script", {})
    retry_count = state.get("retry_count", 0)
    feedback_items = []

    # Check 1: All required sections are present and non-empty
    for section in settings.SECTION_NAMES:
        if not draft_script.get(section, "").strip():
            feedback_items.append(f"'{section}' 섹션이 비어 있습니다.")

    # Check 2: Total character count is within range
    full_text = " ".join(draft_script.get(s, "") for s in settings.SECTION_NAMES)
    char_count = len(full_text)
    if char_count < settings.MIN_CHAR_COUNT:
        feedback_items.append(
            f"전체 글자 수({char_count}자)가 최소 기준({settings.MIN_CHAR_COUNT}자)보다 짧습니다. 더 자세히 설명해 주세요."
        )
    elif char_count > settings.MAX_CHAR_COUNT:
        feedback_items.append(
            f"전체 글자 수({char_count}자)가 최대 기준({settings.MAX_CHAR_COUNT}자)을 초과합니다. 더 간결하게 줄여 주세요."
        )

    # Check 3: etymology section mentions origin language or root
    etymology_text = draft_script.get("etymology", "")
    etymology_keywords = ["어원", "라틴", "그리스", "영어", "독일", "프랑스", "어근", "뜻이에요", "의미", "유래"]
    if etymology_text and not any(kw in etymology_text for kw in etymology_keywords):
        feedback_items.append("'etymology' 섹션에 어원 설명(어근, 유래 언어 등)이 부족합니다.")

    # Check 4: memory_anchor section contains a concrete daily-life image
    memory_text = draft_script.get("memory_anchor", "")
    if memory_text and len(memory_text) < 15:
        feedback_items.append("'memory_anchor' 섹션이 너무 짧습니다. 구체적인 일상 이미지를 추가해 주세요.")

    quality_passed = len(feedback_items) == 0
    review_feedback = "\n".join(f"- {item}" for item in feedback_items) if feedback_items else ""

    return {
        **state,
        "quality_passed": quality_passed,
        "review_feedback": review_feedback,
        "retry_count": retry_count + (0 if quality_passed else 1),
    }
