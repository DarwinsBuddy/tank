from flask import copy_current_request_context, session
from flask_socketio import disconnect, emit

from tank import AppConfig


def setup(socket, config: AppConfig):
    @socket.on('disconnect_request', namespace=config.socketio_namespace)
    def disconnect_request():
        @copy_current_request_context
        def can_disconnect():
            disconnect()

        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'Disconnected!', 'count': session['receive_count']},
             callback=can_disconnect)
