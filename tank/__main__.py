import signal
import sys

from .server import App

if __name__ == "__main__":
    app = App()

    # Shut down the scheduler when exiting the app
    # atexit.register(stop_application)
    def signal_handler(sig, frame):
        print('You pressed Ctrl+C!', sig, frame)
        app.stop()
        print("Application stopped")
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)
    app.start()
