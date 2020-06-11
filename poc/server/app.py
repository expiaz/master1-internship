import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/libs/mirage')

from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def onConnect():
    pass

@socketio.on('disconnect')
def onDisconnect():
    pass

@socketio.on('test')
def onTest(data):
    print('received test: ' + str(data['data']))
    socketio.emit('log', {
        'type': 'info',
        'message': 'Connected'
    })

socketio.run(app)