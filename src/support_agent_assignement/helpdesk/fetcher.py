import httpx
from support_agent_assignement.helpdesk.client import HelpdeskClient
from support_agent_assignement.helpdesk.schema import Ticket


async def fetch_all_open_tickets(client:HelpdeskClient)-> list[Ticket]:

    cursor=None
    all_tickets=[]
    while True:

        page = await client.fetch_open_tickets(cursor=cursor)

        all_tickets.extend(page.tickets)

        if not page.next_cursor:
            break

        cursor = page.next_cursor

    return all_tickets    

