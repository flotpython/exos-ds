import numpy as np


def np_from_text(text):
    """
    convert a text representation of a board into a numpy array
    """
    return np.array([[int(c) if c != "." else 0 for c in line] for line in text.split("\n") if line.strip()])


# from D. Knuth taocp section 7.2.2.1 figure (29)
BOARD_29a = np_from_text("""
..3.1....
415....9.
2.65..3..
5...8...9
.7.9...32
.38..4.6.
...26.4.3
...3....8
32...795.
""")

BOARD_29b = np_from_text("""
......3..
1..4.....
......1.5
9........
.....26..
....53...
.5.8.....
...9...7.
.83....4.
""")

BOARD_29c = np_from_text("""
.3..1....
...4..1..
.5.....9.
2.....6.4
....35...
1........
4..6.....
.......5.
.9.......
""")
