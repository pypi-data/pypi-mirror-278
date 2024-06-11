from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from latch_o11y.o11y import setup as setup_o11y

setup_o11y()
AioHttpClientInstrumentor().instrument()

if __name__ == "__main__":
    from .app import main

    main()
