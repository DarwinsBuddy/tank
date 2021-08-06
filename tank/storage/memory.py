import threading
import datetime


class InMemoryStore:

    def __init__(self, max_data):
        self.data_lock = threading.Lock()
        self.HISTORY = 'history'
        self.max_data = max_data
        self.data = {
            self.HISTORY: []
        }

    def get_history(self, limit=None):
        with self.data_lock:
            if limit is None:
                return self.data[self.HISTORY]
            else:
                return self.data[self.HISTORY][:limit]

    def add_measurement(self, measurement):
        date = datetime.datetime.utcnow().isoformat()
        print("Storing measurement ", measurement, "m at ", date)
        with self.data_lock:
            self.data[self.HISTORY].append({
                'date': date,
                'depth': float(measurement)
            })
            if len(self.data[self.HISTORY]) >= self.max_data:
                overlap = (len(self.data[self.HISTORY]) - self.max_data)
                self.data[self.HISTORY] = self.data[self.HISTORY][overlap:]

    def get_last_measurement(self):
        with self.data_lock:
            return self.data[self.HISTORY][-1] if len(self.data[self.HISTORY]) > 0 else -1
