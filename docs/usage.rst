Using SPGA
==========

This document explains how to use the SPGA library to solve optimization problems with genetic algorithms.

Basic Setup
-----------

First, import the necessary components:

.. code-block:: python

   from spga import (
       genetic_algorithm,
       Solution,
       create_genetic_operations,
       tournament_selection,
       mean_crossover,
       uniform_mutation
   )

Example 1: Single-Variable Function Optimization
------------------------------------------------

Optimizing the function f(x) = sin(x) * x² in the interval [0, 12.55]:

.. code-block:: python

   import math
   import random

   # Problem configuration
   SEARCH_SPACE = (0, 12.55)
   POPULATION_SIZE = 100
   NUM_ITERATIONS = 100

   def population_generator(**kwargs):
       return [Solution(
           solution=[random.uniform(*SEARCH_SPACE)],
           fitness=None
       ) for _ in range(kwargs['population_size'])]

   def evaluate_fitness(individual, **kwargs):
       x = individual.solution[0]
       return math.sin(x) * (x ** 2)

   # Algorithm configuration
   ga_args = {
       'population_size': POPULATION_SIZE,
       'num_iterations': NUM_ITERATIONS,
       'optimization': 'max',
       'tournament_size': 3,
       'mutation_probability': 0.15,
       'crossover_probability': 0.8,
       'max_its_with_enhancing': 20
   }

   genetic_ops = create_genetic_operations(
       selection_func=tournament_selection,
       crossover_func=mean_crossover,
       mutation_func=uniform_mutation
   )

   # Execution
   result = genetic_algorithm(
       population_generator=population_generator,
       evaluate_fitness=evaluate_fitness,
       genetic_operations=genetic_ops,
       args=ga_args,
       verbose=True,
       plot=True
   )

Example 2: Polynomial Fitting (Multi-Variable Optimization)
-----------------------------------------------------------

Fitting a polynomial to a dataset using Mean Absolute Error (MAE):

.. code-block:: python

   # Configuration
   SOL_SIZE = 10  # Polynomial degree + 1
   SEARCH_SPACE = [-1, 1]
   POPULATION_SIZE = 100
   NUM_ITERATIONS = 500

   # Sample data (x, y)
   data = [[-3,-329.24], [-2.5,-18.696777], ...] 

   def population_generator(**kwargs):
       return [Solution(
           solution=[random.uniform(*SEARCH_SPACE) for _ in range(SOL_SIZE)],
           fitness=None
       ) for _ in range(kwargs['population_size'])]

   def evaluate_fitness(individual, **kwargs):
       # MAE calculation
       data = kwargs['data']
       fit = 0
       for x, y in data:
           pred = sum(coeff * (x**i) for i, coeff in enumerate(individual.solution))
           fit += abs(y - pred)
       return fit/len(data)

   # Custom operators
   def custom_tournament(population, **kargs):
       # Custom tournament selection implementation
       ...

   def uniform_crossover(parent1, parent2, **kargs):
       # Uniform crossover implementation
       ...

   def constant_mutation(individual, **kargs):
       # Constant-value mutation
       ...

   # Configuration with custom operators
   genetic_ops = create_genetic_operations(
       selection_func=custom_tournament,
       crossover_func=uniform_crossover,
       mutation_func=constant_mutation
   )

   ga_args = {
       'population_size': POPULATION_SIZE,
       'num_iterations': NUM_ITERATIONS,
       'optimization': 'min',
       'data': data,
       # ... other parameters
   }

   result = genetic_algorithm(
       population_generator=population_generator,
       evaluate_fitness=evaluate_fitness,
       genetic_operations=genetic_ops,
       args=ga_args
   )

Core Components
---------------

1. **Solution**: Class representing an individual solution
   - ``solution``: Solution representation (list, value, etc.)
   - ``fitness``: Fitness value (calculated by evaluate_fitness)
   - ``modified``: Flag to control re-evaluations

2. **genetic_algorithm**: Main function that runs the algorithm
   - Key parameters:
   * ``population_generator``: Function that creates initial population
   * ``evaluate_fitness``: Evaluation function
   * ``genetic_operations``: Genetic operators pipeline
   * ``args``: Configuration parameters

3. **create_genetic_operations**: Factory to create operations pipeline
   - Allows customization of selection, crossover and mutation

Configurable Parameters
-----------------------

Main parameters in the ``args`` dictionary:

- ``population_size``: Population size
- ``num_iterations``: Maximum number of iterations
- ``optimization``: 'max' or 'min' (maximize or minimize)
- ``tournament_size``: Tournament size for selection
- ``mutation_probability``: Mutation probability (0-1)
- ``crossover_probability``: Crossover probability (0-1)
- ``max_its_with_enhancing``: Early stopping after N iterations without improvement

Customization Guide
-------------------

To create custom genetic operators:

1. **Selection Functions**:
   - Must accept a population and return a new population
   - Use kwargs to access algorithm parameters

2. **Crossover Functions**:
   - Accept two parent Solutions
   - Return two child Solutions
   - Set modified=True on new solutions

3. **Mutation Functions**:
   - Accept one Solution
   - Return modified Solution
   - Set modified=True if changes were made

Visualization
-------------

Enable plots by setting ``plot=True`` in ``genetic_algorithm()``:

.. code-block:: python

   result = genetic_algorithm(
       ...,
       plot=True  # Shows fitness progression plot
   )

The plot displays:
- Mean population fitness
- Fitness standard deviation
- Elite individual fitness