from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from celery_decipher.settings import settings

tracer_provider: TracerProvider | None = None


def initialize_tracer(service_name: str) -> TracerProvider:
    global tracer_provider

    resource = Resource.create({"service.name": service_name})
    otlp_exporter = OTLPSpanExporter(settings.otel_exporter_otlp_endpoint)
    tracer_provider = TracerProvider(resource=resource)
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)
    return tracer_provider


def get_tracer() -> TracerProvider:
    """
    Get the global tracer provider.
    """
    if tracer_provider is None:
        raise ValueError(
            "Tracer provider is not initialized. Call initialize_tracer first."
        )
    return tracer_provider
