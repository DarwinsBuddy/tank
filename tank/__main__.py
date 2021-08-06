import argparse
import os

from flask import render_template, copy_current_request_context, session, send_from_directory, jsonify, request
from flask_socketio import emit, disconnect

from tank.web import AppWrapper


parser = argparse.ArgumentParser(description='Tank WebUI')
parser.add_argument('-e', '--env', nargs=1, help='Environment (dev|prod) default: dev', type=str, default='dev')
parser.add_argument('-m', '--mock', action='store_true', help='Start with mocked measurements', default=False)
parser.add_argument('-zp', '--zmq-port', type=int, nargs=1, help='Listen port for zmq subscriber', default=5555)
parser.add_argument('-za', '--zmq-addr', type=str, nargs=1, help='Listen address for zmq subscriber',
                    default='127.0.0.1')

args = parser.parse_args()

if __name__ == "__main__":
    NAMESPACE = '/data'
    webapp = AppWrapper(args, NAMESPACE)
    socket = webapp.socket
    app = webapp.app



    def _corsify_actual_response(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        print(app.static_folder)
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')


    @app.route('/history')
    def history():
        limit = int(request.args.get('limit')) or webapp.MAX_DATA
        print("LIMIT: ", limit)
        response = {'history': webapp.store.get_history(limit)}
        return _corsify_actual_response(jsonify(response))


    @app.route('/ws-test')
    def ws_test(self):
        return render_template('ws.html', sync_mode=self.socket.async_mode)


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


    @socket.on('disconnect_request', namespace=NAMESPACE)
    def disconnect_request():
        @copy_current_request_context
        def can_disconnect():
            disconnect()

        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'Disconnected!', 'count': session['receive_count']},
             callback=can_disconnect)
