from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from random import random
import string

app = Flask(__name__)
socketio = SocketIO(app)

active_sessions = {}

def generate_session_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('create_session')
def handle_create_session():
    session_id = generate_session_id()
    active_sessions[session_id] = []
    emit('session_created', {'session_id': session_id}, broadcast=True)

@socketio.on('join_session')
def handle_join_session():
    session_id = data['session_id']
    if session_id in active_sessions:
        active_sessions[session_id].append(request.sid)
        emit('joined_session', {'session_id': session_id}, room=request.sid)
        emit('user_joined', {'user_id': request.sid}, room=session_id)

@socketio.on('disconnect')
def handle_disconnect():
    for session_id, users in active_sessions.items():
        if request.sid in users:
            users.remove(request.sid)
            emit('user_left', {'user_id': request.sid}, room=session_id)

        if __name__ == '__main__':
            socketio.run(app)