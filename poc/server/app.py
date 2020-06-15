import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/libs/mirage')

from flask import Flask, render_template
from flask_socketio import SocketIO

from mirage.core import app
from mirage.libs import utils

server = Flask(__name__)
socketio = SocketIO(server)

mirage = app.App(homeDir=utils.initializeHomeDir())

@server.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def onConnect():
    pass

@socketio.on('disconnect')
def onDisconnect():
    pass


@socketio.on('startAttack')
def startAttack(payload):
    if payload['attack'] == 'scan':
        m = utils.loadModule('ble_locate')
        m['DEVICE_CALLBACK'] = onDeviceFound
        m['SCAN_TYPE'] = 'devices'
        m['TIME'] = '5'
        m.execute()

        m = utils.loadModule('ble_locate')    
        m['CONNECTION_CALLBACK'] = onConnectionFound
        m['SCAN_TYPE'] = 'connections'
        m['TIME'] = '100'
        m.execute()

        socketio.emit('log', {
            'type': 'success',
            'message': 'Scan finished successfully'
        })
        socketio.emit('attackFinished')

    elif payload['attack'] == 'spoofing':
        m = utils.loadModule('ble_mitm')
        m['TARGET'] = payload['target']

    elif payload['attack'] == 'hijack':
        m = utils.loadModule('ble_sniff')
        m['SNIFFING_MODE'] = 'existingConnections'
        m['HIJACK'] = 'yes'
        m['TARGET'] = payload['target']


def stepLogger(level, message):
    socketio.emit('log', {
        'type': level,
        'message': message
    })

utils.registerLogger(stepLogger)


def onDeviceFound(devices):
    print(devices)
    socketio.emit('devicesUpdate', devices)

def onConnectionFound(connections):
    socketio.emit('connectionsUpdate', connections)

try:
    socketio.run(server)
except (KeyboardInterrupt,EOFError):
    mirage.exit()

