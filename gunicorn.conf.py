import multiprocessing
import os

# The snowflake worker-slot field is 3 bits (see shortner/snowflake.py),
# so more than 8 concurrent workers would wrap and start colliding sooner.
MAX_WORKERS = 8

workers = min(multiprocessing.cpu_count() * 2 + 1, MAX_WORKERS)


def post_fork(server, worker):
    os.environ["GUNICORN_WORKER_SLOT"] = str(worker.age % 8)
