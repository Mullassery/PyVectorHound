"""Retry-with-exponential-backoff helper for calls to caller-supplied
functions that hit external services (LLM judges, embedding functions).

PyVectorHound doesn't bundle an HTTP/LLM client of its own, so it can't
retry at the transport layer -- this wraps whatever callable the caller
passed in (embed_fn, llm_judge_fn) and retries the call itself on
exception, which is where rate limits and transient network errors
actually surface.
"""

import random
import time
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def call_with_backoff(
    fn: Callable[..., T],
    *args: Any,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    **kwargs: Any,
) -> T:
    """Call `fn(*args, **kwargs)`, retrying on exception with exponential
    backoff and jitter.

    Args:
        fn: Callable to invoke (e.g. an llm_judge_fn or embed_fn).
        max_retries: Number of retry attempts after the first failure.
        base_delay: Delay before the first retry, in seconds. Doubles each
            subsequent attempt (1x, 2x, 4x, ...), capped at max_delay.
        max_delay: Upper bound on any single delay.

    Raises:
        The last exception raised by `fn`, if every attempt fails.
    """
    last_exc: Exception = RuntimeError("call_with_backoff: fn was never called")
    for attempt in range(max_retries + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001 - caller's fn, any exception is a valid retry signal
            last_exc = exc
            if attempt == max_retries:
                break
            delay = min(base_delay * (2**attempt), max_delay)
            delay += random.uniform(0, delay * 0.1)  # jitter to avoid thundering herd
            time.sleep(delay)
    raise last_exc
