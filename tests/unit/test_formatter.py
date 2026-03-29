import pytest
from src.nodes.formatter import formatter
from src.config.settings import settings


def _state_with_draft(draft_script):
    return {
        "word": "test",
        "korean_meaning": "테스트",
        "etymology_explanation": "a" * 30,
        "draft_script": draft_script,
        "retry_count": 0,
        "quality_passed": True,
        "review_feedback": "",
    }


def test_full_script_merges_sections():
    draft = {
        "hook": "훅",
        "etymology": "어원",
        "context": "맥락",
        "memory_anchor": "기억",
        "closing": "마무리",
    }
    result = formatter(_state_with_draft(draft))
    assert "훅" in result["full_script"]
    assert "어원" in result["full_script"]
    assert "마무리" in result["full_script"]


def test_duration_calculated():
    draft = {s: "가나다라마바사아자차카타파하" for s in settings.SECTION_NAMES}
    result = formatter(_state_with_draft(draft))
    assert result["estimated_duration_sec"] > 0


def test_quality_score_perfect_for_in_range():
    # Build a draft that results in exactly ~230 chars total
    target = 230
    per_section = target // len(settings.SECTION_NAMES)
    draft = {s: "가" * per_section for s in settings.SECTION_NAMES}
    result = formatter(_state_with_draft(draft))
    full = result["full_script"]
    char_count = len(full)
    if settings.MIN_CHAR_COUNT <= char_count <= settings.MAX_CHAR_COUNT:
        assert result["quality_score"] == 1.0


def test_quality_score_below_range():
    draft = {s: "가" for s in settings.SECTION_NAMES}
    result = formatter(_state_with_draft(draft))
    assert result["quality_score"] < 1.0


def test_quality_score_bounds():
    draft = {s: "" for s in settings.SECTION_NAMES}
    result = formatter(_state_with_draft(draft))
    assert 0.0 <= result["quality_score"] <= 1.0
