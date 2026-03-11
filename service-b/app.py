from flask import Flask
from prometheus_client import Counter, generate_latest

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

# --------- JAEGER CONFIG ---------
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "service-a"})
    )
)

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

FlaskInstrumentor().instrument_app(app)
# ---------------------------------

REQUEST_COUNT = Counter("requests_total", "Total Requests")

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return "Hello from Service b "

@app.route("/metrics")
def metrics():
    return generate_latest()

# IMPORTANT: start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
