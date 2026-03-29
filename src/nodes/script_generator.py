import json
import re
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from src.schemas.state import ScriptState
from src.config.settings import settings
from src.prompts.script_prompt import SYSTEM_PROMPT_TEMPLATE


def _extract_json(text: str) -> dict:
    """Extract JSON from LLM response, handling markdown code blocks."""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        text = match.group(1).strip()
    return json.loads(text)


def script_generator(state: ScriptState) -> ScriptState:
    """LangGraph node: generates a 4+1 section script via init_chat_model."""

    llm = init_chat_model(
        f"openai:{settings.OPENAI_MODEL}",
        temperature=settings.LLM_TEMPERATURE,
        max_tokens=settings.LLM_MAX_TOKENS,
        api_key=settings.OPENAI_API_KEY,
    )

    retry_feedback = state.get("review_feedback", "")
    user_content = f"""단어: {state['word']}
한국어 뜻: {state['korean_meaning']}
어원 설명: {state['etymology_explanation']}"""

    if retry_feedback:
        user_content += f"\n\n**이전 생성 피드백**:\n{retry_feedback}\n위 피드백을 반영하여 다시 작성하세요."

    messages = [
        SystemMessage(content=SYSTEM_PROMPT_TEMPLATE),
        HumanMessage(content=user_content),
    ]

    response = llm.invoke(messages)
    draft_script = _extract_json(response.content)

    for section in settings.SECTION_NAMES:
        if section not in draft_script:
            draft_script[section] = ""

    return {
        **state,
        "draft_script": draft_script,
        "retry_count": state.get("retry_count", 0),
    }
