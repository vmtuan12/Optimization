from random import choices, randint, randrange, random
from typing import List, Callable, Tuple

Solution = List[int]
SolutionSet = List[Solution]

# take nothing, spit out solution
SolutionSetFunc = Callable[[], SolutionSet]
# take Solution and spit out a value number
FitnessFunc = Callable[[Solution], int]
# take solutionSet and fitness function, select 2 solutions to be the parents of the next generation
SelectionFunc = Callable[[SolutionSet, FitnessFunc], Tuple[Solution, Solution]]
# take 2 genomes and return 2 new genomes after crossing
CrossoverFunc = Callable[[Solution, Solution], Tuple[Solution, Solution]]
# take 1 genome and sometimes return a modified one
MutationFunc = Callable[[Solution], Solution]

# generate a solution randomly
def generate_solution(length: int) -> Solution:
    return choices([0, 1], k=length)

# generate solution until solution has desired size
def generate_solutionSet(size: int, solution_length: int) -> SolutionSet:
    return [generate_solution(solution_length) for _ in range(size)]

# crossover operator
def crossover(a: Solution, b: Solution) -> Tuple[Solution, Solution]:
    if len(a) != len(b):
        raise ValueError("Solution a and b must be of same length")

    length = len(a)
    if length < 2:
        return a, b

    # randomly choose an index to cut the solution
    p = randint(1, length - 1)
    # combine first half of solution a and second half of solution b
    # the same goes for b and a
    return a[0:p] + b[p:], b[0:p] + a[p:]

# mutation operator
def mutation(solution: Solution, num: int = 1, probability: float = 0.5) -> Solution:
    for _ in range(num):
        index = randrange(len(solution))
        # change the item of selected solution index if random <= probability
        solution[index] = solution[index] if random() > probability else abs(solution[index] - 1)
    return solution

# selection operator
# solutions with higher fitness are more likely to be chosen
def selection_pair(solutionSet: SolutionSet, fitness_func: FitnessFunc) -> SolutionSet:
    return choices(
        population=solutionSet,
        weights=[fitness_func(gene) for gene in solutionSet],
        k=2 # draw twice from population to get a pair
    )

# main function
def run_evolution(
        solutionSet_func: SolutionSetFunc,
        fitness_func: FitnessFunc,
        # end condition, if the fitness of the best solution exceeds this limit, we reach our goal
        fitness_limit: int,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = crossover,
        mutation_func: MutationFunc = mutation,
        # maximum generations the evolution runs if it has not reached the fitness limit before that
        generation_limit: int = 100) -> Tuple[SolutionSet, int]:

    # new solutionSet
    solutionSet = solutionSet_func()

    for i in range(generation_limit):
        # sort solutionSet by fitness
        solutionSet = sorted(solutionSet, key=lambda solution: fitness_func(solution), reverse=True)

        # check whether we have reached the fitness limit
        if fitness_func(solutionSet[0]) >= fitness_limit:
            break
        
        # keep top 2 solution for the next generation
        next_generation = solutionSet[0:2]

        # pick 2 parents and get 2 solutions everytime -> loop len/2
        # we have already copied the top 2 solutions from the last generation -> save 1 loop
        for j in range(int(len(solutionSet) / 2) - 1):
            parents = selection_func(solutionSet, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        solutionSet = next_generation
        
    # sort the last time before returning
    solutionSet = sorted(solutionSet, key=lambda solution: fitness_func(solution), reverse=True)
    return solutionSet, i
