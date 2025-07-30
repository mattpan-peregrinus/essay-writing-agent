"""Graph construction for the essay writer workflow."""

from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import (
    plan_node, generation_node, reflection_node,
    research_plan_node, research_critique_node
)


def should_continue(state):
    """Determine whether to continue with revisions or end."""
    if state["revision_number"] > state["max_revisions"]:
        return END
    return "reflect"


def create_essay_graph():
    """Create and compile the essay writer graph."""
    builder = StateGraph(AgentState)
    
    # Add nodes
    builder.add_node("plan", plan_node)
    builder.add_node("research_plan", research_plan_node)
    builder.add_node("generate", generation_node)
    builder.add_node("reflect", reflection_node)
    builder.add_node("research_critique", research_critique_node)
    
    # Set entry point
    builder.set_entry_point("plan")
    
    # Add edges
    builder.add_edge("plan", "research_plan")
    builder.add_edge("research_plan", "generate")
    builder.add_edge("reflect", "research_critique")
    builder.add_edge("research_critique", "generate")
    
    # Add conditional edge for revision loop
    builder.add_conditional_edges(
        "generate",
        should_continue,
        {END: END, "reflect": "reflect"}
    )
    
    return builder.compile()