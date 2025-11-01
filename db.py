from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

Base = declarative_base()

class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    caller = Column(String, nullable=False)
    status = Column(String, default='pending')
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    answer = Column(Text)

class Answer(Base):
    __tablename__ = 'answers'
    question = Column(Text, primary_key=True)
    answer = Column(Text)

engine = create_engine('sqlite:///agent_receptionist.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_request(question, caller):
    # Check if question already answered in knowledge base
    kb = session.query(Answer).filter_by(question=question).first()
    if kb:  # Already answered, no need to add request
        return None

    # Optional: Check if a pending request is already present for that question+caller
    existing = session.query(Request).filter_by(question=question, caller=caller, status='pending').first()
    if existing:
        return existing.id

    req = Request(question=question, caller=caller)
    session.add(req)
    session.commit()
    return req.id

def resolve(req_id, answer):
    req = session.query(Request).filter_by(id=req_id).first()
    if req:
        req.status = 'resolved'
        req.answer = answer
        session.commit()
        # Update knowledge base
        kb = session.query(Answer).filter_by(question=req.question).first()
        if kb:
            kb.answer = answer
        else:
            kb = Answer(question=req.question, answer=answer)
            session.add(kb)
        session.commit()
        return True
    return False

def get_unresolved():
    return session.query(Request).filter_by(status='pending').all()

def get_resolved():
    return session.query(Request).filter_by(status='resolved').all()

def lookup_answer(question):
    kb = session.query(Answer).filter_by(question=question).first()
    return kb.answer if kb else None

def get_pending_request(question, caller):
    return session.query(Request).filter_by(question=question, caller=caller, status='pending').first()

def get_requests_by_caller(caller_id):
    return session.query(Request).filter_by(caller=caller_id).order_by(Request.created.desc()).all()

def notify_customer(caller, message):
    # Simulate sending notification
    print(f"[Notification] To {caller}: {message}")

def search_requests(search_term, status=None):
    query = session.query(Request)
    if status:
        query = query.filter(Request.status == status)
    if search_term:
        like_term = f"%{search_term}%"
        query = query.filter((Request.question.ilike(like_term)) | (Request.caller.ilike(like_term)))
    return query.order_by(Request.created.desc()).all()

def get_request_by_id(req_id):
    return session.query(Request).filter_by(id=req_id).first()

def notify_caller(request_obj, answer):
    print(f"[AI Agent] Notifying caller '{request_obj.caller}': '{answer}'")
    # Implement webhook/SMS here




