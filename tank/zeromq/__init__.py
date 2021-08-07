# zmq
# subscribe to all relevant topics
import random

from .. import config
from .pub import ZMQPublisher
from .sub import ZMQSubscriber
from ..storage import store

zmq_sub = ZMQSubscriber("depth", store.add_measurement)

if config.args.mock:
    # publish mocked depth measurement
    zmq_pub = ZMQPublisher("depth")


    def mock_measure_depth(min_depth=100, max_depth=250):
        # mocked measuring
        depth = random.randint(min_depth, max_depth) / 100
        print("[MEASURING] ", depth)
        zmq_pub.send(f'{depth}')


def start_zeromq():
    zmq_sub.start()


def close_zeromq():
    if zmq_pub is not None:
        print('>>> Closing mock publisher')
        zmq_pub.close()
    zmq_sub.close()
