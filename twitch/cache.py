from datetime import timedelta, datetime
from typing import Dict


class Cache:
    EXPIRATION_FIELD: str = "CACHE_EXPIRATION"

    def __init__(self, duration: timedelta = None):
        self._store: Dict[str, dict] = {}
        self._duration: timedelta = duration or timedelta(minutes=30)

    def get(self, key: str) -> dict:
        return self._store[key] if self.has(key) and not self.expired(key) else None

    def set(self, key: str, value: dict, duration: timedelta = None) -> datetime:
        expiration: datetime = datetime.now() + duration or self._duration
        self._store[key] = {**value, **{f'{Cache.EXPIRATION_FIELD}': expiration}}
        return expiration

    def has(self, key: str) -> bool:
        return key in self._store

    def expired(self, key: str) -> bool:
        return self.has(key) and self._store[key][Cache.EXPIRATION_FIELD] > datetime.now()

    def flush(self) -> None:
        self._store = {}

    def remove(self, key) -> None:
        if self.has(key):
            del self._store[key]

    def clean(self) -> None:
        [self.remove(key) for key in list(self._store.keys()) if self.expired(key)]
