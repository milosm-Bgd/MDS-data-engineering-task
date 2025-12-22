import threading
from queue import Queue
from unittest.mock import Mock

from streaming.minibatch import minibatch_collector
from streaming.worker import worker


def test_minibatch_collector_groups_messages():
    out_queue = Queue()

    def fake_source():
        for i in range(5):
            yield f"msg-{i}"

    minibatch_collector(
        message_source=fake_source(),
        window_sec=1,
        out_queue=out_queue
    )

    batch = out_queue.get_nowait()
    assert len(batch) == 5


def test_streaming_worker_processes_batch():
    queue = Queue()
    stop_event = threading.Event()
    metrics = {"batches_ok": 0, "batches_failed": 0, "messages_processed": 0}
    #put one batch
    queue.put([1, 2, 3, 4, 5])
    #mock processing function
    mock_process_fn = Mock(return_value=5)
  

    t = threading.Thread(
        target=worker,
        args=(1, queue, metrics, stop_event, mock_process_fn),
        daemon=True
    )
    t.start()

    queue.join()
    stop_event.set()

    assert metrics["batches_ok"] == 1
    assert metrics["messages_processed"] == 5
    mock_process_fn.assert_called_once()

