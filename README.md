# SPGA - Simple and Personalizable Genetic Algorithm

[![PyPI version](https://img.shields.io/pypi/v/spga.svg)](https://pypi.org/project/spga/)
[![Python versions](https://img.shields.io/pypi/pyversions/spga.svg)](https://pypi.org/project/spga/)

## Quickstart
```python
from spga import GeneticAlgorithm, DefaultOperators
import random

# 1. Define solution representation
def create_random_solution(params):
    return [random.uniform(-10, 10) for _ in range(params['dimensions'])]

# 2. Implement fitness function
def evaluate(solution, params):
    return sum(x**2 for x in solution)  # Minimize sphere function

# 3. Configure and run
results = GeneticAlgorithm(
    population_generator=create_random_solution,
    fitness_function=evaluate,
    operators=DefaultOperators(),
    params={
        'population_size': 50,
        'generations': 100,
        'dimensions': 5,
        'optimization': 'min'
    }
).run()

print(f"Best solution: {results.best_solution}")
print(f"Fitness: {results.best_fitness}")