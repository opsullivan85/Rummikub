from dataclasses import dataclass
from typing import Iterator
from play import Play
from piece import Piece
import pickle
import atexit


class Board:
    """The play area for a game of rummikub."""

    def __init__(self) -> None:
        self.plays: list[Play] = []
        self.num_patial_plays = 0
        """Stores the number of partial plays on the board.
        ex. [r1] + [r2] is a partial play, but [r1, r2] + [r3] is not.
        """

    def __hash__(self) -> int:
        """Gets the hash of the board.

        >>> board1 = Board()
        >>> board1.plays.append(Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)]))
        >>> board2 = Board()
        >>> board2.plays.append(Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)]))
        >>> hash(board1) == hash(board2)
        True

        Returns:
            int: The hash of the board.
        """
        return hash(tuple(self.plays))

    def __eq__(self, other: "Board") -> bool:
        """Checks if two boards are equal.

        >>> board1 = Board()
        >>> board1.plays.append(Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)]))
        >>> board2 = Board()
        >>> board2.plays.append(Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)]))
        >>> board1 == board2
        True

        Args:
            other (Board): The object to compare to.

        Returns:
            bool: True if the boards are equal, False otherwise.
        """
        return self.plays == other.plays

    def __str__(self) -> str:
        return "Board:\n\t" + "\n\t".join(str(play) for play in self.plays)

    def copy(self) -> "Board":
        """Return a copy of the board.

        >>> board1 = Board()
        >>> board1.plays.append(Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)]))
        >>> board2 = board1.copy()
        >>> board1 == board2
        True
        >>> board1 is board2
        False
        >>> board1.plays[0] = Play([Piece("red", 1)])
        >>> board1 == board2
        False

        Returns:
            Board: The copy of the board.
        """
        new_board = Board()
        new_board.plays = [play.copy() for play in self.plays]
        new_board.num_patial_plays = self.num_patial_plays
        return new_board

    def get_places_for_piece(
        self, piece: Piece, allow_partial: bool = False
    ) -> Iterator[int]:
        """Gets the places where a piece can be placed on the board.

        >>> board = Board()
        >>> board.plays.append(Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)]))
        >>> list(board.get_places_for_piece(Piece("red", 4)))
        [0]
        >>> list(board.get_places_for_piece(Piece("red", 5)))
        []

        Args:
            piece (Piece): The piece to be placed.
            allow_partial (bool): If the play can be a partial play.
                ex. [r1] + [r2] is a partial play, but [r1, r2] + [r3] is not.

        Returns:
            Iterator[int]: The places where the piece can be placed.
                As indices of self.plays.
        """
        for i, play in enumerate(self.plays):
            if play.can_add_piece(piece, allow_partial=allow_partial):
                yield i

    def add_piece(self, piece: Piece, play_index: int) -> "Board":
        """Adds a piece to the board on a certian play.

        Args:
            piece (Piece): The piece to be placed.
            play_index (int): The index of the play to place the piece on.

        Returns:
            Board: This board with the piece added.
        """
        was_partial = self.plays[play_index].is_valid()
        self.plays[play_index].add_piece(piece)
        is_partial = self.plays[play_index].is_valid()

        # update the number of partial plays
        # it can only change if the play was partial and is no longer partial
        if was_partial and not is_partial:
            self.num_patial_plays -= 1
        elif not was_partial and is_partial:
            raise RuntimeError("This function shouldn't make a new play partial")

        return self

    def add_play(self, play: Play) -> "Board":
        """Adds a play to the board.

        Args:
            play (Play): The play to be added.

        Returns:
            Board: This board with the play added.
        """
        self.plays.append(play)
        if not play.is_valid():
            self.num_patial_plays += 1

        return self

    def get_neighbors(
        self, piece: Piece, allow_partial: bool = False
    ) -> Iterator["Board"]:
        """Gets the neighbors of the board.

        >>> board = Board()
        >>> board.plays.append(Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)]))
        >>> neighbor = list(board.get_neighbors(Piece("red", 4)))[0]
        >>> board2 = Board()
        >>> board2.plays.append(Play([Piece("red", 1), Piece("red", 2), Piece("red", 3), Piece("red", 4)]))
        >>> neighbor == board2
        True

        Args:
            piece (Piece): The piece to be placed.
            allow_partial (bool): If the play can be a partial play.
                ex. [r1] + [r2] is a partial play, but [r1, r2] + [r3] is not.

        Returns:
            Iterator[Board]: The neighbors of the board.
        """
        for i in self.get_places_for_piece(piece, allow_partial=allow_partial):
            new_board = self.copy()
            new_board.add_piece(piece, i)
            yield new_board

    def is_valid(self) -> bool:
        """Checks if the board is valid.

        >>> board = Board()
        >>> _ = board.add_play(Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)]))
        >>> board.is_valid()
        True
        >>> _ = board.add_play(Play([Piece("red", 1), Piece("red", 2), Piece("red", 4)]))
        >>> board.is_valid()
        False

        Args:
            allow_partial (bool): If the play can be a partial play.
                ex. [r1] + [r2] is a partial play, but [r1, r2] + [r3] is not.

        Returns:
            bool: True if the board is valid, False otherwise.
        """
        return self.num_patial_plays == 0


