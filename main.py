import random

def is_valid_state(state):
  """Checks if a given state is valid.

  Args:
    state: A string representing the state of the board.

  Returns:
    True if the state is valid, False otherwise.
  """

  for i in range(len(state)):
    for j in range(i + 1, len(state)):
      if state[i] == state[j] or abs(i - j) == abs(state[i] - state[j]):
        return False
  return True

def generate_state(n):
  """Generates a random state for the N-queens problem.

  Args:
    n: The number of queens.

  Returns:
    A string representing the state of the board.
  """

  state = ""
  for i in range(n):
    state += str(random.randint(0, n - 1))
  return state

def generate_states(n, x):
  """Generates x random states for the N-queens problem.

  Args:
    n: The number of queens.
    x: The number of states to generate.

  Returns:
    A list of strings representing the states of the board.
  """

  states = []
  for i in range(x):
    states.append(generate_state(n))
  return states



if __name__ == "__main__":
  n = int(input("Enter the number of queens: "))
  x = int(input("Enter the number of states to generate: "))

  states = generate_states(n, x)

  for state in states:
    print(state)
