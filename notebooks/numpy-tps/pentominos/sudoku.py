from collections import defaultdict
from itertools import product
import numpy as np

def exact_cover_input(sudoku):
    """
    input is expected to be a 9x9 numpy array containing
    the sudoku board encoded with 0 for empty cells

    some examples are defined in sudoku_data.py

    the output is a tuple:
    - is a numpy boolean representing this grid, to be fed into an exact cover solver
    - a dictionary that maps the row index in the boolean array to the (i, j, k) tuple

    when no cell are known, the array will have
    - fewer than 324 rows:
      81 constraints for cells, 81for rows, 81 for columns, and 81 for boxes
    - fewer than 729 columns (81 cells * 9 possible digits)

    assuming the problem has n known cells, the actual outcome will have a
    reduced number of rows and of columns in the following way:
    - rows = 4 * (81-n)
    - columns: there are fewer columns because
        - the known positions are not encoded
        - also the positions that are obviously not possible are not encoded either
          e.g. if we know that cell (1, 0) contains '4' like in BOARD_29a, then
          we know that cell (0, 0) cannot contain '4' either
        see section 7.2.2.1 p. 11 of D. Knuth's TAOCP for the full example of BOARD_29a
    """
    # there are a total of 4*9*9 = 324 constraints
    # i j mean row and column as usual
    # k is the number in that cell; for easying arithmentic
    # it will be in [0,8] instead of [1,9]
    # x is a box index, in [0,8] too, and computed as x = 3*(i//3) + j//3
    # pij means that cell (i,j) is covered exactly once
    # rik means that row i contains digit k
    # cjk means that column j contains digit k
    # bxk means that box x contains digit k
    #
    # so for example, the option of putting number 5 in cell (3,7)
    # will be encoded as:
    # k = 5
    # x = 3*(3//3) + 7//3 = 3*1 + 2 = 5
    # p34, r35, c75, b55
    # so this option will contain 4 columns numbered
    # 3*9+4, 81+9*3+5, 162+7*9+5, 243+5*9+5

    def p_r_c_b(i, j, k):
        """
        the 4 item (column) indices for cell (i,j) containing digit k
        """
        x = 3*(i//3) + j//3
        return 9*i+j, 81 + 9*i+k, 162 + 9*j+k, 243 + 9*x+k

    # def opt(i, j, k):
    #     """
    #     the option (row) index for cell (i,j) containing digit k
    #     """
    #     return 81*i + 9*j + k

    # we start with computing the possible options for each cell
    # i.e. like in (31) on p. 11, we build a dict that has 89 (i, j) keys
    # and a set of possible digits as values
    possible = {}
    for i, j in product(range(9), repeat=2):
        possible[i, j] = set(range(9))
    for i, j in product(range(9), repeat=2):
        k = sudoku[i, j] - 1
        if k >= 0:
            # remove all options for cell (i,j) except the one with digit k
            possible[i, j] = {k}
            bx, by = 3*(i//3), 3*(j//3)
            cx, cy = i%3, j%3
            # remove all options for other cells in the same row, column, and box
            for other in range(9):
                if other != i:
                    possible[other, j] -= {k}
                if other != j:
                    possible[i, other] -= {k}
                ocx, ocy = other%3, other//3
                if (ocx, ocy) != (cx, cy):
                    possible[bx+ocx, by+ocy] -= {k}

    # all the (i, j) that correspond to a given in the problem
    # are removed from the equation
    # NOTE that as far as solving is concerned, we could also remove
    # the (i, j) that have only one possible digit (naked singles)
    # however this would make the decoder/pretty-printer more complex
    # and keeping columns with one single option does not imped the solver
    # thanks to the MRV heuristic
    # so: initialize the result array with 4*9*9 columns
    # and this number of rows:
    nb_rows = sum(len(possible[i, j])
                      for i, j in product(range(9), repeat=2)
                      if sudoku[i, j] == 0)

    result = np.zeros((nb_rows, 4*9*9), dtype=bool)
    # the decoder maps the row index to the (i, j, k) tuple
    decoder = {}

    # also collect the indices of columns to remove
    columns_to_remove = []

    row = 0
    for (i, j), digits in possible.items():
        if sudoku[i, j] == 0:
            for k in digits:
                p, r, c, b = p_r_c_b(i, j, k)
                result[row, [p, r, c, b]] = True
                decoder[row] = (i, j, k)
                row += 1
        else:
            k = next(iter(possible[i, j]))
            p, r, c, b = p_r_c_b(i, j, k)
            columns_to_remove.extend([p, r, c, b])

    # remove those columns and return
    exact_cover_input = np.delete(result, columns_to_remove, axis=1)
    return exact_cover_input, decoder


def pretty_print(problem, solutions, decoder):
    """
    input parameters:
    - problem: a 9x9 numpy array containing the sudoku board
    - solutions: the output of exact_cover that solves the problem
    - decoder: the output of exact_cover_input that maps the row index to the (i, j, k) tuple

    returns:
    - the incoming problem with the solution filled in
    """
    if len(solutions) != 1:
        raise ValueError("expected a single solution")
    solution = solutions[0]
    for row in solution:
        i, j, k = decoder[row]
        if problem[i, j] != 0:
            raise ValueError(f"cell ({i}, {j}) already filled !")
        problem[i, j] = k + 1
    if np.any(problem == 0):
        raise ValueError("not all cells filled")
    return problem

def make_data():

    def iterate_data():
        import sudoku_data
        for name in dir(sudoku_data):
            if name.startswith("BOARD_"):
                sudoku = getattr(sudoku_data, name)
                yield name, sudoku

    import pandas as pd
    for name, sudoku in iterate_data():
        name = name.lower().replace("_", "-")
        problem, decoder = exact_cover_input(sudoku)
        df = pd.DataFrame(problem)
        df.to_csv(f"sudoku-{name}.csv", index=False, header=False)
