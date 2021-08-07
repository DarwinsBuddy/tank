from flask import Flask
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO

from . import routes
from .storage import store
from .config import args, AppConfig, BROADCASTING_INTERVAL, MEASURING_INTERVAL, NAMESPACE
from .zeromq import mock_measure_depth

app = Flask(__name__, static_folder='../webapp/dist', )
app.config.from_object(AppConfig(args.env))

if args.env == 'dev':
    from flask_cors import CORS

    CORS(app)

scheduler = APScheduler()
socket = SocketIO(app, async_mode=None, cors_allowed_origins='*')


def broadcast_history():
    socket.emit('history', store.get_history(), namespace=NAMESPACE)


def broadcast_depth():
    socket.emit('depth', store.get_last_measurement(), namespace=NAMESPACE)


def init_scheduler():
    scheduler.init_app(app)
    scheduler.add_job(func=broadcast_depth,
                      trigger='interval',
                      seconds=BROADCASTING_INTERVAL,
                      id='broadcast_measurement',
                      name='broadcast depth measurement')
    if args.env == 'dev':
        scheduler.add_job(func=mock_measure_depth,
                          args=[100, 250],
                          trigger='interval',
                          seconds=MEASURING_INTERVAL,
                          id='mock_measure_depth',
                          name='measuring depth'
                          )


def stop_server():
    print("shutdown socket")
    socket.stop()
    print("shutdown scheduler")
    scheduler.remove_all_jobs('default')
    scheduler.shutdown(wait=False)


def start_server():
    # socket.run(app, host="127.0.0.1", port="8080", debug="True")
    init_scheduler()

    routes.setup(app)
    scheduler.start()
    print("Starting flask application with config")
    print(app.config)
    app.run(host='127.0.0.1', port=8080)
