from piece import Piece
import pickle
import atexit


class Play:
    """Collection of pieces forming a play on the board."""

    play_valid_cache = {}
    loaded_cache = False
    cache_hits = 0

    def __init__(self, pieces: list[Piece] = None) -> None:
        """Creates a play.

        Args:
            pieces (list[Piece], optional): Pieces to create the play with. Defaults to None.
        """
        self.pieces = pieces or []
        """Pieces in the play. Should be sorted."""
        self.pieces.sort()
        self._is_valid = None

    @staticmethod
    def save_cache():
        """Saves the cache to the file."""
        with open("play_valid_cache.pkl", "wb") as f:
            data = pickle.dumps(Play.play_valid_cache)
            f.write(data)

    @staticmethod
    def load_cache():
        """Loads the cache from the file."""
        try:
            with open("play_valid_cache.pkl", "rb") as f:
                data = f.read()
                Play.play_valid_cache = pickle.loads(data)
                Play.loaded_cache = True
                print("Loaded play_valid_cache")
        except FileNotFoundError:
            pass

    def __hash__(self) -> int:
        """Gets the hash of the play.

        >>> play1 = Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)])
        >>> play2 = Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)])
        >>> hash(play1) == hash(play2)
        True

        Returns:
            int: The hash of the play.
        """
        return hash(tuple(self.pieces))

    def __eq__(self, other: "Play") -> bool:
        """Checks if two plays are equal.

        >>> play1 = Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)])
        >>> play2 = Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)])
        >>> play1 == play2
        True

        Args:
            other (Play): The object to compare to.

        Returns:
            bool: True if the plays are equal, False otherwise.
        """
        if not isinstance(other, Play):
            return False
        return self.pieces == other.pieces

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

        >>> play = Play()
        >>> _ = play.add_piece(Piece("red", 1))
        >>> play.pieces == [Piece("red", 1)]
        True

        Args:
            piece (Piece): The piece to add.

        Returns:
            The play with the piece added to.
        """
        self.pieces.append(piece)
        self.pieces.sort()
        self._is_valid = None  # invalidate cache
        return self

    def can_add_piece(self, piece: Piece, allow_partial: bool = False) -> bool:
        """Checks if a piece can be added to the play.

        >>> play1 = Play([Piece("red", 1), Piece("red", 2)])
        >>> play1.can_add_piece(Piece("red", 3))
        True
        >>> play1.can_add_piece(Piece("red", 4))
        False
        >>> play2 = Play([Piece("red", 1)])
        >>> play2.can_add_piece(Piece("red", 2))
        False
        >>> play2.can_add_piece(Piece("red", 2), allow_partial=True)
        True

        Args:
            piece (Piece): The piece to be added.
            allow_partial (bool): If the play can be a partial play.
                ex. [r1] + [r2] is a partial play, but [r1, r2] + [r3] is not.

        Returns:
            bool: True if the piece can be added, False otherwise.
        """
        return self.copy().add_piece(piece).is_valid(allow_partial=allow_partial)

    def copy(self) -> "Play":
        """Returns a copy of the play.

        >>> play1 = Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)])
        >>> play2 = play1.copy()
        >>> play1 == play2
        True
        >>> play1 is play2
        False

        Returns:
            Play: _description_
        """
        return Play(self.pieces[:])

    def is_valid(self, allow_partial: bool = False) -> bool:
        """Checks if a play is valid.

        >>> Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)]).is_valid_straight()
        True
        >>> Play([Piece("red", 1), Piece("blue", 1), Piece("yellow", 1)]).is_valid_collection()
        True
        >>> Play([Piece("red", 1), Piece("red", 2)]).is_valid_straight()
        False
        >>> Play([Piece("red", 1), Piece("blue", 1)]).is_valid_collection()
        False
        >>> Play([Piece("red", 1), Piece("red", 2)]).is_valid_straight(allow_partial=True)
        True
        >>> Play([Piece("red", 1), Piece("blue", 1)]).is_valid_collection(allow_partial=True)
        True

        Args:
            allow_partial (bool): If the play can be a partial play.
                ex. [r1] + [r2] is a partial play, but [r1, r2] + [r3] is not.

        Returns:
            bool: True if the play is valid, False otherwise.
        """
        # see if already calculated
        if self._is_valid is not None:
            return self._is_valid

        # check cache
        cache_object = (self, allow_partial)
        if cache_object in Play.play_valid_cache:
            Play.cache_hits += 1
            rval = Play.play_valid_cache[cache_object]

        else:
            # do the actual check
            rval = self.is_valid_straight(
                allow_partial=allow_partial
            ) or self.is_valid_collection(allow_partial=allow_partial)
            Play.play_valid_cache[cache_object] = rval

        self._is_valid = rval
        return rval

    def is_valid_straight(self, allow_partial: bool = False) -> bool:
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

        Args:
            allow_partial (bool): If the play can be a partial play.
                ex. [r1] + [r2] is a partial play, but [r1, r2] + [r3] is not.

        Returns:
            bool: True if the play is a valid straight, False otherwise.
        """
        # atleast 3 pieces
        if not allow_partial and len(self.pieces) < 3:
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

    def is_valid_collection(self, allow_partial: bool = False) -> bool:
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

        Args:
            allow_partial (bool): If the play can be a partial play.
                ex. [r1] + [r2] is a partial play, but [r1, r2] + [r3] is not.

        Returns:
            bool: True if the play is a valid collection, False otherwise.
        """
        # atleast 3 pieces
        if not allow_partial and len(self.pieces) < 3:
            return False

        # all same number
        if not all(piece.number == self.pieces[0].number for piece in self.pieces):
            return False

        # all different colors
        if not len(self.pieces) == len(set([piece.color for piece in self.pieces])):
            return False

        return True


if not Play.loaded_cache:
    Play.load_cache()
    atexit.register(Play.save_cache)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
