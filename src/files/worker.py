def bucket_worker(worker_id, queue, metrics, stop_event, process_fn):
    while not stop_event.is_set():
        try:
            bucket = queue.get(timeout=0.5)
        except:
            continue

        try:
            count = process_fn(bucket)
            metrics["buckets_ok"] += 1
            metrics["files_processed"] += count
        except Exception:
            metrics["buckets_failed"] += 1

        queue.task_done()
