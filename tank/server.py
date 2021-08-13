import random

import pkg_resources
from flask import Flask
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO

from . import routes
from .config import args, AppConfig, BROADCASTING_INTERVAL, MEASURING_INTERVAL, NAMESPACE
from .storage import store
from .zeromq import ZMQSubscriber, ZMQPublisher


class App:
    WEBAPP_DIR = 'resources/webapp'
    depth_sub = None

    def __init__(self):
        # self.app = Flask(__name__, static_folder='../webapp/dist', )
        webapp_folder = pkg_resources.resource_filename('tank', self.WEBAPP_DIR)
        dist_folder = '' if args.env == 'dev' else 'dist'
        webapp_root = f'{webapp_folder}/{dist_folder}'
        print("webapp mounted at ", webapp_root)
        self.app = Flask(__name__, static_folder=webapp_root)
        self.app.config.from_object(AppConfig(args.env))
        self.depth_sub = ZMQSubscriber("depth", store.add_measurement)

        if args.env == 'dev':
            from flask_cors import CORS

            CORS(self.app)
        if args.mock:
            # publish mocked depth measurement
            self.depth_mock_pub = ZMQPublisher("depth")
        else:
            self.depth_mock_pub = None

        # tscheduler = ThreadedScheduler(app)
        self.scheduler = APScheduler()
        self.socket = SocketIO(self.app, async_mode=None, cors_allowed_origins='*')

    def mock_measure_depth(self, min_depth=100, max_depth=250):
        # mocked measuring
        depth = random.randint(min_depth, max_depth) / 100
        print("[MEASURING] ", depth)
        if self.depth_mock_pub is not None:
            self.depth_mock_pub.send(f'{depth}')

    def broadcast_history(self):
        self.socket.emit('history', store.get_history(), namespace=NAMESPACE)

    def broadcast_depth(self):
        last_measurement = store.get_last_measurement()
        if last_measurement != -1:
            self.socket.emit('depth', last_measurement, namespace=NAMESPACE)

    def add_jobs(self):
        self.scheduler.add_job(func=self.broadcast_depth,
                               trigger='interval',
                               seconds=BROADCASTING_INTERVAL,
                               id='broadcast_measurement',
                               name='broadcast depth measurement',
                               replace_existing=True
                               )
        if args.mock or args.env == 'dev':
            self.scheduler.add_job(func=self.mock_measure_depth,
                                   args=[100, 250],
                                   trigger='interval',
                                   seconds=MEASURING_INTERVAL,
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
            self.depth_sub.close()

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
        routes.setup(self.app)
        print("___________________")
        print(self.app.config)
        print("___________________")
        print("Starting Scheduler")
        self.scheduler.start()
        print("Starting flask application with config")
        self.app.run(host='127.0.0.1', port=8080)
        print("END")
