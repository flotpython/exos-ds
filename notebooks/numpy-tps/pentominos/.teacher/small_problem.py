from xcover import covers_bool

import numpy as np

INPUT = [
    (1, 0,   0, 1, 1, 0, 1, 0),
    (1, 0,   0, 0, 1, 1, 0, 1),
    (1, 0,   0, 0, 1, 1, 1, 0),
    (1, 0,   1, 0, 1, 1, 0, 0),
    (1, 0,   0, 0, 1, 0, 1, 1),
    (1, 0,   1, 1, 1, 0, 0, 0),
    (1, 0,   0, 0, 0, 1, 1, 1),
    (0, 1,   0, 1, 1, 0, 1, 0),
    (0, 1,   0, 0, 1, 1, 0, 1),
    (0, 1,   0, 0, 1, 1, 1, 0),
    (0, 1,   1, 0, 1, 1, 0, 0),
    (0, 1,   0, 0, 1, 0, 1, 1),
    (0, 1,   1, 1, 1, 0, 0, 0),
    (0, 1,   0, 0, 0, 1, 1, 1),
]

solutions = covers_bool(np.array(INPUT, dtype=bool))

for solution in solutions:
    print(solution)