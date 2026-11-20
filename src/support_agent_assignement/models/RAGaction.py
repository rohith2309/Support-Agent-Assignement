from typing import Literal
from pydantic import BaseModel, Field


class RagActionDecision(BaseModel):
    can_answer_from_faq: bool = Field(
        description=(
            "True ONLY if the retrieved FAQ chunks directly and completely answer the "
            "customer's question/issue using strictly help-centre facts (and respecting customer_plan)."
        )
    )
    action: Literal["reply", "handoff"] = Field(
        description="'reply' if can_answer_from_faq is True; otherwise 'handoff'."
    )
    reason: str = Field(
        description="1-2 sentences explaining why this category, priority, and action were chosen."
    )
    draft_reply: str | None = Field(
        default=None,
        description="Required when action is 'reply'. Written in the customer's language using ONLY the FAQ chunks.",
    )
    english_reply_translation: str | None = Field(
        default=None,
        description="English translation of draft_reply so the developer can verify Dutch/German replies.",
    )
    handoff_note: str | None = Field(
        default=None,
        description="Required when action is 'handoff'. Short note in English for the support agent.",
    )