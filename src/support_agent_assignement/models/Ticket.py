from pydantic import BaseModel
from typing import Literal


class Ticket(BaseModel):

    id: str
    body: str
    channel: str
    subject: str
    received_at: str
    customer_plan: str







    