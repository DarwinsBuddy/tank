from .config import *
from .server import start_server, stop_server
from .zeromq import close_zeromq, start_zeromq


def start_application():
    start_zeromq()
    start_server()


def stop_application():
    print("shutdown triggered")
    stop_server()
    print("shutdown zeromq subscriber")
    close_zeromq()
    print("shutdown socket.io connections")
    print("shutdown complete")
