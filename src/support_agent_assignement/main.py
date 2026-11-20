import json
import asyncio
from datetime import datetime, timezone
from pathlib import Path

from support_agent_assignement.utils.sanitizer import sanitize_text
from support_agent_assignement.helpdesk.client import HelpdeskClient
from support_agent_assignement.helpdesk.fetcher import fetch_all_open_tickets
from support_agent_assignement.helpdesk.submitter import submit_ticket
from support_agent_assignement.graph.workflow import build_ticket_graph

LOG_FILE = Path("logs/tickets.jsonl")
graph = build_ticket_graph()


def load_processed_ids() -> set[str]:
    if not LOG_FILE.exists():
        return set()
    processed = set()
    for line in LOG_FILE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entry = json.loads(line)
            if entry.get("status") in {"submitted", "already_handled"}:
                processed.add(entry["ticket_id"])
    return processed


def write_ticket_log(record: dict) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    safe_line = sanitize_text(json.dumps(record, ensure_ascii=False))
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(safe_line + "\n")

async def main():
    client = HelpdeskClient()
    processed_ids = load_processed_ids()

    try:
        tickets = await fetch_all_open_tickets(client)
        if not tickets:
            print("No open tickets found.")
            return
        print(f"Fetched {len(tickets)} open tickets. Processing...")
        
        for ticket in tickets:
            if ticket.id in processed_ids:
                print(f"[{ticket.id}] Already logged locally, skipping.")
                continue

            result_state = await graph.ainvoke({"ticket": ticket})
            action = result_state["action"]
            payload = result_state["payload"]

            outcome = await submit_ticket(
                client,
                ticket_id=ticket.id,
                action=action,
                payload=payload,
            )

            write_ticket_log(
                {
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "ticket_id": ticket.id,
                    "action": action,
                    "category": payload["category"],
                    "priority": payload["priority"],
                    "language": payload["language"],
                    "reason": payload["reason"],
                    "status": outcome["status"],
                }
            )
            print(f"[{ticket.id}] {action} -> {outcome['status']}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())