#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/libs/mirage')

from mirage.core import app,argParser,loader
from mirage.libs import utils
from mock import mockMaster, mockSlave

if __name__ == '__main__':
    try:
        mainApp = app.App(homeDir=utils.initializeHomeDir())
        
        masterTask = utils.addTask(mockMaster)
        slaveTask = utils.addTask(mockSlave)
    except (KeyboardInterrupt,EOFError):
            mainApp.exit()