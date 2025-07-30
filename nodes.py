"""Graph nodes for the essay writer workflow."""

from langchain_core.messages import SystemMessage, HumanMessage
from state import AgentState
from config import (
    PLAN_PROMPT, WRITER_PROMPT, REFLECTION_PROMPT, 
    RESEARCH_PLAN_PROMPT, RESEARCH_CRITIQUE_PROMPT
)
from models import get_model, get_search, Queries

# Initialize model and search clients
model = get_model()
search_client = get_search()


def plan_node(state: AgentState):
    """Create an essay plan based on the task."""
    messages = [
        SystemMessage(content=PLAN_PROMPT), 
        HumanMessage(content=state['task'])
    ]
    response = model.invoke(messages)
    return {"plan": response.content}


def research_plan_node(state: AgentState):
    """Research information based on the initial plan."""
    queries = model.with_structured_output(Queries).invoke([
        SystemMessage(content=RESEARCH_PLAN_PROMPT),
        HumanMessage(content=state['task'])
    ])
    
    content = state.get('content') or []
    
    for q in queries.queries:
        response = search_client.search(query=q, max_results=2)
        for r in response['results']:
            content.append(r['content'])
    
    return {"content": content}


def generation_node(state: AgentState):
    """Generate essay draft based on plan and research."""
    content = "\n\n".join(state.get('content') or [])
    user_message = HumanMessage(
        content=f"{state['task']}\n\nHere is my plan:\n\n{state['plan']}")
    
    messages = [
        SystemMessage(content=WRITER_PROMPT.format(content=content)),
        user_message
    ]
    
    response = model.invoke(messages)
    return {
        "draft": response.content, 
        "revision_number": state.get("revision_number", 0) + 1
    }


def reflection_node(state: AgentState):
    """Provide critique and feedback on the current draft."""
    messages = [
        SystemMessage(content=REFLECTION_PROMPT), 
        HumanMessage(content=state['draft'])
    ]
    response = model.invoke(messages)
    return {"critique": response.content}


def research_critique_node(state: AgentState):
    """Research additional information based on critique."""
    queries = model.with_structured_output(Queries).invoke([
        SystemMessage(content=RESEARCH_CRITIQUE_PROMPT),
        HumanMessage(content=state['critique'])
    ])
    
    content = state.get('content') or []
    
    for q in queries.queries:
        response = search_client.search(query=q, max_results=2)
        for r in response['results']:
            content.append(r['content'])
    
    return {"content": content}