from flask import Flask, Response
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

HTTP_REQUESTS = Counter('http_requests_total', 'Total HTTP requests', ['status'])

@app.route('/')
def index():
    import random
    if random.randint(0, 10) < 2:
        HTTP_REQUESTS.labels(status='500').inc()
        return "Internal Server Error", 500
    HTTP_REQUESTS.labels(status='200').inc()
    return "Hello, World!", 200

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
