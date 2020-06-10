import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/libs/mirage')

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'