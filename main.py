import json
import sys
from src.schemas.input import ScriptInput
from src.schemas.output import ScriptOutput
from src.graph import graph


def run(word: str, korean_meaning: str, etymology_explanation: str) -> ScriptOutput:
    """Run the script generation pipeline and return a ScriptOutput."""

    input_data = ScriptInput(
        word=word,
        korean_meaning=korean_meaning,
        etymology_explanation=etymology_explanation,
    )

    result = graph.invoke(input_data.model_dump())

    return ScriptOutput(
        word=result["word"],
        script=result["draft_script"],
        full_script=result["full_script"],
        estimated_duration_sec=result["estimated_duration_sec"],
        quality_score=result["quality_score"],
        quality_passed=result.get("quality_passed", False),
    )


if __name__ == "__main__":
    # Example usage
    example = {
        "word": "protect",
        "korean_meaning": "보호하다",
        "etymology_explanation": "protect 라는 동사가 있다. ‘pro(앞에서) + tect(덮다)’. 즉 앞에서 방어하고 덮어주는 것. ‘보호한다’는 소리다. 전쟁 영화를 떠올려보면, 자기편을 ‘보호하기’ 위해 ‘앞에서’ 목숨을 걸고 적군을 막아낸다.",
    }

    try:
        output = run(**example)
        print(json.dumps(output.model_dump(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
