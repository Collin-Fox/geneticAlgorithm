import random

import numpy as np

word_to_number = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "10": "A",
    "11": "B",
    "12": "C",
    "13": "D",
    "14": "E",
    "15": "F",
    "16": "G",
    "17": "H",
    "18": "I",
    "19": "J",
    "20": "K",
    "21": "L",
    "22": "M",
    "23": "N",
    "24": "O",
    "25": "P",
    "26": "Q",
    "27": "R",
    "28": "S",
    "29": "T",
    "30": "U",
    "31": "V",
    "32": "W",
    "33": "X",
    "34": "Y",
    "35": "Z",
    "36": "!",
    "37": "@",
    "38": "#",
    "39": "$",
    "40": "%",
    "41": "^",
    "42": "&",
    "43": "*",
    "44": "(",
    "45": ")",
    "46": "-",
    "47": "_",
    "48": "+",
    "49": "=",
    "50": "["

}
number_to_word = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "A": "10",
    "B": "11",
    "C": "12",
    "D": "13",
    "E": "14",
    "F": "15",
    "G": "16",
    "H": "17",
    "I": "18",
    "J": "19",
    "K": "20",
    "L": "21",
    "M": "22",
    "N": "23",
    "O": "24",
    "P": "25",
    "Q": "26",
    "R": "27",
    "S": "28",
    "T": "29",
    "U": "30",
    "V": "31",
    "W": "32",
    "X": "33",
    "Y": "34",
    "Z": "35",
    "!": "36",
    "@": "37",
    "#": "38",
    "$": "39",
    "%": "40",
    "^": "41",
    "&": "42",
    "*": "43",
    "(": "44",
    ")": "45",
    "-": "46",
    "_": "47",
    "+": "48",
    "=": "49",
    "[": "50"

}

"""
Genetic algorithm used to solve N queens problem
"""


def fitness(n_queen):
    # Initialize the number of conflicts to 0.
    num_conflicts = 0

    # Iterate over all queens.
    for i in range(len(n_queen)):
        # Check if the current queen is attacking any other queen.
        for j in range(i + 1, len(n_queen)):
            # If the two queens are in the same row, column, or diagonal, then they are attacking each other.
            if n_queen[i] == n_queen[j] or abs(i - j) == abs(
                    int(number_to_word[n_queen[i]]) - int(number_to_word[n_queen[j]])):
                num_conflicts += 1

    return num_conflicts


def generate_initial_population(n: int):
    """

    :param population_size:
    :param n: integer of how many queens we have IE n = 7 -> 7 Queens problem, string length is 7

    Call to fitness function after population is generated and sort by fitness
    THE LOWER THE FITNESS THE BETTER THE STATE IS

    :return: Set(no repetitions of strings) of Strings that represent a single N queens problem state.
    """
    # Create the initial string for N queens
    initial = ""
    population_size = int((n * n) * np.ceil(np.log2(n)))
    for i in range(1, n + 1):
        initial += str(word_to_number[str(i)])

    print(initial)
    # Create a set of permutations
    """
    from itertools import permutations
    perms = [''.join(p) for p in permutations(initial)]
    perms = set(perms)
    """

    population_list = []
    while len(population_list) < population_size:
        word = ''.join(random.sample(initial, len(initial)))
        if word not in population_list:
            population_list.append(word)

    # Selecting N random elements from the set for initial population
    # population_list = random.sample(list(initial), population_size)

    return population_list


def sort_by_fitness(population):
    """

    :param population:
    :return:
    """
    population.sort(key=fitness)
    return population


def get_total_fitness(population):
    return sum([fitness(state) for state in population])


def choose_parents(population):
    total = get_total_fitness(population)
    breeding_size = int(len(population) / 10)
    breeding_set = []
    while len(breeding_set) < breeding_size:
        for state in population:
            fit = fitness(state)
            probability = (len(state) * (len(state) - 1) - fit)
            random_gen = random.randint(0, total)
            if len(set(breeding_set)) < breeding_size and random_gen <= probability:
                breeding_set.append(state)
    return set(breeding_set)


