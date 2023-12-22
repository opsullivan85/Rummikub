from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Piece:
    """A piece of the rummikub game."""

    color: str
    number: int

    def __str__(self) -> str:
        return f"{self.color[0]}{self.number}"