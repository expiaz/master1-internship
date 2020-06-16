import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/libs/mirage')

import eventlet
eventlet.monkey_patch(time=True)

from flask import Flask, render_template
from flask_socketio import SocketIO

from mirage.core import app
from mirage.libs import utils,ble

server = Flask(__name__)
socketio = SocketIO(server, async_mode='eventlet')

'''
' STATE MANAGEMENT
'''

class State():
    
    @staticmethod
    def colorGenerator():
        i = 0
        colorPalette = '#2980b9,#f1c40f,#1abc9c,#8e44ad,#34495e'.split(',')
        while True:
            yield colorPalette[i % len(colorPalette)]
            i = i + 1

    def __init__(self):
        # thread instance for current attack
        self.task = None
        # colors for devices on radar map
        self.colors = {}

        self.palette = State.colorGenerator()

    def nextColor(self):
        return next(self.palette)

state = State()

def mirageLogger(level, message):
    socketio.emit('log', {
        'type': level,
        'message': message
    })

'''
' SERVER
'''

@server.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def onConnect():
    pass

@socketio.on('disconnect')
def onDisconnect():
    pass

'''
' CUSTOM EVENTS
'''

@socketio.on('startAttack')
def startAttack(payload):
    if state.task != None:
        return

    if payload['attack'] == 'scanDevice':

        def onDeviceFound(devices):
            for address, device in devices.items():
                if address not in state.colors:
                    state.colors[address] = state.nextColor()
                devices[address]['color'] = state.colors[address]
            socketio.emit('devicesUpdate', list(devices.values()))

        def scanDevices():
            m = utils.loadModule('ble_locate')
            m['DEVICE_CALLBACK'] = onDeviceFound
            m['SCAN_TYPE'] = 'devices'
            m['TIME'] = ''
            m.execute()
        
        state.mirage = app.App(homeDir=utils.initializeHomeDir())
        utils.registerLogger(mirageLogger)
        state.task = eventlet.spawn(scanDevices)

    elif payload['attack'] == 'scanConnection':

        def onConnectionFound(connections):
            socketio.emit('connectionsUpdate', list(connections.values()))

        def scanConnections():
            m = utils.loadModule('ble_locate')
            m['CONNECTION_CALLBACK'] = onConnectionFound
            m['SCAN_TYPE'] = 'connections'
            m['TIME'] = ''
            m.execute()

        state.mirage = app.App(homeDir=utils.initializeHomeDir())
        utils.registerLogger(mirageLogger)
        state.task = eventlet.spawn(scanConnections)

    socketio.emit('attackStarted', payload)

@socketio.on('stopAttack')
def stopAttack(payload):
    # never trust user input
    if state.task == None:
        return
    state.mirage.exit()
    state.task.kill()
    state.task = None
    socketio.emit('attackStopped')

'''
' MAIN
'''
socketio.run(server)

