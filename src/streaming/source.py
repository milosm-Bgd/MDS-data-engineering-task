import time
import random

def message_source(duration_sec=10):
    start = time.time()
    while time.time() - start < duration_sec:
        time.sleep(random.expovariate(1 / 6))  # ~10 msgs/min
        yield f"msg-{int(time.time())}"
