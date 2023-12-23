from board import Board, BoardSolver
from drawpile import DrawPile
from piece import Piece
import itertools


class Hand:
    """Holds the cards in a player's hand."""

    def __init__(self, pieces: list[Piece] = None) -> None:
        self.pieces = pieces or []
        """Stores the pieces in the hand. Should be sorted."""
        self.pieces.sort()

    def __repr__(self) -> str:
        s = ""
        s += ", ".join(str(piece) for piece in self.pieces)
        return s

    def take_turn(
        self, board: Board, draw_pile: DrawPile, max_turn_size: int = 3
    ) -> tuple[Board, bool]:
        """Takes a turn.

        Tries to play a piece from the hand. If no piece can be played, draws a piece from the draw pile.

        >>> from play import Play
        >>> board = Board()
        >>> _ = board.add_play(Play([Piece("red", 1), Piece("red", 2)]))
        >>> draw_pile = DrawPile()
        >>> hand = Hand([Piece("red", 3)])
        >>> new_board, _ = hand.take_turn(board, draw_pile)
        >>> new_board.plays[0] == Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)])
        True

        Args:
            board (Board): The board to play on.
            draw_pile (DrawPile): The draw pile to draw from.
            max_turn_size (int, optional): The maximum number of pieces to play in a turn. Defaults to 3.

        Returns:
            tuple[Board, bool]: The new state of the board, and if a turn was taken.
        """
        took_turn = False
        combination_upper_bound = min(
            max_turn_size, len(self.pieces) + len(board.pieces) + 1
        )
        # try to place as many pieces as possible
        for combination_length in range(combination_upper_bound, 1, -1):
            for pieces in itertools.combinations(self.pieces, combination_length):
                try:
                    board = BoardSolver.insert(board, pieces)
                    self.pieces = [
                        piece for piece in self.pieces if piece not in pieces
                    ]
                    took_turn = True
                    break
                except RuntimeError:
                    pass

        if not took_turn:
            self.pieces.append(draw_pile.draw())
            self.pieces.sort()

        return board, took_turn


if __name__ == "__main__":
    import doctest

    doctest.testmod()
