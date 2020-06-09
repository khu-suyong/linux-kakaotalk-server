from flask import Flask
from flask_socketio import SocketIO, emit

HOST = 'localhost'
PORT = 3000

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
io = SocketIO(app)


@app.route('/')
def index():
    print('test')
    return 'test'


@io.on('connect')
def connect():
    print('receive connect')


@io.on('message')
def test_message(message):

    print('receive message')
    print(type(message), message)
    print(message['room'], message['sender'], message['text'])


if __name__ == '__main__':
    io.run(app, host=HOST, port=PORT)
