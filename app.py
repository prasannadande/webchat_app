from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, send
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)
socketio = SocketIO(app, manage_session=False)

users = {}  # username: password
chat_history = []

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users and users[uname] == pwd:
            session['username'] = uname
            return redirect(url_for('home'))
        error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname not in users:
            users[uname] = pwd
            return redirect(url_for('login'))
        else:
            return "Username already exists!"
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

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
    socketio.run(app, host='0.0.0.0', port=5000)
