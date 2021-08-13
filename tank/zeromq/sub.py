import threading
import time

import zmq

from ..config import ZMQ_RECV_TIMEOUT


class ZMQSubscriber(threading.Thread):

    STOP_TIMEOUT = 5

    def __init__(self, topic, callback=(lambda x: print(x)), port=5555):
        threading.Thread.__init__(self)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.bind(f"tcp://*:{port}")
        self.socket.setsockopt(zmq.SUBSCRIBE, bytes(topic, encoding='utf-8'))
        self.socket.setsockopt(zmq.RCVTIMEO, ZMQ_RECV_TIMEOUT)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.running = True
        self.stopped = False
        self.callback = callback

    def stop(self):
        print("running = False")
        self.running = False
        self.wait_for_stop(self.STOP_TIMEOUT)

    def wait_for_stop(self, timeout=1):
        start = time.time()
        print("Waiting for zmq subscriber shutdown")
        while not self.stopped and time.time()-start < timeout:
            time.sleep(0.1)
        print("Subscriber stopped")

    def run(self):
        while self.running:
            #  Wait for next request from client
            # print("Waiting for request...")
            try:
                message = self.socket.recv()
                print("Received request: %s" % message)
                msg = message.decode('utf-8')
                self.callback(' '.join(msg.split(' ')[1:]))
            except zmq.error.Again as e:
                # print("Nothing received:", e)
                pass
        self.stopped = True
        self.socket.close(0)
