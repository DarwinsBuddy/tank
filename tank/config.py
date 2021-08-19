import argparse
import configparser

import pkg_resources


class AppConfig:

    @staticmethod
    def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Tank WebUI')
        parser.add_argument('-e', '--env', help='Environment (dev|prod) default: dev', type=str, default='prod')
        parser.add_argument('-m', '--mock', action='store_true', help='Start with mocked measurements', default=False)
        parser.add_argument('-c', '--config', type=str,
                            help='Path to config file',
                            default=pkg_resources.resource_filename('tank', 'resources/tank.conf')
                            )
        return parser.parse_args()

    @staticmethod
    def read_config(path):
        config = configparser.ConfigParser()
        with open(path, 'r') as configfile:
            config.read_file(configfile)
        return config

    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.config = self.read_config(args.config)
        # flask
        self.SECRET = self.config['Flask']['secret'] or None
        self.HOST = self.config['Flask']['host'] or '0.0.0.0'
        self.PORT = int(self.config['Flask']['port']) or 8080
        # zmq
        self.ZMQ_PORT = self.config['ZMQ']['port'] or 5555
        # socketio
        self.BROADCASTING_INTERVAL = int(self.config['SocketIO']['broadcasting_interval']) or 5
        self.socketio_namespace = self.config['SocketIO']['namespace'] or '/data'
        # storage
        self.MAX_HISTORY_DATA = int(self.config['Storage']['max_history_data']) or 720
        # custom
        self.ZMQ_RECV_TIMEOUT = 1000
        self.MEASURING_INTERVAL = 5

        if self.args.env == 'dev':
            self.CORS_HEADERS = 'Content-Type'
        if self.args.env == 'dev':
            self.ENV = 'DEV'
        else:
            self.ENV = 'PRODUCTION'
        # self.SCHEDULER_JOBSTORES = {
        #    'mongo': {
        #        'type': 'mongodb'
        #    },
        #    'default': {
        #        'type': 'sqlalchemy',
        #        'url': 'sqlite:///jobs.sqlite'
        #    }
        # }
        # Set the actuator, and the number of threads
        self.SCHEDULER_EXECUTORS = {
            'default': {
                'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
                'max_workers': 20
            },
            # 'processpool': {
            #    'class': 'apscheduler.executors.pool:ProcessPoolExecutor',
            #    'max_workers': 5
            # }
        }
        self.SCHEDULER_JOB_DEFAULTS = {
            'coalesce': False,  # Close the new job by default at #
            # 3 set maximum number of instances running simultaneously scheduler particular job
            'max_instances': 3
        }
        self.SCHEDULER_PAUSED = True
