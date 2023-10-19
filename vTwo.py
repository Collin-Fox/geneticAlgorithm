import math
import random

domainKeyMap = {}
domainValueMap = {}

def generate_domain_dict():
    first_char_code = 48
    last_char_code = 122
    value = 0
    i = first_char_code
    while i <= last_char_code:
        if i == 58:
            i = 65
        if i == 91:
            i = 97
        domainKeyMap[chr(i)] = value
        domainValueMap[value] = chr(i)
        value += 1
        i += 1

def get_domain(size: int) -> str:
    domain = ''
    for i in range(0, size):
        domain += domainValueMap[i]
    return domain

def fitness(state):
    n = len(state)
    clashes = 0

    # Check diagonals
    for i in range(n):
        for j in range(i + 1, n):
            if abs(domainKeyMap[state[i]] - domainKeyMap[state[j]]) == j - i:
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
        state = list(get_domain(n))
        random.shuffle(state)
        state = ''.join(state)

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


def crossover(parent1: str, parent2: str) -> tuple[str, str]:
    size = len(parent1)
    i = 1
    j = 0
    while i >= j:
        i = math.floor(random.uniform(0, size))
        j = math.floor(random.uniform(0, size))

    replacement_dict = {}

    child1 = parent1
    child2 = parent2

    for k in range(i, j + 1):
        child2 = child2.replace(child1[k], "")

    for k in range(0, i):
        replacement_dict[child2[k]] = child1[k]
        child1 = child1[0:k] + child2[k] + child1[k + 1:]

    q = i
    for k in range(j + 1, size):
        replacement_dict[child2[q]] = child1[k]
        child1 = child1[0:k] + child2[q] + child1[k + 1:]
        q += 1

    child2 = parent2
    for k in range(len(child2)):
        if child2[k] in replacement_dict:
            child2 = child2[0:k] + replacement_dict[child2[k]] + child2[k + 1:]

    return child1, child2


def mutate(state: str, mutation_probability: float) -> str:
    mutant = state[:]
    chance = random.uniform(0, 1)

    if mutation_probability < chance:
        transpose_index1 = 0
        transpose_index2 = 0
        while transpose_index1 == transpose_index2:
            transpose_index1 = math.floor(random.uniform(0, len(state)))
            transpose_index2 = math.floor(random.uniform(0, len(state)))
        value1 = state[transpose_index1]
        value2 = state[transpose_index2]
        mutant = mutant[0:transpose_index1] + value2 + mutant[transpose_index1 + 1:]
        mutant = mutant[0:transpose_index2] + value1 + mutant[transpose_index2 + 1:]

    return mutant


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
                childOne, childTwo = crossover(pair[0], pair[1])
                childOne = mutate(childOne, 0.05)
                childTwo = mutate(childTwo, 0.05)
                if fitness(childOne) == 0:
                    print("Solution found!")
                    print(childOne)
                    return childOne
                if fitness(childTwo) == 0:
                    print("Solution found!")
                    print(childTwo)
                    return childTwo
                if childOne not in children:
                    children.append(childOne)
                if childTwo not in children:
                    children.append(childTwo)

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


def print_board(queens_positions: str):
    board = ""
    for i in range(0, int(question)):
        for j in range(0, int(question)):
            if j == domainKeyMap.get(queens_positions[i]):
                board += "Q "
            else:
                board += "- "
        board += "\n"
    print(board)


if __name__ == '__main__':
    generate_domain_dict()
    x = run_algorithm()
    while x == -1:
        x = run_algorithm()
    print_board(x)
