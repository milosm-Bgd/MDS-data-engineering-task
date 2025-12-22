from queue import Queue
import threading

from common.config import MINIBATCH_WINDOW_SECONDS
from streaming.source import message_source
from streaming.minibatch import minibatch_collector
from streaming.retry import retry_with_backoff
from streaming.worker import worker
from streaming.processing import process_batch


from files.generator import create_fake_files
from files.bucketing import bfd_buckets
from files.processor import process_one_bucket
from files.worker import bucket_worker
from common.metrics import init_file_metrics

# I pipeline:  message pipeline
def run_message_pipeline():
    from queue import Queue
    import threading
    import time

    work_queue = Queue(maxsize=50)

    # startovanje worker-a
    metrics = {
        "batches_ok": 0,
        "batches_failed": 0,
        "messages_processed": 0,
    }
    stop_event = threading.Event()

    for i in range(10):
        threading.Thread(
            target=worker,
            args=(i + 1, work_queue, metrics, stop_event, process_batch),
            daemon=True,
        ).start()

    # proizvodnja mini-batcheva (vremenski ograničena simulacija)
    minibatch_collector(
        message_source(duration_sec=300),
        window_sec=5,
        out_queue=work_queue,
    )

    # čekamo da se obrada svih batche-va završi
    work_queue.join()

    # zaustavljanje worker-a
    stop_event.set()
    time.sleep(1)
    print("STREAMING METRICS:", metrics)

# II pipeline: nightly file pipeline:
def run_file_pipeline():
    files = create_fake_files(100)
    buckets = bfd_buckets(files, 10 * 1024 * 1024)

    queue = Queue(maxsize=50)
    for b in buckets:
        queue.put(b)

    metrics = init_file_metrics()
    stop_event = threading.Event()

    for i in range(10):
        threading.Thread(
            target=bucket_worker,
            args=(i + 1, queue, metrics, stop_event, process_one_bucket),
            daemon=True
        ).start()

    queue.join()
    stop_event.set()
    print("NIGHTLY FILES METRICS:", metrics)


if __name__ == "__main__":
    import argparse
    import threading

    parser = argparse.ArgumentParser(description="Data Engineering Pipelines")
    parser.add_argument(
        "--pipeline",
        choices=["files", "streaming", "all"],
        default="files",
        help="Which pipeline to run",
    )
    args = parser.parse_args()

    if args.pipeline == "files":
        run_file_pipeline()

    elif args.pipeline == "streaming":
        run_message_pipeline()

    elif args.pipeline == "all":
        t = threading.Thread(target=run_message_pipeline)
        t.start()

        run_file_pipeline()
        t.join()

