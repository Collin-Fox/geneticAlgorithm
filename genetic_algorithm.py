import random

import numpy as np


def fitness(n_queen):
    # Initialize the number of conflicts to 0.
    num_conflicts = 0

    # Iterate over all queens.
    for i in range(len(n_queen)):
        # Check if the current queen is attacking any other queen.
        for j in range(i + 1, len(n_queen)):
            # If the two queens are in the same row, column, or diagonal, then they are attacking each other.
            if n_queen[i] == n_queen[j] or abs(i - j) == abs(int(n_queen[i]) - int(n_queen[j])):
                num_conflicts += 1

    return num_conflicts


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

    return population_list


x = generate_initial_population(9, 15)
print(fitness(x[0]))
print(fitness(x[1]))
print(fitness(x[2]))