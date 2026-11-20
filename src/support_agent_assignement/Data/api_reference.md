# Roosterly helpdesk API

This is the client's helpdesk. Your agent reads tickets from it and sends one decision per ticket back.
It behaves like a real production API: it is sometimes unavailable, it limits how fast you can call it,
and it refuses to answer a customer twice.

**Base URL:** `https://nakywgkztvzkihdjnwbc.supabase.co/functions/v1/helpdesk`

## Access

Send these two headers with every request:

```
Authorization: Bearer <the key from our email>
X-Candidate-Email: <the email address you applied with>
```

Optional, once: `X-Candidate-Name: <your full name>`.

The key is the same for every candidate in this round; your email address tells the helpdesk who you are.
Your account is created on your first request. Always use the same email address: a different address is a
different account. Keep the key out of your repo (use environment variables and a `.env.example`).

---

## Endpoints

| Method | Path | What it does |
|---|---|---|
| GET | `/status` | Your mode, and how many tickets are open and handled |
| GET | `/examples` | 10 example tickets with our labels and reasoning. Use them for your eval |
| GET | `/tickets?limit=10&cursor=<id>&status=open` | Tickets in your current set. `open` (default) = not yet handled, `all` = everything. Max 10 per page; follow `next_cursor` until it is `null` |
| GET | `/tickets/{id}` | One ticket, plus how it was handled (if it was) |
| POST | `/tickets/{id}/reply` | Send a reply to the customer |
| POST | `/tickets/{id}/handoff` | Hand the ticket to the human support team |
| POST | `/tickets/{id}/close` | Close without action (spam, empty) |
| POST | `/practice/reset` | Re-open all your tickets, so you can run again |

### A ticket

```json
{
  "id": "T005",
  "received_at": "2026-10-05T09:02:00+00:00",
  "channel": "email",
  "customer_plan": "Basis",
  "subject": "Nieuwe medewerker",
  "body": "Goedemorgen, hoe voeg ik een nieuwe medewerker toe aan ons rooster? ..."
}
```

### A labelled example (`GET /examples`)

```json
{
  "id": "E03",
  "subject": "Terugbetaling",
  "body": "We waren in augustus dicht wegens verbouwing. Kunnen we die maand terugkrijgen?",
  "label": {
    "language": "nl",
    "category": "billing",
    "priority": "P2",
    "action": "handoff",
    "reason": "Refund request. Client rule: refunds always go to a human."
  }
}
```

The examples are not part of your 30 tickets. You cannot send decisions for them.

### Sending a decision

`POST /tickets/T005/reply`

```json
{
  "language": "nl",
  "category": "question",
  "priority": "P4",
  "reason": "How-to question answered by FAQ F02. No urgency.",
  "draft_reply": "Hoi Anouk, ga naar Team → Medewerker toevoegen ...",
  "confidence": 0.93
}
```

| Field | Required | Values |
|---|---|---|
| `language` | always | `nl`, `en`, `de`: the language the customer wrote in |
| `category` | always | `bug`, `billing`, `feature_request`, `question`, `other` |
| `priority` | always | `P1` to `P4`, as defined in the brief |
| `reason` | always | One or two sentences: why this category, priority and action |
| `draft_reply` | for `reply` | The answer, in the customer's language |
| `handoff_note` | for `handoff` | What the support agent needs to know, in English |
| `confidence` | optional | Number from 0 to 1 |

---

## Errors you must handle

| Status | Error | Meaning | What your agent should do |
|---|---|---|---|
| 400 | `invalid_json`, `bad_request` | Malformed request | Fix the request |
| 400 | `missing_email` | No `X-Candidate-Email` header | Add it |
| 401 | `unauthorized` | Missing or wrong key | Check the key from our email |
| 404 | `not_found` | Unknown endpoint, or a ticket that is not in your current set | Check the id |
| 409 | `already_handled` | This ticket was already handled. A customer must never get two answers | Do not retry. Your agent should not have sent this |
| 422 | `validation_failed` | A field is missing or invalid. `problems` lists what | Fix the body |
| 429 | `rate_limited` | More than 5 requests per second | Wait `Retry-After` seconds, then retry |
| 503 | `service_unavailable` | Temporary failure. Nothing was saved | Retry with a short backoff |

About 1 in 20 calls to `/tickets` and to the three actions returns a 503 on purpose.

---

## Your final run

Run your agent as often as you like; `POST /practice/reset` re-opens all 30 tickets. When you are done,
do one clean run: reset, then let your agent handle all 30 tickets once. That last run stays in the helpdesk
and is what we score. You do not send us any output.

## When you are done

Reply to our email, before the deadline, with your repo link. See the brief, section 06.

---

## Example with curl

```bash
export HELPDESK=https://nakywgkztvzkihdjnwbc.supabase.co/functions/v1/helpdesk
export KEY=nrd_round_...          # from our email
export ME=you@example.com          # the address you applied with

curl -s -H "Authorization: Bearer $KEY" -H "X-Candidate-Email: $ME" "$HELPDESK/status"
curl -s -H "Authorization: Bearer $KEY" -H "X-Candidate-Email: $ME" "$HELPDESK/examples"
curl -s -H "Authorization: Bearer $KEY" -H "X-Candidate-Email: $ME" "$HELPDESK/tickets?limit=3"
curl -s -X POST -H "Authorization: Bearer $KEY" -H "X-Candidate-Email: $ME" -H "Content-Type: application/json" \
  -d '{"language":"nl","category":"question","priority":"P4","reason":"FAQ F02","draft_reply":"Hoi Anouk, ..."}' \
  "$HELPDESK/tickets/T005/reply"
```
