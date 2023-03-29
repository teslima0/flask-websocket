from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room,send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', {'username': username, 'message': username + ' has joined the chat'}, room=room)

@socketio.on('messages')
def on_messages(data):
    username = data['username']
    message = data['message']
    room = data['room']
    emit('message', {'username': username, 'message': message}, room=room, broadcast=True)

@socketio.on('message')
def on_message(data):
    username = data['username']
    message = data['message']
    room = data.get('room', 'default-room')

    emit('message', {'username': username, 'message': message}, room=room)

@socketio.on('chat-message')
def handle_chat_message(data):
    username = data['username']
    message = data['message']
    room = data['room']
    send({'username': username, 'message': message}, room=room)


if __name__ == '__main__':
    socketio.run(app)
