#!/usr/bin/env python3

"""
a rustic way to map pentomino-like problems
onto exact_cover, and back
"""

import numpy as np
import exact_cover_py
from pentominos_data import PENTOMINOS


# convenience: all boards defined in pentominos_data.py
import pentominos_data as data
glob = dir(data)
ALL_BOARDS = {x: getattr(data, x) for x in data.__dict__ if x.startswith('BOARD')}


# globals
DEBUG = False
NO_SYMMETRY = False


def compute_symmetries(a):
    """Find all symmetries of a given pentomino."""
    symmetries = []
    for i in range(4):
        a = np.rot90(a)
        if not any(np.array_equal(a, s) for s in symmetries):
            symmetries.append(a)
    a = np.flip(a, axis=0)
    if not any(np.array_equal(a, s) for s in symmetries):
        symmetries.append(a)
    for i in range(4):
        a = np.rot90(a)
        if not any(np.array_equal(a, s) for s in symmetries):
            symmetries.append(a)
    return symmetries


def find_all_translations(board, piece):
    """
    given a board and an individual piece, find all possible locations
    by translation
    result is provided as a list of locations
    each location is a flat array of size board.size, where 1 indicates the piece is present
    """
    locations = []
    bh, bw = board.shape
    ph, pw = piece.shape
    for i in range(bh - ph + 1):
        for j in range(bw - pw + 1):
            # does the piece fit in this position ?
            if np.any(board[i: i + ph, j : j + pw] & piece):
                continue
            tmp = board.copy()
            tmp[i: i + ph, j: j + pw] |= piece
            # .flatten() = .reshape(-1)
            locations.append(tmp.flatten())
    return locations


def decorate_location_with_piece_number(location, nb_pieces, piece_index):
    """
    location is a flat array of size board.size, where 1 indicates the piece is present
    nb_pieces is the total number of pieces
    piece_index is the index of the piece

    returns a flat array of size  (nb_pieces + location.size)
    with a single 1 added in the position of the piece_index
    """
    result = np.zeros((nb_pieces + location.size,), dtype=location.dtype)
    result[piece_index] = 1
    result[-location.size :] = location
    return result


def all_exact_cover_lines(board, pieces):
    """
    produce the matrix that gets input into exact_cover
    """
    lines = []
    nb_pieces = len(pieces)
    for piece_index, piece in enumerate(pieces):
        if NO_SYMMETRY:
            symmetries = [piece]
        else:
            symmetries = compute_symmetries(piece)
        for s_index, s in enumerate(symmetries):
            # print(
            #     40 * "=",
            #     f"piece {list(RAW_SHAPES.keys())[piece_index]} symmetry {s_index}",
            # )
            locations = find_all_translations(board, s)
            for location in locations:
                # if piece_index == 0:
                # print(location.reshape(board.shape).astype(int))
                line = decorate_location_with_piece_number(
                    location, nb_pieces, piece_index
                )
                lines.append(line)
    result = np.array(lines)
    # now there is a technicity: some columns here are full of 1's
    # this is for places where the board has 1s already
    projection = ~result.all(axis=0)
    indices_to_keep = np.where(projection > 0)[0]
    return result[:, indices_to_keep]


def solve(board, pieces, name="anonymous"):
    """
    given a board definition and a list of pieces,
    computes 'lines' as the input to exact_cover_py
    and the solution provided by exact_cover_py
    both are returned
    """
    lines = all_exact_cover_lines(board, pieces)
    if DEBUG:
        print(
            f"sending to exact_cover_py lines with {lines.shape=} and {lines.dtype=}"
        )
        # print(lines)
        # save input matrix as csv
        import pandas as pd
        df = pd.DataFrame(lines, dtype=np.uint8)
        df.to_csv(f"{name}.csv", index=False)
    try:
        solutions_gen = exact_cover_py.exact_covers(lines)
        solution = next(solutions_gen)
        DEBUG and print(f"solution is of {type(solution)=})")
        DEBUG and print(f"and in details", solution)
        # for index, i in enumerate(solution):
        #     print(f"piece {index} goes at {lines[i]}")
        return lines, solution
    except exact_cover.error.NoSolution:
        # print(f"no solution found on board {board.shape=}")
        return lines, None


