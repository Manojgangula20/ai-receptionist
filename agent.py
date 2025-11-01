import db
import asyncio
from livekit.agents import AgentSession, cli, WorkerOptions
from livekit_agent import LiveKitAgent

agent = LiveKitAgent()

async def hangup_call(session):
    from livekit import api
    await session.context.api.room.delete_room(api.DeleteRoomRequest(room=session.context.room.name))

async def detected_voicemail(session):
    await session.generate_reply(instructions="Leaving a voicemail letting you know we'll call back later.")
    await asyncio.sleep(0.5)
    await hangup_call(session)

async def entrypoint(session: AgentSession):
    caller_id = session.participant.identity if (hasattr(session, "participant") and session.participant) else None
    await session.generate_reply(
        instructions=agent.greet()
    )

    while True:
        user_message = await session.receive_message()
        if user_message is None:
            break

        question = user_message.text
        print(f"[Agent] Caller ({caller_id}) asked: {question}")

        # Voicemail detection (customize this as needed)
        if "voicemail" in question.lower() or "answering machine" in question.lower():
            await detected_voicemail(session)
            break

        answer = agent.get_answer(question)
        if answer:
            await session.generate_reply(text=answer)
            continue

        pending = db.get_pending_request(question, caller_id)
        if pending:
            await session.generate_reply(text="Your request is still pending supervisor review, please wait.")
            continue

        req_id = db.add_request(question, caller_id)
        await session.generate_reply(
            text="Let me check with my supervisor and get back to you soon. Your request will be reviewed."
        )
        print(f"[Agent] Escalation: Request {req_id} created for {caller_id}")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(
        entrypoint_fnc=entrypoint,
        agent_name="my-telephony-agent"
    ))
