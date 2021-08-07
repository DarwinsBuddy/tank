import signal
import sys

from tank import start_application, stop_application


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!', sig, frame)
    stop_application()
    sys.exit(0)


if __name__ == "__main__":
    # Shut down the scheduler when exiting the app
    # atexit.register(stop_application)
    signal.signal(signal.SIGINT, signal_handler)
    start_application()
