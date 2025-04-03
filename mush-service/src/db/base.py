import logging
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class BaseService(ABC, Generic[T]):
    connection: Optional[T] = None

    @abstractmethod
    async def init(self) -> None:
        """
        Initialize the service connection. This method must be implemented by subclasses.
        """
        pass

    async def close(self) -> None:
        """
        Close the service connection.
        """
        if self.connection:
            await self.connection.close()
            self.connection = None
            logging.info(f"{self.__class__.__name__} connection closed.")

    async def get_connection(self) -> T:
        """
        Get the current service connection instance. If the connection has not been initialized, it raises an error.

        Returns:
            T: The connection instance currently in use.

        Raises:
            RuntimeError: If the connection is not initialized.
        """
        if self.connection is None:
            raise RuntimeError(
                f"{self.__class__.__name__} connection has not been initialized. Call `init()` first."
            )
        return self.connection
