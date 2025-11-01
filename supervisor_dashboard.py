from flask import Flask, render_template, request, redirect, url_for
import db
from datetime import datetime, timezone
from livekit_agent import LiveKitAgent
agent = LiveKitAgent()

app = Flask(__name__)


@app.route('/')
def dashboard():
    search = request.args.get('search', '').strip()
    status_filter = request.args.get('status', 'all')

    if status_filter == 'pending':
        pending = db.search_requests(search, status='pending')
        resolved = []
    elif status_filter == 'resolved':
        resolved = db.search_requests(search, status='resolved')
        pending = []
    else:  # 'all'
        pending = db.search_requests(search, status='pending')
        resolved = db.search_requests(search, status='resolved')

    # Fetch all learned answers for display in separate section
    return render_template('dashboard.html', pending=pending, resolved=resolved,
                           search=search, status_filter=status_filter
                           )

@app.route('/live_calls')
def live_calls():
    rooms = db.get_active_livekit_rooms()  # or define this elsewhere
    active_calls = []
    for room in rooms:
        active_calls.append({
            'caller_id': room['name'],
            'call_id': room['name'],
            'status': 'active',
            'duration': f"{int(room['duration'] // 60):02d}:{int(room['duration'] % 60):02d}"
        })
    return render_template('live_calls.html', active_calls=active_calls)

@app.route('/answer', methods=['POST'])
def answer():
    req_id = request.form.get('req_id')
    answer_text = request.form.get('answer')

    if not req_id or not answer_text:
        return redirect('/')

    req_id = int(req_id)
    req = db.session.get(db.Request, req_id)
    if req is None:
        print(f"[ERROR] Request {req_id} not found")
        return redirect('/')

    req.answer = answer_text
    req.status = 'resolved'
    req.answered = datetime.now(timezone.utc)
    db.session.commit()

    # Notify caller
    print(f"[Notification] To {req.caller}: {req.question} — {answer_text}")
    print(f"Agent: Supervisor resolved request {req_id} - Customer notified")

    # Update agent in-memory KB
    agent.update_knowledge(req.question, req.answer)

    # ---- Update database table Answer for persistent learned answers ----
    # Assuming db.Answer(question=..., answer=...)
    answer_row = db.session.query(db.Answer).filter_by(question=req.question).first()
    if answer_row:
        answer_row.answer = answer_text
    else:
        new_answer = db.Answer(question=req.question, answer=answer_text)
        db.session.add(new_answer)
    db.session.commit()
    # ----------------------------------------------------

    return redirect(url_for('dashboard'))


@app.route('/caller/<caller_id>')
def caller_history(caller_id):
    requests = db.get_requests_by_caller(caller_id)
    return render_template('caller_history.html', requests=requests, caller=caller_id)

@app.route('/learned_answers')
def learned_answers():
    answers = db.session.query(db.Answer).order_by(db.Answer.question).all()
    return render_template('learned_answers.html', answers=answers)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
