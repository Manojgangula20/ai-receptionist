from flask import Flask, render_template, request, redirect, url_for
import db
from datetime import datetime, timezone

app = Flask(__name__)

@app.route('/')
def dashboard():
    pending = db.get_pending()
    return render_template('dashboard.html', pending=pending)

@app.route('/resolved')
def resolved():
    resolved_requests = db.get_resolved()
    return render_template('resolved.html', resolved=resolved_requests)

@app.route('/unresolved')
def unresolved():
    unresolved_requests = db.get_unresolved()
    return render_template('unresolved.html', unresolved=unresolved_requests)

@app.route('/answer', methods=['POST'])
def answer():
    req_id = request.form.get('req_id')
    answer_text = request.form.get('answer')
    if not req_id or not answer_text:
        return redirect('/')
    req_id = int(req_id)
    db.resolve(req_id, answer_text)
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
