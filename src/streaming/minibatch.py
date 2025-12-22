import time

def minibatch_collector(message_source, window_sec, out_queue):
    batch = []
    start_time = None

    for msg in message_source:
        if start_time is None:
            start_time = time.time()

        batch.append(msg)

        if time.time() - start_time >= window_sec:
            out_queue.put(batch)
            batch = []
            start_time = None

    if batch:
        out_queue.put(batch)
