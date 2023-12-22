from dataclasses import dataclass
from typing import Literal


# @dataclass(eq=True, frozen=True)
class Piece:
    """A piece of the rummikub game."""
    
    __slots__ = ["color", "number"]
    
    colors = ("red", "blue", "yellow", "black")
    """Valid colors for a piece."""
    
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
            raise ValueError(f"Invalid color. Available colors are: {', '.join(Piece.colors)}")
        self.color = color
        
        if number not in range(1, 14):
            raise ValueError("Invalid number. Number must be between 1 and 13.")
        self.number = number

    def __str__(self) -> str:
        """Converts the piece to a string.

        >>> str(Piece("red", 1))
        'r1'
        """
        return f"{self.color[0]}{self.number}"
    
    def __eq__(self, __value: object) -> bool:
        """Checks if two pieces are equal.
        
        >>> r = Piece("red", 1)
        >>> r2 = Piece("red", 1)
        >>> r == r2
        True
        """
        return isinstance(__value, Piece) and self.color == __value.color and self.number == __value.number
    
    def __hash__(self) -> int:
        """Hashes the piece.
        
        >>> r1 = Piece("red", 1)
        >>> r2 = Piece("red", 1)
        >>> hash(r1) == hash(r2)
        True
        """
        return hash((self.color, self.number))
    
if __name__ == "__main__":
    import doctest

    doctest.testmod()