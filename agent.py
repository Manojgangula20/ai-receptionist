import db
import time
# If you want a global agent object
from livekit_agent import LiveKitAgent
agent = LiveKitAgent()


def handle_incoming_call(question, caller_id):
    # Check if question already answered in knowledge base
    answer = db.lookup_answer(question)
    if answer:
        print(f"Agent: {answer}")
        print(f"---> Customer {caller_id} notified immediately with answer.\n")
        return answer

    # Check if there is already a pending request for this caller + question
    pending = db.get_pending_request(question, caller_id)
    if pending:
        print("Agent: Your request is still pending supervisor review.")
        print(f"---> Ticket #{pending.id} submitted at {pending.created.strftime('%Y-%m-%d %H:%M:%S')}")
        print("---> We’ll notify you once resolved.\n")
        return None

    # Otherwise, add a new pending request
    req_id = db.add_request(question, caller_id)
    print(f"Agent: Let me check with my supervisor and get back to you. [Request {req_id} created]")
    print(f"---> Customer {caller_id} will be contacted after supervisor resolves.\n")
    return None


def simulate_calls():
    test_calls = [
        ("What are your hours?", "caller001"),
        ("Can I book an appointment for a haircut?", "caller002"),
        ("Do you offer hair coloring services?", "caller003"),
        ("Do you offer hair coloring services?", "caller003"),  # Duplicate caller/question
        ("Can I book an appointment for a haircut?", "caller002"),  # Duplicate caller/question
        ("Do you offer hair coloring services?", "caller999"),  # Different caller, same question
        ("What are your hours?", "caller999"),  # Different caller, known answer
        ("What are your cancellation policies?", "caller998"),
        ("Is parking available at your location?", "caller997"),
        ("Do you offer group discounts?", "caller996"),
    ]
    for question, caller in test_calls:
        handle_incoming_call(question, caller)
        time.sleep(2)


if __name__ == "__main__":
    print("Agent system online. Simulating calls...\n")
    simulate_calls()
    print("Check supervisor dashboard at http://localhost:5000 to resolve requests!")
