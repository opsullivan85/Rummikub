if __name__ == "__main__":
    # import doctest

    # doctest.testmod()

    from board import Board
    from drawpile import DrawPile
    from hand import Hand
    from piece import Piece
    from play import Play

    board = Board()
    board.plays.append(Play([Piece("red", 1), Piece("red", 2), Piece("red", 3)]))
    draw_pile = DrawPile()

    person_1 = Hand()
    person_1.pieces.append(draw_pile.draw())
    person_1.pieces.append(draw_pile.draw())
    person_1.pieces.append(draw_pile.draw())

    person_2 = Hand()
    person_2.pieces.append(draw_pile.draw())
    person_2.pieces.append(draw_pile.draw())
    person_2.pieces.append(draw_pile.draw())

    while True:
        print(board)
        print("Person 1:")
        print(person_1)
        print("Person 2:")
        print(person_2)

        board, turn_taken = person_1.take_turn(board, draw_pile)
        board, turn_taken = person_2.take_turn(board, draw_pile)

        print()
        print()
        print()
        print()
        print()
