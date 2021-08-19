import random
from pprint import pprint

import pkg_resources
from flask import Flask
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO

from . import routes
from .config import AppConfig
from .storage import InMemoryStore
from .zeromq import ZMQSubscriber, ZMQPublisher


class App:
    WEBAPP_DIR = 'resources/webapp'
    depth_sub = None

    def __init__(self, config: AppConfig):
        self.config = config
        self.store = InMemoryStore(config)
        webapp_folder = pkg_resources.resource_filename('tank', self.WEBAPP_DIR)
        dist_folder = 'dist'
        webapp_root = f'{webapp_folder}/{dist_folder}'
        print("webapp mounted at ", webapp_root)
        self.app = Flask(__name__, static_folder=webapp_root)
        self.app.config.from_object(config)
        self.depth_sub = ZMQSubscriber(
            "depth",
            self.store.add_measurement,
            self.config.ZMQ_PORT,
            self.config.ZMQ_RECV_TIMEOUT
        )

        if self.config.args.env == 'dev':
            from flask_cors import CORS

            CORS(self.app)
        if self.config.args.mock:
            # publish mocked depth measurement
            self.depth_mock_pub = ZMQPublisher("depth")
        else:
            self.depth_mock_pub = None

        self.scheduler = APScheduler()
        self.socket = SocketIO(self.app, async_mode=None, cors_allowed_origins='*')

    def mock_measure_depth(self, min_depth=100, max_depth=250):
        # mocked measuring
        depth = random.randint(min_depth, max_depth) / 100
        print("[MOCK MEASURING] ", depth)
        if self.depth_mock_pub is not None:
            self.depth_mock_pub.send(f'{depth}')

    def broadcast_history(self):
        self.socket.emit('history', self.store.get_history(), namespace=self.config.socketio_namespace)

    def broadcast_depth(self):
        last_measurement = self.store.get_last_measurement()
        if last_measurement is not None:
            self.socket.emit('depth', last_measurement, namespace=self.config.socketio_namespace)

    def add_jobs(self):
        self.scheduler.add_job(func=self.broadcast_depth,
                               trigger='interval',
                               seconds=self.config.BROADCASTING_INTERVAL,
                               id='broadcast_measurement',
                               name='broadcast depth measurement',
                               replace_existing=True
                               )
        if self.config.args.mock:
            self.scheduler.add_job(func=self.mock_measure_depth,
                                   args=[100, 250],
                                   trigger='interval',
                                   seconds=self.config.MEASURING_INTERVAL,
                                   id='mock_measure_depth',
                                   name='measuring depth',
                                   replace_existing=True
                                   )

    def stop(self):
        print("shutdown socket")
        # socket.stop()
        print("shutdown scheduler")
        if self.scheduler is not None and self.scheduler.running:
            self.scheduler.shutdown(wait=False)
        print("shutdown zmq")
        if self.depth_mock_pub is not None:
            print('shutdown mocked zmq pub')
            self.depth_mock_pub.close()
        if self.depth_sub is not None:
            print('shutdown zmq sub')
            self.depth_sub.stop()

    def start(self):
        # socket.run(app, host="127.0.0.1", port="8080", debug="True")
        print("Starting zmq subscribers")
        if self.depth_sub is not None:
            self.depth_sub.start()

        print("Init scheduler")
        self.scheduler.init_app(self.app)
        print("Adding jobs")
        self.add_jobs()
        print("Setup routes")
        routes.setup(self.app, self.store, self.config)
        print("___________________")
        pprint(self.app.config)
        print("___________________")
        print("Starting Scheduler")
        self.scheduler.start()
        print("Starting flask application with config")
        self.app.run(host=self.config.HOST, port=self.config.PORT)
        print("END")