def get_breeding_pairs(breeding_set):
    total_fitness = get_total_fitness(breeding_set)
    breeding_pairs_list = []
    while len(breeding_pairs_list) < 6:
        for state in breeding_set:
            probability = (len(state) * (len(state) - 1)) - fitness(state)
            random_gen = random.randint(1, total_fitness)
            if len(set(breeding_pairs_list)) < 6 and random_gen <= probability:
                breeding_pairs_list.append(state)

    breeding_pairs = [(breeding_pairs_list[0], breeding_pairs_list[1]),
                      (breeding_pairs_list[2], breeding_pairs_list[3]),
                      (breeding_pairs_list[4], breeding_pairs_list[5])]
    return breeding_pairs


def crossover(breeding_pairs):
    i = -1
    j = -1

    # Breeding pairs
    a, b = breeding_pairs

    # Randomly select two indices
    while i == j:
        i = random.randint(0, len(a) - 1)
        j = random.randint(0, len(a) - 1)

    # Make sure i < j
    min_index = min(i, j)
    max_index = max(i, j)

    # Get the substrings
    p0_retained = a[min_index:max_index]
    p0_left = a[:min_index]
    p0_right = a[max_index:]
    p0_replaced = p0_left + p0_right

    # Replace the substring in the other parent
    holder = b
    p1_retained = ""
    p1_replaced = ""

    # Replace the substring in the other parent
    for letter in holder:
        if letter in p0_retained:
            p1_retained += letter
        else:
            p1_replaced += letter
            holder = holder.replace(letter, "?")

    # Replace the positions needed to replace w ?'s
    replaceHolder = ""
    for i in range(0, min_index):
        replaceHolder += "?"

    p0_retained = replaceHolder + p0_retained
    for i in range(max_index, len(a)):
        p0_retained += "?"

    # Replace the positions in p1 needed to replace w p0s extras
    for letter in holder:
        if letter == "?":
            holder = holder.replace("?", p0_replaced[0], 1)
            p0_replaced = p0_replaced[1:]

    # Replace the positions in p0 needed to replace w p1s extras
    for letter in p0_retained:
        if letter == "?":
            p0_retained = p0_retained.replace("?", p1_replaced[0], 1)
            # print(p0_retained)
            p1_replaced = p1_replaced[1:]

    child1 = p0_retained
    child2 = holder

    return child1, child2


def mutate(child):
    for i in range(len(child)):
        # Max Length of Child aka number of Ns
        max_len = len(child[i])
        # Randomly select a number between 0 and 100
        # If the number is less than 5% then mutate
        if random.randint(0, 100) <= 5:
            print("Mutating: ", child[i], "to:")
            a = -1
            b = -1
            while a == b:
                a = random.randint(0, max_len - 1)
                b = random.randint(0, max_len - 1)
            # Swap char a with char b

            charmin = child[i][min(a, b)]
            charmax = child[i][max(a, b)]

            child[i] = child[i].replace(charmax, charmin)
            child[i] = child[i].replace(charmin, charmax, 1)

            print(child[i])

    return child


def run_genetic_algorithm(n):
    x = generate_initial_population(n)
    x = sort_by_fitness(x)
    breeding_set = sort_by_fitness(list(choose_parents(x)))
    counter = 0
    print("Initital Population")
    for state in breeding_set:
        print(state, "Fitness", fitness(state))

    while counter < 50:
        breeding_pairs = get_breeding_pairs(breeding_set)
        print(breeding_pairs)
        breeding_children = []

        while len(breeding_children) < 50:
            for pair in breeding_pairs:
                child1, child2 = crossover(pair)
                mut_list = [child1, child2]
                mut_list = mutate(mut_list)
                child1 = mut_list[0]
                child2 = mut_list[1]
                if len(breeding_children) < 50:
                    breeding_children.append(child1)
                if len(breeding_children) < 50:
                    breeding_children.append(child2)

            breeding_children = set(breeding_children)
            breeding_children = list(breeding_children)

        # Send Children through mutate function
        # breeding_children = mutate(breeding_children)
        breeding_children = sort_by_fitness(breeding_children)

        for state in breeding_children:
            print(state, "Fitness", fitness(state))
            if fitness(state) == 0:
                print("N Queens Solution Found", state)
                return state

        counter += 1
        print("Generation: ", counter)
        breeding_set = breeding_children
    return False


n = input("Enter and integer up to 35 for the N queens problem")

x = run_genetic_algorithm(int(n))
while x is False:
    print("Not Found, generating new initial population")
    x = run_genetic_algorithm(int(n))
