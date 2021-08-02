import argparse
import atexit
import datetime
import os
import random
import threading

from flask_apscheduler import APScheduler
from flask import Flask, render_template, copy_current_request_context, session, send_from_directory, make_response, \
    jsonify, request
from flask_socketio import SocketIO, disconnect, emit

parser = argparse.ArgumentParser(description='Tank WebUI')
parser.add_argument('-e', '--env', nargs=1, help='Environment (dev|prod) default: dev', type=str, default='dev')

args = parser.parse_args()
dev = args.env == 'dev'
app = Flask(__name__, static_folder='../webapp/build')

# my data
MEASURING_INTERVAL = 5  # seconds
MAX_HISTORY_SECONDS = 3600
MAX_DATA = int(MAX_HISTORY_SECONDS / MEASURING_INTERVAL)
BROADCASTING_INTERVAL = 1  # seconds
BROADCASTING_HISTORY_INTERVAL = 5  # seconds
data_lock = threading.Lock()
HISTORY = 'history'
data = {
    HISTORY: []
}

if dev:
    from flask_cors import CORS

    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    socket = SocketIO(app, async_mode=None, cors_allowed_origins='*')
else:
    socket = SocketIO(app, async_mode=None, cors_allowed_origins='*')

app.config['SECRET_KEY'] = '6956d8a3-e24c-4557-bfad-9d0f578b33c9'

NAMESPACE = '/data'


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
    limit = int(request.args.get('limit')) or MAX_DATA
    print("LIMIT: ", limit)
    response = {'history': data[HISTORY][:limit]}
    return _corsify_actual_response(jsonify(response))


@app.route('/ws-test')
def ws_test():
    return render_template('ws.html', sync_mode=socket.async_mode)


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


def measure_depth(min_depth=100, max_depth=250):
    # mocked measuring
    depth = random.randint(min_depth, max_depth) / 100
    date = datetime.datetime.utcnow().isoformat()
    print("[MEASURING] ", depth, "m at ", date)
    with data_lock:
        data[HISTORY].append({
            'date': date,
            'depth': depth
        })
        if len(data[HISTORY]) >= MAX_DATA:
            overlap = (len(data[HISTORY]) - MAX_DATA)
            data[HISTORY] = data[HISTORY][overlap:]


def broadcast_depth():
    with data_lock:
        depth = data[HISTORY][-1] if len(data[HISTORY]) > 0 else -1
    socket.emit('depth', depth, namespace=NAMESPACE)


def broadcast_history():
    with data_lock:
        socket.emit('history', data[HISTORY], namespace=NAMESPACE)


if __name__ == "__main__":
    scheduler = APScheduler()
    scheduler.api_enabled = True
    scheduler.start()
    scheduler.add_job(
        func=measure_depth,
        args=[100, 250],
        trigger='interval',
        seconds=MEASURING_INTERVAL,
        id='measure',
        name='measuring depth',
        replace_existing=True
    )
    scheduler.add_job(
        func=broadcast_depth,
        trigger='interval',
        seconds=BROADCASTING_INTERVAL,
        id='broadcast_measurement',
        name='broadcast depth measurement',
        replace_existing=True
    )
    # scheduler.add_job(
    #    func=broadcast_history,
    #    trigger='interval',
    #    seconds=BROADCASTING_HISTORY_INTERVAL,
    #    id='broadcast_history',
    #    name='broadcast depth history',
    #    replace_existing=True
    # )
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    app.run(host='127.0.0.1', port=8080)
    socket.run(app, host="127.0.0.1", port="8080", debug="True")
