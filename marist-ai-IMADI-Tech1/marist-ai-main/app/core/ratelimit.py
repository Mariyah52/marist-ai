import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request

from app.core.config import settings

_hits: dict[str, deque] = defaultdict(deque)


def client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def check_rate_limit(request: Request) -> None:
    """Simple per-visitor limit so a public chat box can't burn through API credit."""
    key = client_ip(request)
    now = time.monotonic()
    window = settings.chat_rate_window_seconds
    hits = _hits[key]
    while hits and now - hits[0] > window:
        hits.popleft()
    if len(hits) >= settings.chat_rate_limit:
        raise HTTPException(
            status_code=429,
            detail="You've sent a lot of messages. Please wait a few minutes and try again.",
        )
    hits.append(now)
