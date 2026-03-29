from src.schemas.state import ScriptState
from src.config.settings import settings


def formatter(state: ScriptState) -> ScriptState:
    """LangGraph node: merges draft sections into full_script and calculates metadata."""

    draft_script = state.get("draft_script", {})

    # Merge sections in order
    sections = [draft_script.get(section, "") for section in settings.SECTION_NAMES]
    full_script = " ".join(s for s in sections if s)

    # Estimate reading duration (Korean reading speed: 270 chars/min)
    char_count = len(full_script)
    estimated_duration_sec = int((char_count / settings.KOREAN_READING_SPEED) * 60)

    # Calculate quality score based on char count proximity to target range
    if settings.MIN_CHAR_COUNT <= char_count <= settings.MAX_CHAR_COUNT:
        quality_score = 1.0
    elif char_count < settings.MIN_CHAR_COUNT:
        ratio = char_count / settings.MIN_CHAR_COUNT
        quality_score = max(0.0, ratio)
    else:
        ratio = settings.MAX_CHAR_COUNT / char_count
        quality_score = max(0.0, ratio)

    quality_score = round(quality_score, 2)

    return {
        **state,
        "full_script": full_script,
        "estimated_duration_sec": estimated_duration_sec,
        "quality_score": quality_score,
    }
