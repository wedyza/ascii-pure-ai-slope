import asyncio
import time
from typing import Any
from uuid import UUID, uuid4


class InMemoryStorage:
    def __init__(self, ttl: int = 300) -> None:
        self._store: dict[UUID, dict[str, Any]] = {}
        self._timestamps: dict[UUID, float] = {}
        self._ttl = ttl
        self._cleanup_task: asyncio.Task[None] | None = None

    def _start_cleanup(self) -> None:
        if self._cleanup_task is None or self._cleanup_task.done():
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def _cleanup_loop(self) -> None:
        while True:
            await asyncio.sleep(60)
            self._evict_expired()

    def _evict_expired(self) -> None:
        now = time.time()
        expired = [
            key
            for key, ts in self._timestamps.items()
            if now - ts > self._ttl
        ]
        for key in expired:
            self._store.pop(key, None)
            self._timestamps.pop(key, None)

    def create(self, data: dict[str, Any]) -> UUID:
        self._start_cleanup()
        entry_id = uuid4()
        self._store[entry_id] = data
        self._timestamps[entry_id] = time.time()
        return entry_id

    def get(self, entry_id: UUID) -> dict[str, Any] | None:
        return self._store.get(entry_id)

    def update(self, entry_id: UUID, data: dict[str, Any]) -> None:
        if entry_id in self._store:
            self._store[entry_id].update(data)
            self._timestamps[entry_id] = time.time()

    def delete(self, entry_id: UUID) -> bool:
        existed = entry_id in self._store
        self._store.pop(entry_id, None)
        self._timestamps.pop(entry_id, None)
        return existed

    def size(self) -> int:
        return len(self._store)


storage = InMemoryStorage()
