import datetime

from flask import Flask, request
from flask_socketio import SocketIO

from client import Client, BridgeClient, UserClient, ClientManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
io = SocketIO(app)


@app.route('/')
def index():
    result = ''

    for c in ClientManager.instance().all():
        result += 'id: %s, type: %s\n' % (c.id, c.type)

    return result


@io.on('connect')
def connect():
    pass


@io.on('register-client')
def connect(data):
    client_id = request.sid
    client_type = data['type']
    uuid = data['uuid']

    check = ClientManager.instance().find(uuid)

    if check is not None:
        ClientManager.instance().delete(uuid)

    if client_type == 'bridge':
        BridgeClient(client_id, uuid)
    elif client_type == 'user':
        UserClient(client_id, uuid, data['target'])
    else:
        Client(client_id, client_type, uuid)


@io.on('ping')
def ping():
    print("pong!", request.sid)


@io.on('disconnect')
def disconnect():
    pass


@io.on('unregister-client')
def disconnect(data):
    client_type = data['type']
    client_uuid = data['uuid']

    if client_type == 'bridge':
        pass
    ClientManager.instance().delete(client_uuid)

    print("disconnect")


@io.on('message')
def message(data):
    r = data['room']
    text = data['text']
    data['date'] = str(datetime.datetime.now())

    client = ClientManager.instance().find(data['uuid'])
    users = ClientManager.instance().find_users(client.uuid)

    for user in users:
        if r not in user.rooms:
            json = {
                'title': r,
                'caption': text
            }

            user.rooms.append(r)
            io.emit('room', json, room=user.id)

            print('room', request.sid)

        io.emit('message', data, room=user.id)

    print('message', request.sid)


@io.on('room')
def room(data):
    client = ClientManager.instance().find(data['uuid'])

    for r in client.rooms:
        io.emit('room', {
            'title': r,
            'caption': ''
        }, room=client.id)

    print('room', request.sid)


@io.on('send')
def send(data):
    uuid = data['uuid']

    client = ClientManager.instance().find(uuid)
    target = ClientManager.instance().find(client.target_id)

    io.emit('send', data, room=target.id)

    print('send', request.sid)


if __name__ == '__main__':
    io.run(app)
