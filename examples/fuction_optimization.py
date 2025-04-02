"""
Genetic Algorithm Function Optimization Example

Objective: Maximize the function f(x) = sin(x) * x^2 in the interval [0, 12.55]
"""
import math
import random
import numpy as np
from spga import (
    genetic_algorithm,
    Solution,
    create_genetic_operations,
    tournament_selection,
    mean_crossover,
    uniform_mutation
)

# 1. Problem configuration
SEARCH_SPACE = (0, 12.55)  # Search space boundaries
POPULATION_SIZE = 100
NUM_ITERATIONS = 100

def population_generator(args):
    """
    Generates initial population with random solutions within search space.
    
    Parameters:
        args (dict): Algorithm parameters containing:
            - population_size (int): Number of individuals in population
            
    Returns:
        list[Solution]: List of Solution objects with random values
    """
    return [Solution(
        solution=[random.uniform(*SEARCH_SPACE)],
        fitness=None
    ) for _ in range(args['population_size'])]

def evaluate_fitness(individual, args):
    """
    Evaluates fitness of an individual solution.
    
    Parameters:
        individual (Solution): Solution to evaluate
        args (dict): Additional parameters (unused in this case)
        
    Returns:
        float: Fitness value (0 for invalid solutions, sin(x)*x² otherwise)
    """
    x = individual.solution[0]
    if x > SEARCH_SPACE[1] or x < SEARCH_SPACE[0]:
        return 0
    return math.sin(x) * (x ** 2)

# 4. Algorithm configuration
ga_args = {
    'population_size': POPULATION_SIZE,
    'num_iterations': NUM_ITERATIONS,
    'optimization': 'max',  # Optimization direction
    'mutation_probability': 0.15,  # Probability of mutation
    'crossover_probability': 0.8,    # Probability of crossover (disabled here)
    'max_its_with_enhancing': 20  # Max iterations without improvement
}

# Configure genetic operations pipeline
genetic_operations = create_genetic_operations(
    selection_func=tournament_selection,
    crossover_func=mean_crossover,
    mutation_func=uniform_mutation,
    elitism=True
)

# 5. Algorithm execution
result = genetic_algorithm(
    population_generator=population_generator,
    evaluate_fitness=evaluate_fitness,
    genetic_operations=genetic_operations,
    args=ga_args,
    verbose=True,
    plot=True
)

# 6. Results output
print("\n--- FINAL RESULTS ---")
print(f"Best solution found: x = {result.best_solution[0]:.4f}")
print(f"Function value: f(x) = {result.best_fitness:.4f}")

