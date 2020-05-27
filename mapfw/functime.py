from time import time


def time_fun(problem, funct):
    s = time()
    solution = funct(problem)
    e = time() - s
    return solution, e
