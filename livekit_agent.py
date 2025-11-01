import db
import os
from dotenv import load_dotenv
import requests


BUSINESS_PROMPT = """

You are assisting callers for Glamour Essence Salon, a premier beauty and hair care destination located in downtown. This salon offers a wide range of services including:

1. Haircuts, styling, and coloring for men, women, and children

2. Manicure and pedicure with premium nail care treatments

3. Facials, skin treatments, and professional makeup services

4 Relaxing massages including Swedish, deep tissue, and hot stone therapies

5. Bridal and special event hairstyling and beautification

The salon operates Monday through Saturday from 9 AM to 7 PM, and is closed on Sundays. Walk-ins are accepted but appointments are recommended to guarantee availability. The salon is known for its friendly staff, hygienic environment, and use of high-quality products.

For bookings and inquiries, callers can request appointments, check available services, pricing details, and operating hours.

"""
load_dotenv(dotenv_path='.env.local')

class LiveKitAgent:
    def __init__(self, livekit_url=None, api_key=None, api_secret=None):
        self.livekit_url = livekit_url or os.environ.get("LIVEKIT_URL")
        self.api_key = api_key or os.environ.get("LIVEKIT_API_KEY")
        self.api_secret = api_secret or os.environ.get("LIVEKIT_API_SECRET")
        self.knowledge_base = self.load_knowledge()

    def load_knowledge(self):
        answers = db.session.query(db.Answer).all()
        return {a.question.lower(): a.answer for a in answers}

    def on_participant_joined(self, participant):
        print(f"Call started from {participant.identity}")
        print("Greeting with business info:")
        print(BUSINESS_PROMPT)

    def on_message_received(self, participant, message):
        question = message.content.lower()
        print(f"Received from {participant.identity}: {question}")

        answer = self.knowledge_base.get(question)
        if answer:
            print(f"Answering immediately: {answer}")
            print(f"Sending answer to {participant.identity}: {answer}")
        else:
            print("Unknown question, escalating...")
            existing = db.get_pending_request(question, participant.identity)
            if not existing:
                req_id = db.add_request(question, participant.identity)
                print(f"Help request [ID {req_id}] created.")
                print(f"Notify supervisor: Hey, I need help answering '{question}'.")
            else:
                print("Help request already exists, not duplicating.")

    def get_active_livekit_rooms():
        livekit_url = os.environ.get("LIVEKIT_URL")
        api_key = os.environ.get("LIVEKIT_API_KEY")
        api_secret = os.environ.get("LIVEKIT_API_SECRET")
        if not (livekit_url and api_key and api_secret):
            # Handle missing config
            return []

        # The rooms listing endpoint (docs: https://docs.livekit.io/api/server-rest/#list-rooms)
        url = f"{livekit_url}/api/v1/rooms"

        # Use basic auth for LiveKit
        response = requests.get(url, auth=(api_key, api_secret))
        if response.status_code == 200:
            data = response.json()
            return data.get('rooms', [])
        else:
            print("LiveKit API error:", response.text)
            return []
    def update_knowledge(self, question, answer):
        self.knowledge_base[question] = answer
        # Optionally save to disk/db for persistence

    def notify_caller_via_webhook(caller_id, message):
        webhook_url = "https://example.com/notify-caller"
        payload = {"caller": caller_id, "message": message}
        requests.post(webhook_url, json=payload)
if __name__ == "__main__":
    # You can add LiveKit connection logic here or use mocks in testing
    pass
