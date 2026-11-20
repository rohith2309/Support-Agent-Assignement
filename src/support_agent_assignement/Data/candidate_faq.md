# Take-home: questions candidates usually ask

Read this before you email us. If your question is not here, reply to the email the assignment came with.
We answer within one working day.

## Deadline

**When is the deadline?**
72 hours after we send the assignment. If it arrives on Monday, your delivery is due on Thursday, end of
day. The exact date and time are in our email. If something comes up, tell us before the deadline.

**Do I have to do it in one go?**
No. Work whenever you like before the deadline.

**What if I do not finish everything?**
Submit what you have and write in your README what you left out and what you would do next. An honest,
unfinished agent scores better than a rushed one you cannot explain.

## The helpdesk API

**Where are the address and the key?**
In the email the assignment came with. The key is the same for everyone in this round. Your email address
in the `X-Candidate-Email` header is what makes it your account.

**Which email address do I use?**
The one you applied with, every time. A different address creates a different account, and we will not find
your final run.

**I get 503 errors, or a 429. Is the API broken?**
No, that is on purpose. About 1 in 20 calls fails with a 503, and more than 5 calls a second gets a 429.
Handling this is part of the test. See `api_reference.md`.

**I get a 409.**
Your agent tried to handle a ticket that was already handled. A customer must never get two answers. Your
agent should prevent this, for example after a crash or a retry.

**Can I start the practice tickets again?**
Yes, as often as you like: `POST /practice/reset` re-opens all 30.

**Where are the labelled examples?**
In the API: `GET /examples` returns 10 tickets with our labels and reasoning. Use them for your eval.

**What is the final run?**
When you are done: `POST /practice/reset`, then let your agent handle all 30 tickets once. That last run
stays in the helpdesk and is what we score. You do not send us any output.

**The API is not responding at all.**
Wait a minute and try `GET /status`. If it still fails, email us. If the problem is on our side, we move
your deadline.

## The language

**Why are the tickets in Dutch when everything else is in English?**
Because the client's customers write in Dutch. The brief, the API, the help centre and our emails are in
English; only the customer tickets are not.

**I do not read Dutch. Is that a problem?**
No. Most engineers we place do not read Dutch either. Working with a language you cannot read is part of the
job and part of this test. How you handle it, and how you check that a Dutch reply is correct, is up to you.

**May I translate the tickets?**
Yes. Translate first, work in Dutch directly, or something else: all fine. Explain your choice and what it
costs under Decisions in your README.

**Which language should replies be in?**
The language the customer wrote in. Handoff notes for the support team are in English.

## Tools and models

**Which model or framework should I use?**
Any. Free tiers and local models are fine. A paid model should cost well under €1 for the whole assignment.
We do not reimburse costs.

**May I use Claude Code, Cursor, Copilot or ChatGPT to build it?**
Yes, please. That is how this job is done. Mention in your README how you used them. In the live session you
will explain your code and change it, so make sure you understand what you submit.

**Do I need a user interface?**
No. One command that runs the agent is enough.

## Delivering

**What do I send?**
Reply to our email before the deadline. Subject: `Take-home: <your full name>`. One line: your repo link. No
attachments.

**Public or private repo?**
Either. If it is private, give read access to the GitHub user `nordavo-hiring`.

**Do I send the output of my agent?**
No. Your agent's answers from the final run reach us through the helpdesk.

**Can I keep working after I send the email?**
You can, but we grade the repo as it was when your email arrived. Later commits are ignored.

**Do I need a video?**
No.

## After you send it

**What happens next?**
We score your final run and read your code, usually within 3 working days. Everyone gets written feedback.
If you pass, you get a link to book a 20-minute live session. Sharing your screen, you run your agent on new
tickets you have not seen, walk us through your code and make one small change. Have your setup ready to run.

**Who owns my code?**
You do. We do not use it for any client.

---

Nordavo · Groningen × Bangalore · info@nordavo.nl
