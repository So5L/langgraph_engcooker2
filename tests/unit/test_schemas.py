import pytest
from pydantic import ValidationError
from src.schemas.input import ScriptInput
from src.schemas.output import ScriptOutput
from src.schemas.state import ScriptState


# ── ScriptInput ─────────────────────────────────────────────────────────────

def test_script_input_valid():
    obj = ScriptInput(
        word="resilient",
        korean_meaning="회복력 있는",
        etymology_explanation="라틴어 resilire에서 유래. re(다시) + salire(뛰다). 다시 튀어오른다는 뜻.",
    )
    assert obj.word == "resilient"
    assert obj.korean_meaning == "회복력 있는"


def test_script_input_empty_word_fails():
    with pytest.raises(ValidationError):
        ScriptInput(word="", korean_meaning="뜻", etymology_explanation="a" * 30)


def test_script_input_short_etymology_fails():
    with pytest.raises(ValidationError):
        ScriptInput(word="test", korean_meaning="테스트", etymology_explanation="too short")


def test_script_input_exactly_30_chars_etymology():
    obj = ScriptInput(word="test", korean_meaning="테스트", etymology_explanation="a" * 30)
    assert len(obj.etymology_explanation) == 30


def test_script_input_serialization():
    obj = ScriptInput(
        word="test",
        korean_meaning="테스트",
        etymology_explanation="a" * 30,
    )
    data = obj.model_dump()
    assert data["word"] == "test"
    restored = ScriptInput(**data)
    assert restored.word == obj.word


# ── ScriptState ──────────────────────────────────────────────────────────────

def test_script_state_partial():
    state: ScriptState = {"word": "test", "retry_count": 0}
    assert state["word"] == "test"
    assert state["retry_count"] == 0


def test_script_state_full():
    state: ScriptState = {
        "word": "test",
        "korean_meaning": "테스트",
        "etymology_explanation": "a" * 30,
        "draft_script": {"hook": "안녕", "etymology": "유래", "context": "맥락", "memory_anchor": "기억", "closing": "마무리"},
        "retry_count": 1,
        "quality_passed": True,
        "review_feedback": "",
        "full_script": "전체 스크립트",
        "estimated_duration_sec": 50,
        "quality_score": 0.95,
    }
    assert state["quality_passed"] is True
    assert isinstance(state["draft_script"], dict)


# ── ScriptOutput ─────────────────────────────────────────────────────────────

def test_script_output_valid():
    obj = ScriptOutput(
        word="test",
        script={"hook": "h", "etymology": "e", "context": "c", "memory_anchor": "m", "closing": "cl"},
        full_script="full",
        estimated_duration_sec=50,
        quality_score=0.9,
        quality_passed=True,
    )
    assert obj.quality_score == 0.9


def test_script_output_quality_score_bounds():
    with pytest.raises(ValidationError):
        ScriptOutput(
            word="test",
            script={},
            full_script="f",
            estimated_duration_sec=50,
            quality_score=1.1,  # out of range
            quality_passed=True,
        )
    with pytest.raises(ValidationError):
        ScriptOutput(
            word="test",
            script={},
            full_script="f",
            estimated_duration_sec=50,
            quality_score=-0.1,  # out of range
            quality_passed=False,
        )


def test_script_output_boundary_scores():
    for score in [0.0, 0.5, 1.0]:
        obj = ScriptOutput(
            word="test",
            script={},
            full_script="f",
            estimated_duration_sec=50,
            quality_score=score,
            quality_passed=score >= 0.8,
        )
        assert obj.quality_score == score
