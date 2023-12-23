from board import Board
from drawpile import DrawPile
from hand import Hand

from board import BoardSolver
from play import Play


def main():
    board = Board()
    draw_pile = DrawPile()

    person_1 = Hand()

    person_2 = Hand()

    for _ in range(14):
        person_1.pieces.append(draw_pile.draw())
        person_2.pieces.append(draw_pile.draw())

    person_1.pieces.sort()
    person_2.pieces.sort()

    turn = 0
    while person_1.pieces and person_2.pieces:
        turn += 1
        print(turn)
        print(board)
        print("Person 1:")
        print(f"\t{person_1}")
        print("Person 2:")
        print(f"\t{person_2}")

        board, turn_taken = person_1.take_turn(board, draw_pile)
        board, turn_taken = person_2.take_turn(board, draw_pile)

        print(f"{BoardSolver.nodes_explored = }")
        print(f"{BoardSolver.board_cache_hits = }")
        print(f"{BoardSolver.node_cache_hits = }")
        print(f"{BoardSolver.partial_plays_skipped = }")
        print(f"{BoardSolver.incomplete_depth_skipped = }")
        print(f"{Play.cache_hits = }")
        print()
        print()
        print()
        print()
        print()


if __name__ == "__main__":
    # import doctest

    # doctest.testmod()

    main()
