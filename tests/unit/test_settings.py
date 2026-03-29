import pytest
from src.config.settings import Settings, settings


def test_constants_accessible():
    s = Settings()
    assert s.MIN_CHAR_COUNT == 200
    assert s.MAX_CHAR_COUNT == 260
    assert s.KOREAN_READING_SPEED == 270
    assert s.MAX_RETRY_COUNT == 2
    assert s.TARGET_DURATION_MIN_SEC == 45
    assert s.TARGET_DURATION_MAX_SEC == 60
    assert s.LLM_TEMPERATURE == 0.7
    assert s.LLM_MAX_TOKENS == 1000


def test_section_names():
    s = Settings()
    assert s.SECTION_NAMES == ["hook", "etymology", "context", "memory_anchor", "closing"]
    assert len(s.SECTION_NAMES) == 5


def test_singleton_importable():
    assert settings is not None
    assert isinstance(settings, Settings)


def test_api_key_defaults_to_empty(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    s = Settings()
    assert isinstance(s.OPENAI_API_KEY, str)


def test_model_is_gpt4o_mini():
    s = Settings()
    assert s.OPENAI_MODEL == "gpt-4o-mini"


def test_char_count_range_valid():
    s = Settings()
    assert s.MIN_CHAR_COUNT < s.MAX_CHAR_COUNT
