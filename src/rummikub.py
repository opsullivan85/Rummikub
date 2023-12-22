from board import Board
from drawpile import DrawPile
from hand import Hand


def main():
    board = Board()
    draw_pile = DrawPile()

    person_1 = Hand()
    person_1.pieces.append(draw_pile.draw())
    person_1.pieces.append(draw_pile.draw())
    person_1.pieces.append(draw_pile.draw())

    person_2 = Hand()
    person_2.pieces.append(draw_pile.draw())
    person_2.pieces.append(draw_pile.draw())
    person_2.pieces.append(draw_pile.draw())

    for _ in range(10):
        print(board)
        print("Person 1:")
        print(f"\t{person_1}")
        print("Person 2:")
        print(f"\t{person_2}")

        board, turn_taken = person_1.take_turn(board, draw_pile)
        board, turn_taken = person_2.take_turn(board, draw_pile)

        print()
        print()
        print()
        print()
        print()


if __name__ == "__main__":
    # import doctest

    # doctest.testmod()

    main()
