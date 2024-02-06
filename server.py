from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_httpauth import HTTPBasicAuth
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
auth = HTTPBasicAuth()

users = {
    os.environ.get("USER"): os.environ.get("PASS"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
@auth.login_required
def index():
    return send_from_directory('public', 'index.html')

@app.route('/log', methods=['POST'])
@auth.login_required
def log():
    log_msg = request.json.get('log')
    print('Received log:', log_msg)
    socketio.emit('newLog', log_msg)
    return {'status': 'Log received'}

@app.route('/healthz', methods=['GET'])
def health_check():
    return {'status': 'UP'}

@socketio.on('connection')
def handle_connection():
    print('A USER IS CONNECTED')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    if 'eventlet' in socketio.server_options['async_mode']:
        import eventlet
        eventlet.monkey_patch()
        print("EVENTLET")
        socketio.run(app, host='0.0.0.0', port=port, debug=False)
    else:
        print("NOT EVENTLET")
        socketio.run(app, host='0.0.0.0', port=port, debug=False)
