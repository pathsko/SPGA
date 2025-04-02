# SPGA: Simple and Personalizable Genetic Algorithm

[![PyPI version](https://img.shields.io/pypi/v/spga.svg)](https://pypi.org/project/spga/)
[![Python versions](https://img.shields.io/pypi/pyversions/spga.svg)](https://pypi.org/project/spga/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Overview
SPGA is a lightweight Python framework for building customizable genetic algorithms. Designed for education and production, it offers:
- Full control over genetic operations
- Clean generational workflow
- Built-in progress visualization
- Minimal dependencies (NumPy + Matplotlib)

```bash
pip install spga
```

## Quickstart
```python
from spga import GeneticAlgorithm, DefaultOperators
import random

# 1. Define chromosome representation
def create_solution(params):
    return [random.uniform(-5, 5) for _ in range(3)]  # 3D solution

# 2. Create fitness function
def evaluate(solution, params):
    return sum(x**2 for x in solution)  # Minimize sphere function

# 3. Configure and run
results = GeneticAlgorithm(
    population_generator=create_solution,
    fitness_function=evaluate,
    operators=DefaultOperators(),
    params={
        'population_size': 30,
        'generations': 50,
        'optimization': 'min'
    }
).run()

print(f"Best solution: {results.best_solution}")
print(f"Fitness: {results.best_fitness:.4f}")

```

## Key Features

### Custom Genetic Operators
```python
from spga import BaseOperator

class CustomOperators(BaseOperator):
    def selection(self, population, params):
        # Tournament selection
        candidates = random.sample(population, 3)
        return max(candidates, key=lambda x: x.fitness)
    
    def crossover(self, p1, p2, params):
        # Arithmetic recombination
        return [(a+b)/2 for a,b in zip(p1.solution, p2.solution)]
    
    def mutation(self, solution, params):
        # Gaussian mutation
        return [g + random.gauss(0, 0.1) for g in solution.solution]
```

## Progress Tracking