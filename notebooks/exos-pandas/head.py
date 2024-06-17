from itertools import islice

def head(filename, nb_lines=5):
    """
    print the first nb_lines of file filename
    """
    with open(filename) as feed:
        for lineno, line in islice(enumerate(feed, 1), nb_lines):
            print(f"{lineno}:{line}", end="")
