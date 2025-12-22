from .validation import validate_file, copy_and_verify

def process_one_bucket(bucket):
    processed = 0
    for path in bucket:
        if not validate_file(path):
            continue
        copy_and_verify(path)
        processed += 1
    return processed
