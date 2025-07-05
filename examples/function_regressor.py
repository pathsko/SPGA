"""
Genetic Algorithm Function Optimization Example

Objective: Maximize the function f(x) = sin(x) * x^2 in the interval [0, 12.55]
"""
import math
import random
import numpy as np
from copy import deepcopy
from spga import (
    genetic_algorithm,
    Solution,
    create_genetic_operations,
    tournament_selection,
    mean_crossover,
    uniform_mutation
)

# 1. Problem configuration
SOL_SIZE = 10 # Search space boundaries
SEARCH_SPACE = [-1, 1]
POPULATION_SIZE = 100
NUM_ITERATIONS = 500

def population_generator(**kwargs):
    """
    Generates initial population with random solutions within search space.
    
    Parameters:
        args (dict): Algorithm parameters containing:
            - population_size (int): Number of individuals in population
            
    Returns:
        list[Solution]: List of Solution objects with random values
    """
    return [Solution(
        solution=[random.uniform(*SEARCH_SPACE) for _ in range(SOL_SIZE)],
        fitness=None
    ) for _ in range(kwargs['population_size'])]

data = [
        [-3,-329.24],
        [ -2.5,-18.696777],
        [-2,8.97],
        [-1.5,0.072636719],
        [-1,-2.86],
        [-0.5,-1.8504492],
        [0,0.25],
        [0.5,5.3464648],
        [1,27.12],
        [1.5,136.69088],
        [2,617.21],
        [2.5,2366.1753],
        [3,7788.22]
        ]

def evaluate_fitness(individual, **kwargs):
    #MAE
    data = kwargs['data']
    fit = 0
    for p in data:
        pred = 0
        for i in range(len(individual.solution)):
            pred += individual.solution[i] * p[0]**i
        fit += abs(p[1] - pred)
    return fit/len(data)
        


#Custom tournament selection
def custom_tournament(population, **kargs):
    optimization = kargs['optimization']
    tournament_size = kargs.get('tournament_size', 3)
    new_population = []
    for i in range(len(population)):
        # Select random individuals for tournament
        tournament = random.sample(population, tournament_size)
        # Get best individual
        if optimization == 'max':
            best = max(tournament, key=lambda x: x.fitness)
        else:
            best = min(tournament, key=lambda x: x.fitness)
        new_population.append(deepcopy(best))
    return new_population

#Custom crossover function
def uniform_crossover(parent1, parent2, **kargs):
    child1,child2 = [],[]
    for i in range(len(parent1.solution)):
        if random.random() < 0.5:
            child1.append(parent1.solution[i])
            child2.append(parent2.solution[i])
        else:
            child1.append(parent2.solution[i])
            child2.append(parent1.solution[i])
    return Solution(solution=child1, fitness=None),Solution(solution=child2, fitness=None)

#Redefined mutation function
def constant_mutation(individual, **kargs):
    for i in range(len(individual.solution)):
        index = random.randint(0, len(individual.solution)-1)
        fact = 1.0
        if random.random() < 0.5:
            fact = -1.0
        individual.solution[index] = individual.solution[index] + fact * 0.01
    return individual

# Configure genetic operations pipeline
genetic_operations = create_genetic_operations(
    selection_func=custom_tournament,
    crossover_func=uniform_crossover,
    mutation_func=constant_mutation,
    elitism=True
)



ga_args = {
    'population_size': POPULATION_SIZE,
    'num_iterations': NUM_ITERATIONS,
    'optimization': 'min',  # Optimization direction
    'tournament_size': 3,  # Number of individuals in tournament
    'mutation_probability': 0.2,  # Probability of mutation
    'crossover_probability': 0.6,    # Probability of crossover (disabled here)
    'max_its_with_enhancing': 100,  # Max iterations without improvement
    'data': data
}
# 5. Algorithm execution
result = genetic_algorithm(
    population_generator=population_generator,
    evaluate_fitness=evaluate_fitness,
    genetic_operations=genetic_operations,
    args=ga_args,
    verbose=False,
    plot=False
)

# 6. Results output
print("\n--- FINAL RESULTS ---")
print(f"Best solution found: {result.best_solution}")
print(f"Function value: f(x) = {result.best_fitness:.4f}")

print(evaluate_fitness(Solution(solution=result.best_solution),data=data))