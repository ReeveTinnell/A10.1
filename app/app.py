from flask import Flask
from prometheus_client import start_http_server, Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# Prometheus Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Request latency', ['endpoint'])
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU Usage Percentage')

@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    start_time = time.time()
    response = "Hello, Prometheus!"
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start_time)
    return response

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Simulate CPU usage (for testing)
def simulate_cpu_usage():
    while True:
        CPU_USAGE.set(random.uniform(10, 90))
        time.sleep(5)

if __name__ == '__main__':
    import threading
    threading.Thread(target=simulate_cpu_usage, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
