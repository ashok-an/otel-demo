
import os
import requests
import subprocess
from fastapi import FastAPI, Request
from opentelemetry import trace
#from opentelemetry.exporter.console import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

#from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

# configure JaegerSpanExporter
jaeger_exporter = JaegerExporter(
    agent_host_name=os.environ.get("OTEL_EXPORTER_JAEGER_AGENT_HOST", "localhost"),
    agent_port=int(os.environ.get("OTEL_EXPORTER_JAEGER_AGENT_PORT", 6831)),
)

# configure ConsoleSpanExporter
#console_exporter = ConsoleSpanExporter()

# create a TracerProvider with the Jaeger and Console exporters and a BatchExportSpanProcessor
trace_provider = TracerProvider()
trace_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
#trace_provider.add_span_processor(BatchExportSpanProcessor(console_exporter))

# register the TracerProvider as the global TracerProvider
trace.set_tracer_provider(trace_provider)

# get a Tracer object
tracer = trace.get_tracer(__name__)

# initialize FastAPI app
app = FastAPI()
FastAPIInstrumentor().instrument_app(app)


@app.get("/calculate")
def calculate(a: int, b: int, c: int, r: Request):
    # Extract the parent span context from the request headers
    trace_header = r.headers.get("traceparent")
    parent_span_context = None
    if trace_header is not None:
        parent_span_context = trace.propagation.extract(dict.__getitem__, trace_header)

    # Start a new span
    with trace_provider.get_tracer(__name__).start_as_current_span("calculate", context=parent_span_context):
        # Call the add.pl script
        process = subprocess.Popen(["perl", "../perl-cli/arithmetic.pl", str(a), str(b), str(c)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Extract the result from the output
        output, error = process.communicate()
        result = str(output.decode("utf-8").strip())

        # Set the span status based on the result
        if result == "":
            status_code = 2 #trace.Status.ERROR
        else:
            status_code = 1 #trace.Status.OK

        # Log the span
        span = trace.get_current_span()
        span.set_status(status_code)
        print(f"SPAN {span.get_span_context().span_id} calculate {result} {status_code}")

        # Return the result
        return {"result": result}
