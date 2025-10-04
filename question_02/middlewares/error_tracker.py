from prometheus_client import Counter
from fastapi import Request, Response

# Define a counter for HTTP errors
ERROR_COUNT = Counter(
    "http_request_errors_total",
    "Total number of error responses",
    ["method", "endpoint", "status_code"]
)

async def error_tracking_middleware(request: Request, call_next):
    response: Response = await call_next(request)
    if response.status_code >= 400:  # Track only 4xx and 5xx
        ERROR_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        ).inc()
    return response
