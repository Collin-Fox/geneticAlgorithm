import random
import numpy as np
from itertools import permutations


def fitness(queen_positions):
    num_conflicts = 0

    for i in range(len(queen_positions)):
        for j in range(i + 1, len(queen_positions)):
            if queen_positions[i] == queen_positions[j] or abs(i - j) == abs(queen_positions[i] - queen_positions[j]):
                num_conflicts += 1

    return num_conflicts


def generate_initial_population(n):
    population_size = int((n * n) * np.ceil(np.log2(n)))
    initial = "".join([str(i) for i in range(1, n + 1)])

    population = set()
    while len(population) < population_size:
        permutation = "".join(random.sample(initial, len(initial)))
        population.add(permutation)

    return list(population)


def sort_by_fitness(population):
    return sorted(population, key=fitness)


def select_parents(population):
    parents = []
    total_fitness = sum(fitness(p) for p in population)

    for individual in population:
        fitness_value = fitness(individual)
        probability = (len(individual) * (len(individual - 1)) - fitness_value) / total_fitness

        if random.random() < probability:
            parents.append(individual)

    return parents


def crossover(parent1, parent2):
    i = random.randint(0, len(parent1) - 1)
    j = random.randint(0, len(parent2) - 1)

    child1 = parent1[:i] + parent2[i:j] + parent1[j:]
    child2 = parent2[:i] + parent1[i:j] + parent2[j:]

    return child1, child2


def mutate(individual):
    # Mutate with 5% probability
    if random.random() < 0.05:
        i = random.randint(0, len(individual) - 1)
        j = random.randint(0, len(individual) - 1)
        individual = swap_chars(individual, i, j)

    return individual


def swap_chars(string, i, j):
    lst = list(string)
    lst[i], lst[j] = lst[j], lst[i]
    return "".join(lst)


def genetic_algorithm(n):
    population = generate_initial_population(n)
    population = sort_by_fitness(population)

    for _ in range(50):
        parents = select_parents(population)
        children = []

        for i in range(0, len(parents), 2):
            child1, child2 = crossover(parents[i], parents[i + 1])
            child1 = mutate(child1)
            child2 = mutate(child2)
            children.extend([child1, child2])

        population = sort_by_fitness(children)

        best = population[0]
        if fitness(best) == 0:
            return best

    return None

genetic_algorithm(30)