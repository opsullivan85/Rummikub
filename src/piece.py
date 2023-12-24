from dataclasses import dataclass
from typing import Literal


# @dataclass(eq=True, frozen=True)
class Piece:
    """A piece of the rummikub game."""

    __slots__ = ["color", "number"]

    colors = ("red", "blue", "yellow", "black")
    """Valid colors for a piece."""

    max_number = 13
    """Maximum number for a piece."""

    def __init__(self, color: str, number: int) -> None:
        """Initializes a piece.

        >>> r = Piece("red", 1)
        >>> Piece("green", 1)
        Traceback (most recent call last):
        ...
        ValueError: Invalid color. Available colors are: red, blue, yellow, black
        >>> Piece("red", 14)
        Traceback (most recent call last):
        ...
        ValueError: Invalid number. Number must be between 1 and 13.

        Args:
            color (str): Color of the piece.
            number (int): Number of the piece.
        """
        if color not in Piece.colors:
            raise ValueError(
                f"Invalid color. Available colors are: {', '.join(Piece.colors)}"
            )
        self.color = color

        if number not in range(1, Piece.max_number + 1):
            raise ValueError(
                f"Invalid number. Number must be between 1 and {Piece.max_number}."
            )
        self.number = number

    def __str__(self) -> str:
        """Converts the piece to a string.

        >>> str(Piece("red", 1))
        'r1'

        Returns:
            str: The string representation of the piece.
        """
        return f"{self.color}{self.number}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        """Checks if two pieces are equal.

        >>> r = Piece("red", 1)
        >>> r2 = Piece("red", 1)
        >>> r == r2
        True

        Args:
            other (object): The object to compare to.

        Returns:
            bool: True if the pieces are equal, False otherwise.
        """
        return (
            isinstance(other, Piece)
            and self.color == other.color
            and self.number == other.number
        )

    def __lt__(self, other: object) -> bool:
        """Checks if one piece is less than another.

        Color takes precedence over number.

        >>> r = Piece("red", 1)
        >>> b = Piece("blue", 1)
        >>> b < r
        True
        >>> r < Piece("red", 2)
        True

        Args:
            other (object): The object to compare to.

        Returns:
            bool: True if the piece is less than the other, False otherwise.
        """
        return isinstance(other, Piece) and (self.color[0], self.number) < (
            other.color[0],
            other.number,
        )

    def __gt__(self, other: object) -> bool:
        """Checks if one piece is greater than another.

        Color takes precedence over number.

        >>> r = Piece("red", 1)
        >>> b = Piece("blue", 1)
        >>> r > b
        True
        >>> Piece("red", 2) > r
        True

        Args:
            other (object): The object to compare to.

        Returns:
            bool: True if the piece is greater than the other, False otherwise.
        """
        return not self < other and self != other

    def __hash__(self) -> int:
        """Hashes the piece.

        >>> r1 = Piece("red", 1)
        >>> r2 = Piece("red", 1)
        >>> hash(r1) == hash(r2)
        True

        Returns:
            int: The hash of the piece.
        """
        return hash((self.color, self.number))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
