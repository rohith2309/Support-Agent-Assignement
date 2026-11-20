from typing import TypedDict

from support_agent_assignement.models.Ticket import Ticket
from support_agent_assignement.models.Ticketfacts import TicketFacts


class AgentState(TypedDict):
    ticket: Ticket

    facts: TicketFacts | None

    priority: str | None

    faq_chunks: list[str]

    action: str | None

    payload: dict | None