from support_agent_assignement.helpdesk.client import HelpdeskClient

async def submit_ticket(client: HelpdeskClient,ticket_id: str, action: str, payload: dict) -> dict:

    response = await client.submit_decision(ticket_id=ticket_id, action=action, payload=payload)
    return response