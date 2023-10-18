import math
import random


def fitness(state):
    n = len(state)
    clashes = 0

    # Check diagonals
    for i in range(n):
        for j in range(i + 1, n):
            if abs(state[i] - state[j]) == j - i:
                clashes += 1

    # Check rows
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]:
                clashes += 1

    # Fitness is 0 when there are no clashes (solution found)
    if clashes == 0:
        return 0

    return clashes


def sort_by_fitness(population):
    fitness_vals = []
    for state in population:
        fitness_vals.append(fitness(state))

    sorted_list = [x for _, x in sorted(zip(fitness_vals, population))]
    return sorted_list


def generate_initial_population(n):
    population = []
    pop_size = (n * n) * math.ceil(math.log(n))

    while len(population) < pop_size:
        state = list(range(n))
        random.shuffle(state)

        if state not in population:
            population.append(state)

    return population


def select_breeding_pool(population, n):
    breeding_pool = []
    pop_size = len(population)
    breeding_pool_size = pop_size // 10

    # Normalize fitnesses to range [0, 1]
    fitness_sums = sum([((n * (n - 1)) - fitness(state)) for state in population])
    fitness_norm = [(n * (n - 1) - fitness(state)) for state in population]

    # Select states based on normalized fitness probability
    for i in range(breeding_pool_size):
        state = random.choices(population, weights=fitness_norm)[0]
        breeding_pool.append(state)

    return breeding_pool


def get_converted_fitness(state, size):
    return (size * (size - 1)) - fitness(state)


def get_breeding_parents(breeding_pool):
    parents = []
    fitness_norm = [(get_converted_fitness(state, int(question))) for state in breeding_pool]
    while len(parents) < 6:
        state = random.choices(breeding_pool, weights=fitness_norm)[0]
        if state not in parents:
            parents.append(state)

    # Arrange into pairs
    parent_pairs = [(parents[0], parents[1]),
                    (parents[2], parents[3]),
                    (parents[4], parents[5])]

    return parent_pairs


def crossover(parent1, parent2):
    child = []
    for i in range(len(parent1)):
        if random.random() < 0.5:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child


def mutate(child):
    for i in range(len(child)):
        if random.random() < 0.05:
            j = random.randint(0, len(child) - 1)
            child[i], child[j] = child[j], child[i]
    return child


question = input("Enter the number of queens: ")


def run_algorithm():
    initialPop = generate_initial_population(int(question))
    initialPop = sort_by_fitness(initialPop)

    breeding_pool = select_breeding_pool(initialPop, int(question))
    breeding_pool = sort_by_fitness(breeding_pool)

    breed_size = len(breeding_pool)

    print("Initial population:")
    for state in initialPop:
        print(state, fitness(state))

    for i in range(50):
        print("Breeding pool:")
        for state in breeding_pool:
            print(state, fitness(state))

        parents = get_breeding_parents(breeding_pool)
        print("Parents:")
        for pair in parents:
            print(pair)

        # Perform 50 crossover and mutation attempts
        children = []
        print("Children:")
        for i in range(50):
            for pair in parents:
                child = crossover(pair[0], pair[1])
                child = mutate(child)
                if fitness(child) == 0:
                    print("Solution found!")
                    print(child)
                    return child
                if child not in children:
                    children.append(child)

        children = sort_by_fitness(children)
        for child in children:
            print(child, fitness(child))

        for child in children:
            if child not in breeding_pool:
                breeding_pool.append(child)

        breeding_pool = sort_by_fitness(breeding_pool)
        breeding_pool = breeding_pool[:breed_size]

        print("New breeding pool:")
        for state in breeding_pool:
            print(state, fitness(state))
    return -1


x = run_algorithm()
while x == -1:
    x = run_algorithm()
