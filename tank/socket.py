from flask import copy_current_request_context, session
from flask_socketio import disconnect, emit

from .config import NAMESPACE


def setup(socket):
    @socket.on('disconnect_request', namespace=NAMESPACE)
    def disconnect_request():
        @copy_current_request_context
        def can_disconnect():
            disconnect()

        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'Disconnected!', 'count': session['receive_count']},
             callback=can_disconnect)
