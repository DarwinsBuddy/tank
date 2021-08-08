import threading

import zmq

from ..config import ZMQ_RECV_TIMEOUT


class ZMQSubscriber(threading.Thread):

    def __init__(self, topic, callback=(lambda x: print(x)), port=5555):
        threading.Thread.__init__(self)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.bind(f"tcp://*:{port}")
        self.socket.setsockopt(zmq.SUBSCRIBE, bytes(topic, encoding='utf-8'))
        self.socket.setsockopt(zmq.RCVTIMEO, ZMQ_RECV_TIMEOUT)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.running = True
        self.callback = callback

    def close(self):
        self.running = False
        self.socket.close()

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
                # print("Nothing recieved:", e)
                pass
