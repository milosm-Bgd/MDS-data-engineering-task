from unittest.mock import patch
from files.bucketing import first_fit_buckets, ffd_buckets, bfd_buckets


def test_first_fit_respects_bucket_size():
    fake_sizes = {
        "f1": 4,
        "f2": 3,
        "f3": 5
    }

    def fake_size(path):
        return fake_sizes[path]

    paths = list(fake_sizes.keys())

    with patch("files.bucketing.file_size_bytes", side_effect=fake_size):
        buckets = first_fit_buckets(paths, target_bytes=7)

    for bucket in buckets:
        total = sum(fake_sizes[p] for p in bucket)
        assert total <= 7


def test_bfd_and_ffd_return_buckets():
    fake_sizes = {"a": 5, "b": 4, "c": 3}

    with patch("files.bucketing.file_size_bytes", side_effect=lambda p: fake_sizes[p]):
        assert len(ffd_buckets(list(fake_sizes), 7)) > 0
        assert len(bfd_buckets(list(fake_sizes), 7)) > 0
