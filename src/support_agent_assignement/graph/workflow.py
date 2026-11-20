from langgraph.graph import StateGraph, START, END
from support_agent_assignement.graph.states import AgentState
from support_agent_assignement.graph.nodes import (
    extract_and_classify_ticket,
    assign_priority_node,
    retrieve_faq_node,
    decide_and_draft_node,
    close_ticket_node,
    handoff_ticket_node
)
from .router import RAG_decision_router

# Assuming RAG_decision_router(agentState: State) -> str returns:
# "close", "handoff", or "retrieve_faq"

def build_ticket_graph():
    builder = StateGraph(AgentState)

    builder.add_node("extract_and_classify", extract_and_classify_ticket)
    builder.add_node("assign_priority", assign_priority_node)
    builder.add_node("retrieve_faq", retrieve_faq_node)
    builder.add_node("decide_and_draft", decide_and_draft_node)
    builder.add_node("close_ticket", close_ticket_node)
    builder.add_node("handoff_ticket", handoff_ticket_node)

    builder.add_edge(START, "extract_and_classify")
    builder.add_edge("extract_and_classify", "assign_priority")

    builder.add_conditional_edges(
        "assign_priority",
        RAG_decision_router,
        {
            "close": "close_ticket",
            "handoff": "handoff_ticket",
            "retrieve_faq": "retrieve_faq",
        },
    )

    builder.add_edge("retrieve_faq", "decide_and_draft")
    builder.add_edge("decide_and_draft", END)
    builder.add_edge("close_ticket", END)
    builder.add_edge("handoff_ticket", END)

    return builder.compile()