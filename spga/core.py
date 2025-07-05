import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from .types import Solution, GeneticAlgorithmResult

import matplotlib.pyplot as plt
import numpy as np
from IPython import get_ipython
from PIL import Image

def plot_with_std(x, means, std_devs, elite_fitness, log=False):
    """
    Visualizes fitness progression with mean, standard deviation and elite fitness.
    Automatically adapts to execution environment (Jupyter notebook or terminal).
    
    Parameters:
        x (array-like): Iteration numbers for x-axis
        means (array-like): Mean fitness values per generation
        std_devs (array-like): Standard deviations of fitness per generation
        elite_fitness (array-like): Best fitness values per generation
        log (bool): Whether to use logarithmic y-scale
        
    Behavior:
        - In Jupyter: Displays interactive plot
        - In terminal: Saves plot as temporary image and displays it
    """
    # Convert inputs to numpy arrays for easier manipulation
    x = np.array(x)
    means = np.array(means)
    std_devs = np.array(std_devs)

    # Calculate upper and lower bounds for standard deviations
    upper = means + std_devs
    lower = means - std_devs

    # Create the plot with appropriate backend
    is_notebook = get_ipython() is not None
    
    if is_notebook:
        # Configuración para Jupyter Notebook
        plt.figure(figsize=(10, 6))
    else:
        # Configuración para terminal (non-interactive backend)
        plt.switch_backend('Agg')
        plt.figure(figsize=(10, 6))

    # Plot the mean fitness as a solid line
    plt.plot(x, means, label="Mean Fitness", color="blue", linestyle="-")

    # Plot the standard deviations as dashed lines
    plt.plot(x, upper, label="Mean + Std Dev", color="red", linestyle="--")
    plt.plot(x, lower, label="Mean - Std Dev", color="green", linestyle="--")

    # Plot the best fitness values (elite fitness)
    plt.plot(x, elite_fitness, label="Elite Fitness", color="orange", linestyle="-")

    # Apply logarithmic scale if specified
    if log:
        plt.yscale("log")

    # Add labels, legend, and title
    plt.xlabel("Iterations")
    plt.ylabel("Average Fitness")
    plt.legend()
    plt.title("Mean and Standard Deviation of Fitness Scores")

    # Display the plot appropriately for the environment
    if is_notebook:
        plt.show()  # Mostrar interactivo en Jupyter
    else:
        # En terminal: guardar a archivo y mostrar mensaje
        import os
        import tempfile
        import time
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"ga_plot_{timestamp}.png"
        save_path = os.path.join(tempfile.gettempdir(), filename)
        
        plt.savefig(save_path, dpi=100)
        plt.close()
        
        img = Image.open(save_path)
        img.show()


def genetic_algorithm(
    population_generator,
    evaluate_fitness,
    genetic_operations,
    args,
    verbose=False,
    plot=False
) -> GeneticAlgorithmResult:
    """
    Core genetic algorithm implementation with elitism and early stopping.
    
    Parameters:
        population_generator (callable): 
            Function that generates initial population. Signature: (args) -> List[Solution]
        evaluate_fitness (callable):
            Fitness function. Signature: (Solution, args) -> float
        genetic_operations (callable):
            Function applying selection, crossover and mutation. Signature: (population, elite, args) -> List[Solution]
        args (dict):
            Algorithm parameters including:
            - population_size (int)
            - num_iterations (int)
            - optimization ('max' or 'min')
            - max_its_with_enhancing (int)
            - [optional] early_stop (bool)
            - [optional] log (bool)
        verbose (bool): 
            Whether to print progress information
        plot (bool): 
            Whether to generate fitness progression plot
            
    Returns:
        GeneticAlgorithmResult: 
            Named tuple containing:
            - population: Final generation
            - best_solution: Best solution found
            - best_fitness: Fitness of best solution
            
    Note:
        Implements elitism (preserves best solution) and early stopping when:
        - Maximum iterations reached OR
        - No improvement for max_its_with_enhancing generations OR
        - Early stop condition met (fitness=0 for minimization)
    """
    its_with_enhancing = 0
    max_its_with_enhancing = args['max_its_with_enhancing']
    # Helper function to get the best individual based on optimization type
    def get_best(population, key, args):
        if args['optimization'] == 'max':
            return max(population, key=key)
        elif args['optimization'] == 'min':
            return min(population, key=key)
        else:
            raise ValueError("Optimization type must be 'max' or 'min'.")

    # Generate initial population
    population = population_generator(**args)

    # Evaluate the fitness of each individual in the population
    fit_means = []
    fit_stds = []
    elite_fitnesses = []

    for individual in population:
        individual.fitness = evaluate_fitness(individual, **args)

    # Get the elite (best individual) from the initial population
    elite = deepcopy(get_best(population, lambda x: x.fitness, args))

    iteration = 0
    # Main loop of the genetic algorithm
    while iteration < args['num_iterations'] and not (
        args.get('early_stop', False) and
        args['optimization'] == 'min' and
        elite.fitness == 0
    ):
        if verbose:
            print(f"Iteration {iteration + 1}")
            print(f"Best fitness: {elite.fitness}")

        # Apply genetic operations to generate the new population
        population = genetic_operations(population, elite, **args)

        # Evaluate the fitness of modified individuals
        for individual in population:
            if individual.modified:
                individual.modified = False
                individual.fitness = evaluate_fitness(individual, **args)

        # Update the elite individual
        elite_fit = elite.fitness
        elite = deepcopy(get_best(population+[elite], lambda x: x.fitness, args))

        # Collect statistics for plotting
        fitness_values = list(map(lambda x: x.fitness, population))
        fit_means.append(np.mean(fitness_values))
        fit_stds.append(np.std(fitness_values))
        elite_fitnesses.append(elite.fitness)

        iteration += 1
        if elite.fitness == elite_fit:
          its_with_enhancing += 1
        else:
          
          its_with_enhancing = 0
        if its_with_enhancing == max_its_with_enhancing:
          break
    # Print the final results if verbose mode is enabled
    if verbose:
        print(f"Best solution: {elite.solution}")
        print(f"Best fitness: {elite.fitness}")

    # Plot the fitness progression if plotting is enabled
    if plot:
        plot_with_std(range(1, iteration + 1), fit_means, fit_stds, elite_fitnesses, log=args.get('log', False))

    # Return the final population, best solution, and best fitness value
    return GeneticAlgorithmResult(
        population=population,
        best_solution=elite.solution,
        best_fitness=elite.fitness
    )