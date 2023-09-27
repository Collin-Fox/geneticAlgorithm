import random

import numpy as np


def fitness(n_queen):
    """
    :param n_queen: String instance of nqueens problem '13....n'

    :return: How many conflicts we have in
    """
    return -1


def generate_initial_population(n: int, population_size: int):
    """

    :param population_size:
    :param n: integer of how many queens we have IE n = 7 -> 7 Queens problem, string length is 7

    Call to fitness function after population is generated and sort by fitness
    THE LOWER THE FITNESS THE BETTER THE STATE IS

    :return: Set(no repetitions of strings) of Strings that represent a single N queens problem state.
    """
    # Create the initial string for N queens
    initial = ""
    for i in range(1, n + 1):
        initial += str(i)

    # Create a set of permutations
    from itertools import permutations
    perms = [''.join(p) for p in permutations(initial)]
    perms = set(perms)

    # Selecting N random elements from the set for initial population
    population_list = random.sample(list(perms), population_size)

    print(population_list)

    return -1


generate_initial_population(9, 15)
