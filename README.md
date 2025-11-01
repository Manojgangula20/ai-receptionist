# AI Receptionist – Human-in-the-Loop

## Overview

This project implements a first-version AI receptionist system featuring human-in-the-loop escalation for unknown customer queries. The system receives calls (via LiveKit), answers from its knowledge base, and escalates unresolved queries to a human supervisor for learning and follow-up.

## Features

- **Inbound Telephony Agent:** Receives phone calls and greets users.
- **Knowledge Base:** Instantly answers known questions with learned responses.
- **Human Escalation:** Routes unknown queries to a supervisor dashboard for review.
- **Supervisor Dashboard (Flask):** View, resolve, and mark customer queries as pending, resolved, or unresolved (timed out).
- **Automatic Learning:** Updates knowledge base with supervisor-provided answers for future calls.
- **Audit & History:** Tracks query/answer history by caller and as learned knowledge.

## Project Structure

```
AI-RECEPTIONIST/
│
├── agent.py             # AI agent (LiveKit inbound calls + escalation)
├── db.py                # Database models and query/answer management
├── supervisor_dashboard.py (or app.py) 
│                        # Flask dashboard for supervisors
├── templates/
│   ├── base.html        # Shared layout/navigation
│   ├── dashboard.html   # Pending requests tab
│   ├── resolved.html    # Resolved requests tab
│   ├── unresolved.html  # Unresolved (timed out) requests
│   ├── learned_answers.html # Learned KB
│   └── caller_history.html  # Caller-specific history
├── static/
│   └── dashboard.css    # Dashboard and status styling
└── README.md            # (This file)
```

## Setup & Run

1. **Install Python requirements**
    ```
    pip install -r requirements.txt
    ```

2. **Set environment variables**
    - (In `.env.local`)
      ```
      LIVEKIT_URL=ws://your-livekit-server
      LIVEKIT_API_KEY=your-key
      LIVEKIT_API_SECRET=your-secret
      ```

3. **Initialize DB**  
    - First run will auto-create `agent_receptionist.db`

4. **Start Agent (inbound only for Phase 1)**
    ```
    uv run agent.py dev
    ```
    - The agent will greet new callers, answer if possible, or escalate to supervisor if unknown.

5. **Start Supervisor Dashboard**
    ```
    python supervisor_dashboard.py
    ```
    - Visit [http://localhost:5000/](http://localhost:5000/) to view, resolve, and manage all requests.

6. **Testing**
    - Simulate inbound calls through LiveKit (see agent.py for demo calls or test via SIP/web).
    - Pending requests appear on the main dashboard for supervisor review.
    - Resolved/unresolved/learned answers update in respective tabs.

## Usage Example

- **Customer calls:** "What are your hours?" → agent checks KB, responds or escalates.
- **Supervisor reviews dashboard:** resolves pending request, adds answer.
- **Future calls** with same question get instant answer.

## Extensibility & Next Steps

- Timed automatic marking from pending → unresolved (see db.py).
- Support for outbound calling, live call transfer, and webhook notifications can be added in Phase 2.
- Basic concurrency/scalability notes: upgrade to Postgres for production or multi-agent use.

## Current Limitations

- **Only inbound (not outbound) telephony in Phase 1.**
- **No live call transfer or direct human callback (Phase 2 feature).**
- **No multi-lingual/call analytics support.**
- **Basic error handling—production systems should add retries/logs.**
