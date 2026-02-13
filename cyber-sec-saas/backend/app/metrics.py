from prometheus_client import Counter, Gauge, Histogram

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "path"],
)

ALERT_COUNT = Gauge(
    "active_alerts",
    "Active alerts count",
)

RISK_SCORE = Gauge(
    "risk_score",
    "Latest risk score",
)

SYSTEM_CPU = Gauge(
    "system_cpu_percent",
    "Average CPU percent (last hour)",
)

SYSTEM_MEMORY = Gauge(
    "system_memory_percent",
    "Average memory percent (last hour)",
)
