from contextlib import AbstractAsyncContextManager
from typing import Union
from ultra_cache.storage.base import BaseStorage

_storage_instance: Union[BaseStorage, None] = None


def init_cache(storage: BaseStorage) -> None:
    global _storage_instance
    _storage_instance = storage


def get_storage() -> BaseStorage:
    if _storage_instance is None:
        raise ValueError("Cache not initialized")

    return _storage_instance


class FastCache(AbstractAsyncContextManager):
    storage: Union[BaseStorage, None] = None

    def __init__(self) -> None:
        pass
