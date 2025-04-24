from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    return {'messages': chat_history[-50:]}

@socketio.on('message')
def handle_message(msg):
    chat_history.append(msg)
    if len(chat_history) > 50:
        chat_history.pop(0)
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
