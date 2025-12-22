import pytest
from streaming.retry import retry_with_backoff


def test_retry_succeeds_after_failure():
    attempts = {"count": 0}

    def flaky():
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise RuntimeError("fail")
        return "ok"

    result = retry_with_backoff(flaky, max_retries=3)
    assert result == "ok"


def test_retry_fails_after_max_retries():
    def always_fail():
        raise RuntimeError("fail")

    with pytest.raises(RuntimeError):
        retry_with_backoff(always_fail, max_retries=2)
