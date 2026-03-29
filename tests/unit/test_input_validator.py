import pytest
from src.nodes.input_validator import input_validator


def _make_state(**kwargs):
    base = {
        "word": "resilient",
        "korean_meaning": "회복력 있는",
        "etymology_explanation": "라틴어 resilire에서 유래. re(다시) + salire(뛰다). 다시 튀어오른다는 뜻.",
    }
    base.update(kwargs)
    return base


def test_valid_input_passes():
    state = _make_state()
    result = input_validator(state)
    assert result["word"] == "resilient"
    assert result["retry_count"] == 0


def test_empty_word_raises():
    state = _make_state(word="")
    with pytest.raises(ValueError, match="입력 검증 실패"):
        input_validator(state)


def test_short_etymology_raises():
    state = _make_state(etymology_explanation="too short")
    with pytest.raises(ValueError, match="입력 검증 실패"):
        input_validator(state)


def test_retry_count_initialized_to_zero():
    state = _make_state()
    result = input_validator(state)
    assert result["retry_count"] == 0


def test_existing_retry_count_preserved():
    state = _make_state()
    state["retry_count"] = 1
    result = input_validator(state)
    assert result["retry_count"] == 1
