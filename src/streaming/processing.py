import random
import time

def process_batch(batch):
    time.sleep(0.2)

    if random.random() < 0.2:
        raise RuntimeError("Random failure happened")

    return len(batch)