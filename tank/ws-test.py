from flask import session
from flask_socketio import emit

from tank.config import NAMESPACE
from .socket import socket

# merely for ws-test
@socket.on('my_event', namespace=NAMESPACE)
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socket.on('my_broadcast_event', namespace=NAMESPACE)
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)