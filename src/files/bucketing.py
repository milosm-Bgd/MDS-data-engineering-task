from .validation import os

def file_size_bytes(path):
    return os.path.getsize(path)


def first_fit_buckets(paths, target_bytes):
    buckets = []
    for path in paths:
        placed = False
        for bucket in buckets:
            if sum(file_size_bytes(p) for p in bucket) + file_size_bytes(path) <= target_bytes:
                bucket.append(path)
                placed = True
                break
        if not placed:
            buckets.append([path])
    return buckets


def ffd_buckets(paths, target_bytes):
    return first_fit_buckets(sorted(paths, key=file_size_bytes, reverse=True), target_bytes)


def bfd_buckets(paths, target_bytes):
    sorted_paths = sorted(paths, key=file_size_bytes, reverse=True)
    buckets = []

    for path in sorted_paths:
        size_p = file_size_bytes(path)
        best_idx, best_remaining = None, None

        for i, bucket in enumerate(buckets):
            current = sum(file_size_bytes(p) for p in bucket)
            if current + size_p <= target_bytes:
                remaining = target_bytes - (current + size_p)
                if best_remaining is None or remaining < best_remaining:
                    best_remaining = remaining
                    best_idx = i

        if best_idx is None:
            buckets.append([path])
        else:
            buckets[best_idx].append(path)

    return buckets
