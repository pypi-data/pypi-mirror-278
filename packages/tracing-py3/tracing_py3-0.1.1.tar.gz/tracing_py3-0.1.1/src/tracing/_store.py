# -- Future Imports --
from __future__ import annotations

# -- STL Imports --
from typing import Generic, TypeVar
from dataclasses import dataclass

T = TypeVar("T")
"""Template type for the stored value."""


@dataclass
class Store(Generic[T]):
    """
    Store is a generic dataclass that holds a single value of a given type.

    Args:
        value (T): The value to store.

    Example::

        >>> store = Store(42)
        >>> store.value
        42
    """

    value: T | None = None

    def set(self, value: T | None) -> Store[T]:
        """
        Sets the stored value.

        Args:
            value (T): The value to store.

        Example::

            >>> store = Store(42)
            >>> store.set(43)
            >>> store.get()
            43
        """
        self.value = value
        return self

    def get(self) -> T | None:
        """
        Returns the stored value.

        Returns:
            T: The stored value.

        Example::

            >>> store = Store(42)
            >>> store.get()
            42
        """
        return self.value
