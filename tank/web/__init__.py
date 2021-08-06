import atexit
import random

from flask import Flask
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO


from ..storage.memory import InMemoryStore
from ..zeromq import ZMQSubscriber, ZMQPublisher


class AppWrapper:
    def __init__(self, args, namespace):
        self.args = args
        self.dev = args.env == 'dev'

        self.namespace = namespace

        # data storage
        self.MEASURING_INTERVAL = 5  # seconds
        self.MAX_HISTORY_SECONDS = 3600
        self.MAX_DATA = int(self.MAX_HISTORY_SECONDS / self.MEASURING_INTERVAL)
        self.store = InMemoryStore(self.MAX_DATA)

        # socket.io communication
        self.BROADCASTING_INTERVAL = 1  # seconds
        self.BROADCASTING_HISTORY_INTERVAL = 5  # seconds

        # scheduler
        self.scheduler = APScheduler()

        # flask
        self.app = Flask(__name__, static_folder='../webapp/dist')

        # zmq
        self.zmq_sub = ZMQSubscriber("depth", self.store.add_measurement)

        if args.mock:
            self.zmq_pub = ZMQPublisher("depth")
        if self.dev:
            from flask_cors import CORS

            CORS(self.app)
            self.app.config['CORS_HEADERS'] = 'Content-Type'
            self.socket = SocketIO(self.app, async_mode=None, cors_allowed_origins='*')
        else:
            self.socket = SocketIO(self.app, async_mode=None, cors_allowed_origins='*')

        self.app.config['SECRET_KEY'] = '6956d8a3-e24c-4557-bfad-9d0f578b33c9'

        self.scheduler.api_enabled = True
        self.scheduler.start()
        if self.args.mock:
            self.scheduler.add_job(
                func=self.mock_measure_depth,
                args=[100, 250],
                trigger='interval',
                seconds=self.MEASURING_INTERVAL,
                id='measure',
                name='measuring depth',
                replace_existing=True
            )
        self.scheduler.add_job(
            func=self.broadcast_depth,
            trigger='interval',
            seconds=self.BROADCASTING_INTERVAL,
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

        # start listening on zeromq port
        self.zmq_sub.start()

        # Shut down the scheduler when exiting the app
        atexit.register(self.stop_application)

        self.app.run(host='127.0.0.1', port=8080)
        self.socket.run(self.app, host="127.0.0.1", port="8080", debug="True")

    def mock_measure_depth(self, min_depth=100, max_depth=250):
        # mocked measuring
        depth = random.randint(min_depth, max_depth) / 100
        print("[MEASURING] ", depth)
        self.zmq_pub.send(bytes(f'{depth}', encoding='utf-8'))

    def broadcast_depth(self):
        self.socket.emit('depth', self.store.get_last_measurement(), namespace=self.namespace)

    def broadcast_history(self):
        self.socket.emit('history', self.store.get_history(), namespace=self.namespace)

    def stop_application(self):
        self.zmq_sub.stop()
        if self.args.mock:
            self.zmq_pub.close()
        self.scheduler.shutdown()

