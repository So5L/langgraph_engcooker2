"""Reusable test fixtures for script generation tests."""

VALID_INPUTS = [
    {
        "word": "ambiguous",
        "korean_meaning": "모호한, 애매한",
        "etymology_explanation": "라틴어 ambiguus에서 유래. ambi(양쪽) + agere(이끌다). 양쪽으로 이끌린다는 뜻에서 어느 쪽인지 불분명한 상태를 의미.",
    },
    {
        "word": "resilient",
        "korean_meaning": "회복력 있는, 탄력 있는",
        "etymology_explanation": "라틴어 resilire에서 유래. re(다시) + salire(뛰다, 튀다). 다시 튀어오른다는 뜻. 역경에서 회복하는 능력을 의미.",
    },
    {
        "word": "ephemeral",
        "korean_meaning": "덧없는, 일시적인",
        "etymology_explanation": "그리스어 ephemeros에서 유래. epi(위에) + hemera(하루). 하루 동안만 지속된다는 의미에서 짧고 덧없는 것을 뜻하게 됨.",
    },
]

INVALID_INPUTS = [
    {"word": "", "korean_meaning": "뜻", "etymology_explanation": "a" * 30},
    {"word": "test", "korean_meaning": "", "etymology_explanation": "a" * 30},
    {"word": "test", "korean_meaning": "뜻", "etymology_explanation": "short"},
]