@dataclass
class SearchNode:
    board: Board
    """The board of the node."""
    pieces: list[Piece] = None
    """The pieces to be placed on the board."""
    parent: "SearchNode" = None
    """The parent node."""
    incomplete_depth: int = 0
    """The depth of the node where the board is invalid."""


class BoardSolver:
    """Class to handle solving the board."""

    solver_cache = {}

    @staticmethod
    def save_cache():
        """Saves the cache to the file."""
        with open("solver_cache.pkl", "wb") as f:
            data = pickle.dumps(BoardSolver.solver_cache)
            f.write(data)

    @staticmethod
    def load_cache():
        """Loads the cache from the file."""
        try:
            with open("solver_cache.pkl", "rb") as f:
                data = f.read()
                BoardSolver.solver_cache = pickle.loads(data)
                print("Loaded solver_cache")
        except FileNotFoundError:
            pass

    @staticmethod
    def insert(board: Board, pieces: list[Piece]) -> Board:
        """Attempts to add a piece to the board.

        Args:
            piece (list[Piece]): The pieces to be inserted.
            board (Board): The board to insert the piece into.

        Returns:
            Board: The new board with the piece inserted.
        """
        pieces = [piece for play in board.plays for piece in play.pieces] + list(pieces)
        return BoardSolver.solve(pieces)

    @staticmethod
    def solve(pieces: list[Piece]) -> Board:
        """Solves the board.

        Args:
            pieces (list[Piece]): The pieces to be placed on the board.

        Returns:
            Board: The solved board.
        """
        # check if there aren't enough pieces to make a solution
        if len(pieces) < 3:
            raise RuntimeError("No solution found.")

        # check if the board has already been solved
        solver_cache_key = tuple(pieces)
        if solver_cache_key in BoardSolver.solver_cache:
            if BoardSolver.solver_cache[solver_cache_key] is None:
                raise RuntimeError("No solution found.")
            return BoardSolver.solver_cache[solver_cache_key]
        BoardSolver.solver_cache[solver_cache_key] = None

        explored = set()
        queue = [
            SearchNode(
                board=Board(),
                pieces=pieces,
            )
        ]
        while queue:
            # depth first search
            node = queue.pop(-1)
            pieces = node.pieces

            # if there are not remaining pieces
            # and the board is valid
            if not pieces and node.incomplete_depth == 0:
                BoardSolver.solver_cache[solver_cache_key] = node.board
                return node.board

            for piece in pieces:
                other_pieces = pieces[:]
                other_pieces.pop(other_pieces.index(piece))
                search_space = list(node.board.get_neighbors(piece, allow_partial=True))

                # if there is no valid neighbor, and the incomplete depth is not too large
                # try to make a new play with the piece
                if not search_space and node.incomplete_depth < 2:
                    neighbor = node.board.copy()
                    neighbor.add_play(Play([piece]))
                    search_space = [neighbor]

                for neighbor in search_space:
                    # check cache
                    if neighbor in explored:
                        continue

                    # don't explore nodes with more than one partial play
                    # this reduces the search space by forcing the solver to
                    # complete partial plays before making new ones
                    if neighbor.num_patial_plays > 1:
                        continue

                    # add to cache
                    explored.add(neighbor)

                    incomplete_depth = (
                        0 if neighbor.is_valid() else node.incomplete_depth + 1
                    )
                    # if the board is valid, add it to the queue
                    queue.append(
                        SearchNode(
                            board=neighbor,
                            pieces=other_pieces,
                            parent=node,
                            incomplete_depth=incomplete_depth,
                        )
                    )
        raise RuntimeError("No solution found.")


BoardSolver.load_cache()
atexit.register(BoardSolver.save_cache)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
