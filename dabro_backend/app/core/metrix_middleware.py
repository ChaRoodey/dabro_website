from datetime import datetime, timezone, timedelta

from fastapi import Request, Response
from prometheus_client import Counter, Gauge

from app.core.logging import get_logger

logger = get_logger(__name__)

TOTAL_EXCEPTIONS_COUNTER = Counter(
    "total_exceptions_counter",
    "Total number of unhandled exceptions in the application",
)

UNIQUE_VISITORS_CURRENT_DAY = Gauge(
    "unique_visitors_current_day",
    "Unique visitors for current stats day",
    ["scope"],
)

TRACKED_PATHS = {
    "/products/all": "products",
    "/staff/all": "staff",
}

all_visitors: set[str] = set()
shop_visitors: set[str] = set()
index_visitors: set[str] = set()


def _get_client_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    if request.client:
        return request.client.host

    return "unknown"


def get_stats_day(now: datetime) -> str:
    shifted = now - timedelta(hours=5)
    return shifted.date().isoformat()


current_day = get_stats_day(datetime.now(timezone.utc))


def flush_daily_stats(stats_day: str) -> None:
    logger.info(
        "daily_unique_visitors stats_day=%s all=%s main=%s shop=%s",
        stats_day,
        len(all_visitors),
        len(index_visitors),
        len(shop_visitors),
    )


def reset_daily_sets() -> None:
    all_visitors.clear()
    shop_visitors.clear()
    index_visitors.clear()

    UNIQUE_VISITORS_CURRENT_DAY.labels(scope="all").set(0)
    UNIQUE_VISITORS_CURRENT_DAY.labels(scope="main").set(0)
    UNIQUE_VISITORS_CURRENT_DAY.labels(scope="shop").set(0)


def update_unique_visitor_metrics() -> None:
    UNIQUE_VISITORS_CURRENT_DAY.labels(scope="all").set(len(all_visitors))
    UNIQUE_VISITORS_CURRENT_DAY.labels(scope="main").set(len(shop_visitors))
    UNIQUE_VISITORS_CURRENT_DAY.labels(scope="shop").set(len(index_visitors))


async def metrics_and_visitors_middleware(request: Request, call_next) -> Response:
    global current_day

    try:
        response = await call_next(request)
    except Exception:
        TOTAL_EXCEPTIONS_COUNTER.inc()
        logger.exception("Unhandled exception path=%s method=%s", request.url.path, request.method)
        raise

    now = datetime.now(timezone.utc)
    new_day = get_stats_day(now)

    if new_day != current_day:
        flush_daily_stats(current_day)
        reset_daily_sets()
        current_day = new_day

    path = request.url.path
    if path in TRACKED_PATHS:
        ip = _get_client_ip(request)

        all_visitors.add(ip)

        scope = TRACKED_PATHS[path]
        if scope == 'products':
            shop_visitors.add(ip)
        elif scope == 'staff':
            index_visitors.add(ip)

    update_unique_visitor_metrics()

    return response
