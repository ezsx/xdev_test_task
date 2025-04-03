from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class ICacheService(ABC):
    """
    Interface for a cache service to manage cached data.
    Defines methods for retrieving, setting, and deleting cached entries.
    """

    @abstractmethod
    async def set(self, key: str, value: str, ex: Optional[int] = None) -> None:
        """
        Stores data in the cache with an optional expiration time.

        Args:
            key (str): The unique identifier for the cached entry.
            value (Dict): The data to store in the cache.
            expire (int, optional): Time in seconds for the cache entry to expire.
                                     Defaults to None, meaning no expiration.
        """
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        """
        Retrieves a cached entry by key.

        Args:
            key (str): The unique identifier for the cached entry.

        Returns:
            Optional[Dict]: The cached data if it exists, otherwise None.
        """
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """
        Deletes a cached entry by key.

        Args:
            key (str): The unique identifier for the cached entry to delete.
        """
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """
        Check if key exists.

        Args:
            key (str): The unique identifier for the cached entry to delete.
        """
        pass
