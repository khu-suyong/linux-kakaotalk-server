import time

from flask import Flask, request
from flask_socketio import SocketIO

from client import Client, BridgeClient, UserClient

HOST = '127.0.0.1'
PORT = 3000

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
io = SocketIO(app)


@app.route('/')
def index():
    result = ''

    for c in Client.all():
        result += f'id: {c.id}, type: {c.type}\n'

    return result


@io.on('connect')
def connect():
    print('connect', request.sid)


@io.on('register-client')
def connect(data):
    client_id = request.sid
    client_type = data['type']

    if type == 'bridge':
        BridgeClient(client_id)
    elif type == 'user':
        UserClient(client_id)
    else:
        Client(client_id, client_type)


@io.on('disconnect')
def disconnect():
    print('disconnect', request.sid)

    Client.delete(request.sid)


@io.on('message')
def message(data):
    Client.find(request.sid)

    room = data['room']
    sender = data['sender']
    text = data['text']


if __name__ == '__main__':
    io.run(app, host=HOST, port=PORT)
