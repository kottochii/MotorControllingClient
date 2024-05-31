from flask import Flask
from flask_socketio import SocketIO

app = Flask("")
io = SocketIO(app)