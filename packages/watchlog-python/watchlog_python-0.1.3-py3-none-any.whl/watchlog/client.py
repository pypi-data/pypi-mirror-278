import requests
import threading

# API endpoint
URL = "http://localhost:3774"

class Watchlog:
    def send_metric(self, method, metric, value=1):
        def make_request():
            try:
                if isinstance(value, (int, float, complex)):
                    data = {'method': method, 'metric': metric, 'value': value}
                    requests.get(url=URL, params=data)
            except Exception as e:
                print(f"Error in send_metric: {e}")

        thread = threading.Thread(target=make_request)
        thread.start()

    def increment(self, metric, value=1):
        try:
            if isinstance(value, (int, float, complex)):
                self.send_metric('increment', metric, value)
        except Exception as e:
            print(f"Error in increment: {e}")

    def decrement(self, metric, value=1):
        try:
            if isinstance(value, (int, float, complex)):
                self.send_metric('decrement', metric, value)
        except Exception as e:
            print(f"Error in decrement: {e}")

    def gauge(self, metric, value):
        try:
            if isinstance(value, (int, float, complex)):
                self.send_metric('gauge', metric, value)
        except Exception as e:
            print(f"Error in gauge: {e}")

    def percentage(self, metric, value):
        try:
            if isinstance(value, (int, float, complex)) and 0 <= value <= 100:
                self.send_metric('percentage', metric, value)
        except Exception as e:
            print(f"Error in percentage: {e}")

    def systembyte(self, metric, value):
        try:
            self.send_metric('systembyte', metric, value)
        except Exception as e:
            print(f"Error in systembyte: {e}")