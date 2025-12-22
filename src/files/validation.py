import os
import hashlib
import shutil

def validate_file(path):
    return os.path.exists(path) and os.path.getsize(path) > 0


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def copy_and_verify(path):
    if not validate_file(path):
        raise ValueError("Invalid file")

    before = sha256_file(path)
    out_path = "data/processed/" + os.path.basename(path)
    shutil.copyfile(path, out_path)
    after = sha256_file(out_path)

    if before != after:
        raise RuntimeError("Checksum mismatch")

    return out_path
