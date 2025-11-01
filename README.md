# AI Receptionist Human-in-the-Loop System

## Overview

This project builds a human-in-the-loop AI receptionist system designed to manage customer relationships through phone interactions. The AI agent can receive calls, answer known questions instantly from a knowledge base, and escalate unknown queries to human supervisors. Supervisors resolve pending requests via a simple dashboard, after which the AI learns from these interactions to improve automatically.

## Features

- Simulated phone call handling with caller identification.
- Instant answers for known questions via a SQLite knowledge base.
- Automatic pending request creation when questions are unknown.
- Supervisor dashboard UI for viewing, answering, and resolving pending requests.
- Lifecycle management of requests: Pending, Resolved, and Unresolved.
- Prevention of duplicate pending requests for the same caller and question.
- Simple simulated notifications for customer follow-ups.
- Extensible architecture for future integration with LiveKit or webhook systems.

## Project Structure

- `agent.py` – Simulates incoming calls and runs AI agent logic.
- `db.py` – Database models and functions managing requests and knowledge base.
- `supervisor_dashboard.py` – Flask server hosting the supervisor UI.
- `templates/dashboard.html` – Dashboard frontend template for supervisors.
- `.env.local` – Local environment variables for configuration such as database URL and secret key.
- `agent_receptionist.db` – SQLite database file (auto-created on first run).

## Setup Instructions

1. Clone the repository:

cd ai-agent-receptionist

2. Create and activate a virtual environment:

source .venv/bin/activate # macOS/Linux
.venv\Scripts\activate # Windows

3. Install dependencies:

pip install -r requirements.txt

text

4. Create a `.env.local` file and add:

DATABASE_URL=sqlite:///agent_receptionist.db
SECRET_KEY=your_secret_key_here

text

## Running the Project

1. To simulate incoming calls and agent logic:

python agent.py

text

2. To start the supervisor dashboard (runs on http://localhost:5000):

python supervisor_dashboard.py

text

3. Use the dashboard to view pending requests and enter answers.

## Usage Notes

- The database file `agent_receptionist.db` is created on the first run automatically.
- Duplicate pending requests for the same caller and question are prevented.
- Supervisor answers update the knowledge base for future instant responses.
- You can clear the database by deleting `agent_receptionist.db` and restarting.

## Future Enhancements

- Integrate actual LiveKit audio call handling for real phone interactions.
- Implement webhook callbacks or SMS notifications for live updates.
- Extend dashboard with analytics and request history per caller.
- Add authentication and supervisor role management.