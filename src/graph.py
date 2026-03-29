from langgraph.graph import StateGraph, END
from src.schemas.state import ScriptState
from src.nodes.input_validator import input_validator
from src.nodes.script_generator import script_generator
from src.nodes.quality_reviewer import quality_reviewer
from src.nodes.formatter import formatter
from src.config.settings import settings


def should_retry(state: ScriptState) -> str:
    """Conditional edge: decide retry or proceed to formatter."""
    if state.get("quality_passed", False):
        return "formatter"
    elif state.get("retry_count", 0) < settings.MAX_RETRY_COUNT:
        return "script_generator"  # Retry
    else:
        return "formatter"  # Force proceed after max retries


def create_graph():
    """Create the complete LangGraph workflow with retry loop."""

    workflow = StateGraph(ScriptState)

    workflow.add_node("input_validator", input_validator)
    workflow.add_node("script_generator", script_generator)
    workflow.add_node("quality_reviewer", quality_reviewer)
    workflow.add_node("formatter", formatter)

    workflow.set_entry_point("input_validator")
    workflow.add_edge("input_validator", "script_generator")
    workflow.add_edge("script_generator", "quality_reviewer")

    workflow.add_conditional_edges(
        "quality_reviewer",
        should_retry,
        {
            "script_generator": "script_generator",
            "formatter": "formatter",
        },
    )

    workflow.add_edge("formatter", END)

    return workflow.compile()


graph = create_graph()
