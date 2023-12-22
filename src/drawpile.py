from piece import Piece
import random


class DrawPile:
    """Draw pile class."""

    duplicates = 2
    """The number of duplicates of each piece in the draw pile."""

    def __init__(self) -> None:
        """Initializes the draw pile.

        >>> draw_pile = DrawPile()
        >>> len(draw_pile._pieces) == DrawPile.duplicates * len(Piece.colors) * Piece.max_number
        True
        """
        self._pieces = []

        for _ in range(DrawPile.duplicates):
            for color in Piece.colors:
                for number in range(1, Piece.max_number + 1):
                    self._pieces.append(Piece(color, number))

        random.shuffle(self._pieces)

    def draw(self) -> Piece:
        """Draws a piece from the draw pile.

        >>> draw_pile = DrawPile()

        # normally this would be randomly shuffled
        >>> draw_pile._pieces = [Piece("red", 1), Piece("red", 2), Piece("red", 3)]
        >>> str(draw_pile.draw())
        'r3'

        Returns:
            Piece: The piece drawn from the draw pile.
        """
        try:
            return self._pieces.pop()
        except IndexError:
            raise RuntimeError("Draw pile is empty.")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
