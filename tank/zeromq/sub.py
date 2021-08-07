import threading

import zmq


class ZMQSubscriber(threading.Thread):

    def __init__(self, topic, callback=(lambda x: print(x)), port=5555):
        threading.Thread.__init__(self)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.bind(f"tcp://*:{port}")
        self.socket.setsockopt(zmq.SUBSCRIBE, bytes(topic, encoding='utf-8'))
        self.running = True
        self.callback = callback

    def close(self):
        self.socket.close()
        self.running = False

    def run(self):
        while self.running:
            #  Wait for next request from client
            message = self.socket.recv()
            print("Received request: %s" % message)
            msg = message.decode('utf-8')
            self.callback(' '.join(msg.split(' ')[1:]))