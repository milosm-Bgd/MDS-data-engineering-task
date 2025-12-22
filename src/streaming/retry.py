import time

def retry_with_backoff(work_fn, max_retries=3, base_delay=0.5):
    attempt = 0
    while True:
        try:
            return work_fn()
        except Exception:
            if attempt >= max_retries:
                raise
            time.sleep(base_delay * (2 ** attempt))
            attempt += 1
