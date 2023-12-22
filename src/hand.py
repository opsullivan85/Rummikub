from board import Board, BoardSolver
from drawpile import DrawPile
from piece import Piece


class Hand:
    """Holds the cards in a player's hand."""

    def __init__(self, pieces: list[Piece] = None) -> None:
        self.pieces = pieces or []

    def __repr__(self) -> str:
        s = ""
        s += ", ".join(str(piece) for piece in self.pieces)
        return s

    def take_turn(self, board: Board, draw_pile: DrawPile) -> Board:
        """Takes a turn.

        Tries to play a piece from the hand. If no piece can be played, draws a piece from the draw pile.

        >>> from play import Play
        >>> board = Board()
        >>> board.plays.append(Play([Piece("red", 1), Piece("red", 2)]))
        >>> draw_pile = DrawPile()
        >>> hand = Hand([Piece("red", 3)])
        >>> new_board = hand.take_turn(board, draw_pile)

        # the pieces are reversed because of how the solver works
        >>> new_board.plays[0].pieces == [Piece("red", 3), Piece("red", 2), Piece("red", 1)]
        True

        Args:
            board (Board): The board to play on.
            draw_pile (DrawPile): The draw pile to draw from.

        Returns:
            Board: The new state of the board. Possible unchanged.
        """
        made_move = False
        # just implementing a greedy algorithm for now
        for piece in self.pieces:
            try:
                board = BoardSolver.insert(board, piece)
                self.pieces.remove(piece)
                made_move = True
            except RuntimeError:
                pass

        if not made_move:
            self.pieces.append(draw_pile.draw())

        return board


if __name__ == "__main__":
    import doctest

    doctest.testmod()
