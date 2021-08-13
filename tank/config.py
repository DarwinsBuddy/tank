import argparse

parser = argparse.ArgumentParser(description='Tank WebUI')
parser.add_argument('-e', '--env', help='Environment (dev|prod) default: dev', type=str, default='prod')
parser.add_argument('-m', '--mock', action='store_true', help='Start with mocked measurements', default=False)
parser.add_argument('-zp', '--zmq-port', type=int, nargs=1, help='Listen port for zmq subscriber', default=5555)
parser.add_argument('-za', '--zmq-addr', type=str, nargs=1, help='Listen address for zmq subscriber',
                    default='0.0.0.0')

args = parser.parse_args()
# data storage
MEASURING_INTERVAL = 5  # seconds
MAX_HISTORY_SECONDS = 3600
MAX_DATA = int(MAX_HISTORY_SECONDS / MEASURING_INTERVAL)
# socket.io communication
BROADCASTING_INTERVAL = 1  # seconds
BROADCASTING_HISTORY_INTERVAL = 5  # seconds
NAMESPACE = '/data'
ZMQ_RECV_TIMEOUT = 1000

class AppConfig:
    def __init__(self, env: str):

        if env == 'dev':
            self.CORS_HEADERS = 'Content-Type'
        if env == 'dev':
            self.ENV = 'DEV'
        else:
            self.ENV = 'PRODUCTION'
        self.SECRET = '6956d8a3-e24c-4557-bfad-9d0f578b33c9'
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
