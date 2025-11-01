import db
import os
from dotenv import load_dotenv

BUSINESS_PROMPT = """
You are assisting callers for Glamour Essence Salon, a premier beauty and hair care destination located in downtown. This salon offers a wide range of services including:

1. Haircuts, styling, and coloring for men, women, and children
2. Manicure and pedicure with premium nail care treatments
3. Facials, skin treatments, and professional makeup services
4. Relaxing massages including Swedish, deep tissue, and hot stone therapies
5. Bridal and special event hairstyling and beautification

The salon operates Monday through Saturday from 9 AM to 7 PM, and is closed on Sundays. Walk-ins are accepted but appointments are recommended to guarantee availability. The salon is known for its friendly staff, hygienic environment, and use of high-quality products.

For bookings and inquiries, callers can request appointments, check available services, pricing details, and operating hours.
"""

load_dotenv(dotenv_path='.env.local')

class LiveKitAgent:
    def __init__(self):
        self.business_prompt = BUSINESS_PROMPT
        self.knowledge_base = self.load_knowledge()

    def load_knowledge(self):
        answers = db.session.query(db.Answer).all()
        return {a.question.lower(): a.answer for a in answers}

    def greet(self):
        return self.business_prompt

    def get_answer(self, question):
        return self.knowledge_base.get(question.lower())

    def update_knowledge(self, question, answer):
        self.knowledge_base[question.lower()] = answer
        # Persisted update to db.Answer handled through supervisor resolution


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
