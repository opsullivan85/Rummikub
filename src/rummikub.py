from dataclasses import dataclass
from typing import Iterator


@dataclass
class Piece:
    """A piece of the rummikub game."""

    color: str
    number: int

    def __str__(self) -> str:
        return f"{self.color} {self.number}"


class Play:
    """Collection of pieces forming a play on the board."""

    def __init__(self, pieces: list[Piece] = None) -> None:
        self.pieces = pieces or []

    def __repr__(self) -> str:
        s = ""
        if self.is_valid_straight():
            s += "Straight: "
        elif self.is_valid_collection():
            s += "Collection: "
        else:
            s += "Invalid: "

        s += ", ".join(str(piece) for piece in self.pieces)

        return s

    def add_piece(self, piece: Piece) -> "Play":
        """Adds a piece to the play.

        Args:
            piece (Piece): The piece to add.
        """
        self.pieces.append(piece)
        return self

    def can_add_piece(self, piece: Piece) -> bool:
        """Checks if a piece can be added to the play.

        Args:
            piece (Piece): The piece to be added.

        Returns:
            bool: True if the piece can be added, False otherwise.
        """
        return self.copy().add_piece(piece).is_valid()

    def copy(self) -> "Play":
        """Return a copy of the play."""
        return Play(self.pieces[:])

    def is_valid(self) -> bool:
        """Checks if a play is valid.

        >>> Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)]).is_valid_straight()
        True
        >>> Play([Piece("red", 1), Piece("blue", 1), Piece("yellow", 1)]).is_valid_collection()
        True

        Returns:
            bool: True if the play is valid, False otherwise.
        """
        return self.is_valid_straight() or self.is_valid_collection()

    def is_valid_straight(self) -> bool:
        """Checks if a play is a valid straight.

        >>> Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)]).is_valid_straight()
        True
        >>> Play([Piece("red", 1), Piece("red", 2)]).is_valid_straight()
        False
        >>> Play([Piece("red", 1), Piece("red", 2), Piece("red", 4)]).is_valid_straight()
        False
        >>> Play([Piece("red", 1), Piece("red", 1), Piece("red", 1)]).is_valid_straight()
        False
        >>> Play([Piece("red", 1), Piece("red", 2), Piece("blue", 3)]).is_valid_straight()
        False


        Returns:
            bool: True if the play is a valid straight, False otherwise.
        """
        # atleast 3 pieces
        if len(self.pieces) < 3:
            return False

        # all same color
        if not all(piece.color == self.pieces[0].color for piece in self.pieces):
            return False

        # all consecutive numbers
        numbers = [piece.number for piece in self.pieces]
        numbers.sort()
        for expected, number in enumerate(numbers, numbers[0]):
            if not number == expected:
                return False

        return True

    def is_valid_collection(self) -> bool:
        """Checks if a play is a valid collection.

        >>> Play([Piece("red", 1), Piece("blue", 1), Piece("yellow", 1)]).is_valid_collection()
        True
        >>> Play([Piece("red", 1), Piece("blue", 1)]).is_valid_collection()
        False
        >>> Play([Piece("red", 1), Piece("blue", 1), Piece("red", 1)]).is_valid_collection()
        False
        >>> Play([Piece("red", 1), Piece("blue", 1), Piece("red", 2)]).is_valid_collection()
        False
        >>> Play([Piece("red", 1), Piece("blue", 1), Piece("red", 1), Piece("yellow", 1)]).is_valid_collection()
        False

        Returns:
            bool: True if the play is a valid collection, False otherwise.
        """
        # atleast 3 pieces
        if len(self.pieces) < 3:
            return False

        # all same number
        if not all(piece.number == self.pieces[0].number for piece in self.pieces):
            return False

        # all different colors
        if not len(self.pieces) == len(set([piece.color for piece in self.pieces])):
            return False

        return True


class Board:
    """The play area for a game of rummikub."""

    def __init__(self) -> None:
        self.plays: list[Play] = []

    def __str__(self) -> str:
        return "Board:\n\t" + "\n\t".join(str(play) for play in self.plays)

    def copy(self) -> "Board":
        """Return a copy of the board."""
        new_board = Board()
        new_board.plays = [play.copy() for play in self.plays]
        return new_board

    def get_places_for_piece(self, piece: Piece) -> Iterator[int]:
        """Gets the places where a piece can be placed on the board.

        >>> board = Board()
        >>> board.plays.append(Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)]))
        >>> list(board.get_places_for_piece(Piece("red", 4)))
        [0]
        >>> list(board.get_places_for_piece(Piece("red", 5)))
        []

        Args:
            piece (Piece): The piece to be placed.

        Returns:
            Iterator[int]: The places where the piece can be placed.
                As indices of self.plays.
        """
        for i, play in enumerate(self.plays):
            if play.can_add_piece(piece):
                yield i

    def get_neighbors(self, piece: Piece) -> Iterator["Board"]:
        """Gets the neighbors of the board.

        Args:
            piece (Piece): The piece to be placed.

        Returns:
            Iterator[Board]: The neighbors of the board.
        """
        print(f"Getting neighbors: {list(self.get_places_for_piece(piece))}")
        for i in self.get_places_for_piece(piece):
            new_board = self.copy()
            new_board.plays[i].add_piece(piece)
            yield new_board

    def is_valid(self) -> bool:
        """Checks if the board is valid.

        >>> board = Board()
        >>> board.plays.append(Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)]))
        >>> board.is_valid()
        True
        >>> board.plays.append(Play([Piece("red", 1), Piece("red", 2), Piece("red", 4)]))
        >>> board.is_valid()
        False

        Returns:
            bool: True if the board is valid, False otherwise.
        """
        return all(play.is_valid() for play in self.plays)


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

    def solve(self, pieces: list[Piece]) -> Board:
        """Solves the board.

        Args:
            pieces (list[Piece]): The pieces to be placed on the board.

        Returns:
            Board: The solved board.
        """
        root = SearchNode(
            board=Board(),
            pieces=pieces,
        )
        queue = [root]
        while queue:
            # depth first search
            node = queue.pop(-1)
            pieces = node.pieces

            # solved
            if not pieces:
                return node.board

            search_space = list(node.board.get_neighbors(pieces[0]))
            if not search_space and node.incomplete_depth < 2:
                # if there is no valid neighbor, and the incomplete depth is not too large
                # try to make a new play with the piece
                neighbor = node.board.copy()
                neighbor.plays.append(Play([pieces[0]]))
                search_space = [neighbor]

            for neighbor in search_space:
                incomplete_depth = (
                    0 if neighbor.is_valid() else node.incomplete_depth + 1
                )
                # if the board is valid, add it to the queue
                queue.append(
                    SearchNode(
                        board=neighbor,
                        pieces=pieces[1:],
                        parent=node,
                        incomplete_depth=incomplete_depth,
                    )
                )
        raise RuntimeError("No solution found.")


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("\n" * 5)

    print("Solving board")

    solver = BoardSolver()
    solver.solve(
        [
            Piece("red", 1),
            Piece("red", 2),
            Piece("red", 3),
        ]
    )
