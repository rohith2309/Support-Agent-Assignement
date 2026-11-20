from pydantic import BaseModel, Field
from typing import Literal


class TicketFacts(BaseModel):
    language: Literal["en", "nl", "de"] = Field(
        description="The language the customer wrote the ticket in."
    )
    category: Literal["bug", "billing", "feature_request", "question", "other"] = Field(
        description=(
            "'bug' for crashes/errors; 'billing' for invoices/prices/plans/refunds; "
            "'feature_request' for new ideas/integrations not in the product; "
            "'question' for how-to or maintenance inquiries; "
            "'other' for spam, empty tickets, GDPR/AVG requests, or general messages."
        )
    )
    english_summary: str = Field(
        description="A concise 1-sentence summary of the customer's issue/question in English."
    )
    primary_intent: str = Field(
        description="Short phrase in English describing what the user wants (e.g. 'change VAT number on invoice', 'request refund')."
    )

    # --- P1 Signals ---
    many_users_affected: bool = Field(
        description="True ONLY if multiple users or an entire location/company are blocked right now (e.g. total outage)."
    )
    security_or_legal_risk: bool = Field(
        description="True ONLY for security incidents (breach, unauthorized access) or explicit legal threats. (Note: standard GDPR/AVG data access requests are NOT P1 legal threats)."
    )

    # --- P2 Signals ---
    customer_blocked: bool = Field(
        description="True if a customer/manager is blocked from performing a core task right now with no workaround (e.g., cannot publish next week's rota, cannot log in)."
    )
    money_or_contract_issue: bool = Field(
        description="True ONLY if actual money dispute, refund, overcharge, cancellation, or contract change is involved. False for simple pricing inquiries or how to download/edit invoice details."
    )
    refund_request: bool = Field(
        description="True if the customer asks for a refund, credit, or money back."
    )
    gdpr_request: bool = Field(
        description="True if the customer makes a personal data request (GDPR / AVG in Dutch, e.g., 'inzageverzoek' or data deletion)."
    )

    # --- P3 Signal ---
    has_issue_with_workaround: bool = Field(
        description="True if something is broken, crashing on one device, or unclear, but other staff/devices work or there is a workaround (e.g. app crashes on one old phone while others work)."
    )

    # --- Action Guardrails ---
    spam_or_empty: bool = Field(
        description="True ONLY if the ticket is spam (e.g. crypto/marketing ads) or completely empty/gibberish."
    )
    requires_mandatory_human_handoff: bool = Field(
        description=(
            "True if ANY of the client's mandatory human escalation rules apply: "
            "refunds or disputed charges, cancellations or contract changes, "
            "GDPR/AVG personal data requests, security incidents, legal threats, "
            "or customers threatening to leave."
        )
    )