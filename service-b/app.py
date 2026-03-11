from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter('service_b_requests_total','Total requests')

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return {"service":"B"}

@app.route("/metrics")
def metrics():
    return generate_latest(),200,{'Content-Type':CONTENT_TYPE_LATEST}

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
