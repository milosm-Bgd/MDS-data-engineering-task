import os
import random

def create_fake_files(n=10, min_kb=50, max_kb=500):
    os.makedirs("data/incoming_files", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    paths = []
    for i in range(n):
        size_kb = random.randint(min_kb, max_kb)
        path = f"data/incoming_files/file_{i}.bin"
        with open(path, "wb") as f:
            f.write(os.urandom(size_kb * 1024))
        paths.append(path)

    return paths
