import string
import threading
import time

from django.conf import settings

EPOCH_MS = 1704067200000  # 2024-01-01T00:00:00Z

TIMESTAMP_BITS = 38
WORKER_ID_BITS = 5
SEQUENCE_BITS = 4

MAX_WORKER_ID = (1 << WORKER_ID_BITS) - 1
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

WORKER_ID_SHIFT = SEQUENCE_BITS
TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS

BASE62_ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase


def _current_millis() -> int:
    return int(time.time() * 1000)


def _to_base62(num: int) -> str:
    if num == 0:
        return BASE62_ALPHABET[0]
    digits = []
    while num > 0:
        num, rem = divmod(num, 62)
        digits.append(BASE62_ALPHABET[rem])
    return "".join(reversed(digits))


class SnowflakeGenerator:
    def __init__(self, worker_id: int):
        if worker_id < 0 or worker_id > MAX_WORKER_ID:
            raise ValueError(f"worker_id must be between 0 and {MAX_WORKER_ID}")
        self.worker_id = worker_id
        self._lock = threading.Lock()
        self._last_timestamp = -1
        self._sequence = 0

    def next_id(self) -> int:
        with self._lock:
            timestamp = _current_millis()

            if timestamp == self._last_timestamp:
                self._sequence = (self._sequence + 1) & MAX_SEQUENCE
                if self._sequence == 0:
                    while timestamp <= self._last_timestamp:
                        timestamp = _current_millis()
            else:
                self._sequence = 0

            self._last_timestamp = timestamp

            return (
                ((timestamp - EPOCH_MS) << TIMESTAMP_SHIFT)
                | (self.worker_id << WORKER_ID_SHIFT)
                | self._sequence
            )

    def next_short_code(self) -> str:
        return _to_base62(self.next_id())


_generator = SnowflakeGenerator(worker_id=settings.WORKER_ID)


def generate_short_code() -> str:
    return _generator.next_short_code()
