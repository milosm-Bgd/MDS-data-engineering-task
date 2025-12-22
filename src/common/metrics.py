def init_streaming_metrics():
    return {
        "batches_ok": 0,
        "batches_failed": 0,
        "messages_processed": 0
    }


def init_file_metrics():
    return {
        "buckets_ok": 0,
        "buckets_failed": 0,
        "files_processed": 0
    }
