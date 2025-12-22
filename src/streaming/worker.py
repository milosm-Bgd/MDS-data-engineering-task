def worker(worker_id, queue, metrics, stop_event, process_fn):
    while not stop_event.is_set():
        try:
            batch = queue.get(timeout=0.5)
        except:
            continue

        try:
            count = process_fn(batch)
            metrics["batches_ok"] += 1
            metrics["messages_processed"] += count
        except Exception:
            metrics["batches_failed"] += 1

        queue.task_done()
