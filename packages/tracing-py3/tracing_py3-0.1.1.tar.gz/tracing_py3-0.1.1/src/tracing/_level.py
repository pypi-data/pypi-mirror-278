# -- Future Imports -- (Use with caution, may not work as expected in all cases)
from __future__ import annotations

# -- STL Imports --
from enum import Enum

class Level(Enum):
    """
    Enumeration of logging levels. The levels are ordered by increasing severity. The levels are
    defined as follows:

    - DEBUG: Detailed information, typically of interest only when diagnosing problems.
    - INFO: Confirmation that things are working as expected.
    - WARN: An indication that something unexpected happened, or indicative of some problem in the
        near future (e.g. 'disk space low'). The software is still working as expected.
    - ERROR: Due to a more serious problem, the software has not been able to perform some function.
    - CRITICAL: A serious error, indicating that the program itself may be unable to continue
        running.

    Aliases:

    - TRACE: Alias for DEBUG.
    - FATAL: Alias for CRITICAL.
    - PANIC: Alias for CRITICAL.

    The levels can be accessed by their string value or their integer value. The levels can also be
    converted to a dictionary with the level names as keys and the level values as values.

    Example usage::

        >>> Level.DEBUG
        Level.DEBUG[10]

        >>> Level.DEBUG.name
        'DEBUG'

        >>> Level.DEBUG.value
        10

        >>> Level.DEBUG == Level.from_str("DEBUG")
        True

        >>> Level.DEBUG == Level.from_int(10)
        True
    """

    DEBUG = 10
    TRACE = DEBUG
    INFO = 20
    WARN = 30
    ERROR = 40
    CRITICAL = 50
    FATAL = CRITICAL
    PANIC = CRITICAL

    def __str__(self) -> str:
        """
        Returns the string value of the level.

        Returns:
            str: The string value of the level.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Returns the string representation of the level.

        Returns:
            str: The string representation of the level.
        """
        return f"{self.name}[{self.value}]"

    @staticmethod
    def from_str(level: str) -> Level:
        """
        Returns the level corresponding to the specified string value.

        Args:
            level (str): The string value of the level.

        Returns:
            Level: The level corresponding to the specified string value.
        """
        try:
            # may throw a KeyError, if the level is not found
            return Level[level.upper()]

        # handle the KeyError and raise a ValueError
        except KeyError as exc:
            raise ValueError(f"Invalid logging level: {level}") from exc

    @staticmethod
    def from_int(level: int) -> Level:
        """
        Returns the level corresponding to the specified integer value.

        Args:
            level (int): The integer value of the level.

        Returns:
            Level: The level corresponding to the specified integer value.
        """
        try:
            # may throw a ValueError, if the level is not found
            return Level(level)

        # handle the ValueError and raise a ValueError
        except ValueError as exc:
            raise ValueError(f"Invalid logging level: {level}") from exc

    @staticmethod
    def as_dict() -> dict[str, int]:
        """
        Returns a dictionary with the level names as keys and the level values as values.

        Returns:
            dict[str, int]: The dictionary with the level names as keys and the level values as
            values.
        """
        return {level.name: level.value for level in Level}