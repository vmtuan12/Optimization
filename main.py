from genetic import Solution, run_evolution, generate_solutionSet
from collections import namedtuple
from typing import List
from functools import partial

Thing = namedtuple('Thing', ['name', 'value', 'weight'])

first_example = [
    Thing('Laptop', 500, 2200),
    Thing('Headphones', 150, 160),
    Thing('Coffee Mug', 60, 350),
    Thing('Notepad', 40, 333),
    Thing('Water Bottle', 30, 200),
]

second_example = [
    Thing('Mints', 5, 25),
    Thing('Socks', 10, 38),
    Thing('Tissues', 15, 80),
    Thing('Phone', 900, 400),
    Thing('Baseball Cap', 100, 70)
] + first_example

# function to determine how good the solution is
def fitness(solution: Solution, things: List[Thing], weight_limit: int) -> int:
    if len(solution) != len(things):
        raise ValueError("solution and things must be of same length")

    weight = 0
    value = 0
    for i, thing in enumerate(things):
        if solution[i] == 1:
            weight += thing.weight
            value += thing.value

            if weight > weight_limit:
                return 0

    # return overall value as long as it is smaller than weight limit
    return value


def from_solution(solution: Solution, things: List[Thing]) -> List[Thing]:
    result = []
    for i, thing in enumerate(things):
        if solution[i] == 1:
            result.append(things[i]) 

    return result

# print functions
def to_string(things: List[Thing]):
    return f"[{', '.join([t.name for t in things])}]"

def value(things: List[Thing]):
    return sum([t.value for t in things])

def weight(things: List[Thing]):
    return sum([p.weight for p in things])

def print_stats(things: List[Thing]):
    print(f"Things: {to_string(things)}")
    print(f"Value: {value(things)}")
    print(f"Weight: {weight(things)}")

solutionSet, generations = run_evolution(
    solutionSet_func=partial(
        generate_solutionSet, size=10, solution_length=len(second_example)
    ),
    fitness_func=partial(
        # remember to adjust appropriate weight_limit
        fitness, things=second_example, weight_limit=3000
    ),
    # remember to adjust appropriate fitness_limit and generation_limit
    fitness_limit=1680,
    generation_limit=2500
)

print("Answer:")
print(f"Best solution set: {solutionSet[0]} | Generations: {generations}")
print_stats(from_solution(solutionSet[0], second_example))

