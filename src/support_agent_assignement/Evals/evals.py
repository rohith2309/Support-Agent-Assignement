import asyncio
import json
from pathlib import Path
from ..helpdesk.schema import Ticket
from ..graph.workflow import build_ticket_graph

graph = build_ticket_graph()

async def run_eval(
    examples_path: str | Path = Path(__file__).resolve().parents[1] / "Data" / "example.json",
):
    raw_data = json.loads(Path(examples_path).read_text(encoding="utf-8"))
    examples = raw_data["examples"] if isinstance(raw_data, dict) else raw_data

    total = len(examples)
    exact_matches = 0
    field_scores = {"language": 0, "category": 0, "priority": 0, "action": 0}

    for item in examples:
        label = item["label"]
        ticket = Ticket.model_validate({k: v for k, v in item.items() if k != "label"})

        result = await graph.ainvoke({"ticket": ticket})
        payload = result["payload"]
        pred = {
            "language": payload["language"],
            "category": payload["category"],
            "priority": payload["priority"],
            "action": result["action"],
        }

        all_ok = True
        for field in field_scores:
            if pred[field] == label[field]:
                field_scores[field] += 1
            else:
                all_ok = False

        if all_ok:
            exact_matches += 1

        status = "PASS" if all_ok else "FAIL"
        print(f"[{status}] {ticket.id}: pred={pred} | expected={ {k: label[k] for k in field_scores} }")

        # Print English summary/translation so you can verify Dutch replies without reading Dutch
        if pred["action"] == "reply":
            print(f"       Draft ({pred['language']}): {payload.get('draft_reply')}")
            print(f"       Summary (en): {result['facts'].english_summary}\n")
        elif not all_ok:
            print(f"       Reason: {payload.get('reason')}\n")
        
        await asyncio.sleep(1.5)    

    print("-" * 60)
    print(f"Exact Match: {exact_matches}/{total}")
    for field, count in field_scores.items():
        print(f"  {field}: {count}/{total}")


if __name__ == "__main__":
    asyncio.run(run_eval())