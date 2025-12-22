import threading
import time
from queue import Queue
from unittest.mock import Mock

from files.worker import bucket_worker


def test_bucket_worker_processes_all_buckets():
    queue = Queue()
    stop_event = threading.Event()

    metrics = {
        "buckets_ok": 0,
        "buckets_failed": 0,
        "files_processed": 0
    }

    queue.put(["f1", "f2"])
    queue.put(["f3"])

    mock_process_fn = Mock(side_effect=lambda b: len(b))

    t = threading.Thread(
            target=bucket_worker,
            args=(1, queue, metrics, stop_event, mock_process_fn),
            daemon=True
        )
    t.start()

    queue.join()
    stop_event.set()

    assert metrics["buckets_ok"] == 2
    assert metrics["files_processed"] == 3
    assert mock_process_fn.call_count == 2