def pretty_solution(board, pieces, lines, solution):
    """
    Parameters:
      - board: the shape to be filled 
      - pieces: the pieces to fill the board
      - lines: the full data as passed to exact_cover
      - solution: one solution, as a list of indices within lines
    Returns:
      - a board with the pieces numbered according to the solution

    NOTE: in the incoming board, obstacles are 1 and free space is 0
    however in the outcome of this function, obstacles are 0 and then
    each piece is numbered starting from 1
    """
    # the main job here is to interpret each line in the solution
    # as a piece and its final location
    # remember there may be forbidden slots in the board, and that these
    # are not represented in the solution

    # map an index in the solution >= nb_pieces
    # to the rank in the - flattened - board
    DEBUG and print(f"{lines.astype(np.uint8)=}")
    WIDTH = len(lines[0])
    map = np.zeros(WIDTH, dtype=int)
    # the first slot in the board (upper-left corner) is mapped to column nb-pieces
    index = len(pieces)
    for i in range(board.size):
        if board.flat[i] == 0:
            map[index] = i
            index += 1
    DEBUG and print(f"map={map}")
    first_line = lines[solution[0]]
    DEBUG and print(f"{first_line=}")

    # need to invert the board as 0s are now obstacles
    result = 1 - board

    def fill_result_with_solution(solution_line):
        # compute piece number
        piece_index = np.where(solution_line[: len(pieces)] == True)[0][0]
        # first piece is numberd 1
        piece_index += 1
        for i in range(len(pieces), len(solution_line)):
            if solution_line[i] == True:
                result.flat[map[i]] = piece_index

    for solution_index in solution:
        fill_result_with_solution(lines[solution_index])
    return result


def sanity_check(lines, solution):
    extract = lines[solution]
    DEBUG and print(f"sanity check {extract.shape}")
    # print(extract)
    DEBUG and print(f"sum by column=", extract.sum(axis=0))


def enable_full_print():
    import sys

    np.set_printoptions(threshold=sys.maxsize)
    np.set_printoptions(linewidth=150)


def full_monty(name, board, pieces):
    print(40*'=', name)
    lines, solution = solve(board, pieces, name)
    if solution is None:
        print(f"no solution for", board)
    else:
        sanity_check(lines, solution)
        pretty = pretty_solution(board, pieces, lines, solution)
        print(pretty)


def draw(solution, *, cmap_name="copper", filename=None):
    """
    given a nd-array with 0's for obstacles and
    positive numbers for contiguous pieces, draw it under matplotlib
    """
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from matplotlib.colors import ListedColormap
    nb_colors = solution.max() + 1
    cmap = mpl.colormaps[cmap_name].resampled(nb_colors)
    # make color 0 transparent
    tmp = cmap(range(nb_colors))
    tmp[0, :] = 1, 1, 1, 0
    cmap_0 = ListedColormap(tmp)
    plt.figure()
    plt.imshow(solution, cmap=cmap_0)
    if filename:
        plt.savefig(filename)
    plt.show()


def triminoes():
    full_monty("triminoes", SMALL_BOARD, [SMALL_PIECE, SMALL_PIECE])


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--no-symmetry", action="store_true")
    parser.add_argument("-s", "--small", action="store_true")
    parser.add_argument("-p", "--pentamino", action="store_true")
    args = parser.parse_args()
    global DEBUG
    DEBUG = args.debug
    global NO_SYMMETRY
    NO_SYMMETRY = args.no_symmetry
    enable_full_print()
    if args.small:
        triminoes()
    elif args.pentamino:
        full_monty("pentamino", ALL_BOARDS['BOARD_5_12'], PENTOMINOS)
    else:
        for name, board in ALL_BOARDS.items():
            full_monty(name, board, PENTOMINOS)


if __name__ == "__main__":
    main()
