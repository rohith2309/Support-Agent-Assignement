from typing import Optional
from pydantic import BaseModel


class Ticket(BaseModel):

    id: str
    body: str
    channel: str
    subject: str
    received_at: str
    customer_plan: str



class TicketsResponse(BaseModel):
    tickets: list[Ticket]
    next_cursor: Optional[str] = None