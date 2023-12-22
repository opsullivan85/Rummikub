from piece import Piece
from board import BoardSolver


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("\n" * 5)

    print("Solving board")

    solver = BoardSolver()
    b = solver.solve(
        [
            Piece("black", 1),
            Piece("yellow", 1),
            Piece("red", 1),
            Piece("black", 11),
            Piece("yellow", 11),
            Piece("red", 11),
            Piece("blue", 11),
            # Piece("blue", 5),
            # Piece("blue", 6),
            # Piece("blue", 7),
            # Piece("blue", 8),
            # Piece("black", 6),
            # Piece("black", 7),
            # Piece("black", 8),
            # Piece("red", 4),
            # Piece("red", 5),
            # Piece("red", 6),
            # Piece("red", 7),
            # Piece("red", 8),
            # Piece("black", 9),
            # Piece("yellow", 9),
            # Piece("red", 9),
        ]
    )
    print(b)
