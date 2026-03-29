import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # API Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Script Generation Constants
    MIN_CHAR_COUNT: int = 200
    MAX_CHAR_COUNT: int = 260
    TARGET_DURATION_MIN_SEC: int = 45
    TARGET_DURATION_MAX_SEC: int = 60

    # Korean reading speed (characters per minute)
    KOREAN_READING_SPEED: int = 270

    # Quality Review
    MAX_RETRY_COUNT: int = 2

    # Input Validation
    MIN_ETYMOLOGY_LENGTH: int = 30
    MIN_KOREAN_MEANING_LENGTH: int = 1

    # Section Names
    SECTION_NAMES = ["hook", "etymology", "context", "memory_anchor", "closing"]

    # LLM Generation
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 1000


settings = Settings()
