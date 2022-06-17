from typing import List


def sat301(good_boards: List[str]):
    board_bit_reps = {tuple(sum(1 << i for i in range(9) if b[i] == c) for c in "XO") for b in good_boards}
    win = [any(i & w == w for w in [7, 56, 73, 84, 146, 273, 292, 448]) for i in range(512)]

    def tie(x, o):  # returns True if O has a forced tie/win. It's O's turn to move.
        if o | x != 511:  # complete board
            o |= 1 << [i for i in range(9) if (x, o | (1 << i)) in board_bit_reps][0]
        return not win[x] and (win[o] or all((x | o) & (1 << i) or tie(x | (1 << i), o) for i in range(9)))

    return all(tie(1 << i, 0) for i in range(9))
def sol301():
    """
    Compute a strategy for O (second player) in tic-tac-toe that guarantees a tie. That is a strategy for O that,
    no matter what the opponent does, O does not lose.

    A board is represented as a 9-char string like an X in the middle would be "....X...." and a
    move is an integer 0-8. The answer is a list of "good boards" that O aims for, so no matter what X does there
    is always good board that O can get to with a single move.
    """
    win = [any(i & w == w for w in [7, 56, 73, 84, 146, 273, 292, 448]) for i in range(512)]  # 9-bit representation

    good_boards = []

    def x_move(x, o):  # returns True if o wins or ties, x's turn to move
        if win[o] or x | o == 511:  # full board
            return True
        for i in range(9):
            if (x | o) & (1 << i) == 0 and not o_move(x | (1 << i), o):
                return False
        return True  # O wins/ties

    def o_move(x, o):  # returns True if o wins or ties, o's turn to move
        if win[x]:
            return False
        if x | o == 511:
            return True
        for i in range(9):
            if (x | o) & (1 << i) == 0 and x_move(x, o | (1 << i)):
                good_boards.append(
                    "".join(".XO"[((x >> j) & 1) + 2 * ((o >> j) & 1) + 2 * (i == j)] for j in range(9)))
                return True
        return False  # X wins

    res = x_move(0, 0)
    assert res

    return good_boards
# assert sat301(sol301())
