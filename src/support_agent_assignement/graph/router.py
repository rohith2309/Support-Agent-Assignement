from support_agent_assignement.graph.states import AgentState

def RAG_decision_router(agentState: AgentState):
    facts = agentState["facts"]
    
    if facts.spam_or_empty:
        return "close"
    elif facts.requires_mandatory_human_handoff:
        return "handoff"
    return "retrieve_faq"
    