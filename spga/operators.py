import random
from copy import deepcopy
from typing import List, Callable
from .types import Solution

def tournament_selection(population: List[Solution], 
                        **kargs) -> Solution:
    """
    Tournament selection with support for maximization/minimization
    
    Args:
        population: Current population of solutions
        tournament_size: Number of individuals in each tournament
        optimization: 'max' to select highest fitness or 'min' for lowest
        
    Returns:
        List[Solution]: New population after selection
    """
    optimization = kargs['optimization']
    tournament_size = kargs.get('tournament_size', 3)
    new_population = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        if optimization == 'max':
            selected = deepcopy(max(tournament, key=lambda x: x.fitness))
        else:
            selected = deepcopy(min(tournament, key=lambda x: x.fitness))
        new_population.append(selected)
    return new_population

def single_point_crossover(parent1: Solution, 
                          parent2: Solution, 
                          **kwargs) -> Solution:
    """
    Single-point crossover for list-based solutions
    
    Args:
        parent1: First parent solution
        parent2: Second parent solution
        
    Returns:
        Tuple[Solution, Solution]: Two child solutions
        
    Raises:
        ValueError: If parents have invalid length for crossover
    """
    if len(parent1.solution) < 2:
        raise ValueError("Parents must have at least 2 genes for crossover.")
    
    point = random.randint(1, len(parent1.solution)-1)
    child1 = parent1.solution[:point] + parent2.solution[point:]
    child2 = parent2.solution[:point] + parent1.solution[point:]   
    
    if len(child1) != len(parent1.solution) or len(child2) != len(parent2.solution):
        raise ValueError("Crossover resulted in invalid child length.")
    return Solution(child1, None, modified=True), Solution(child2, None, modified=True)

def mean_crossover(parent1: Solution,
                   parent2: Solution, 
                   **kwargs) -> Solution:
    """
    Arithmetic mean crossover for continuous solutions
    
    Args:
        parent1: First parent solution
        parent2: Second parent solution
        
    Returns:
        Tuple[Solution, Solution]: Two child solutions
        
    Raises:
        ValueError: If parents have different lengths
    """
    if len(parent1.solution) != len(parent2.solution):
        raise ValueError("Parents must have the same number of genes for crossover.")
    
    child1 = [(x + y) / 2 for x, y in zip(parent1.solution, parent2.solution)]
    child2 = [(x + y) * 2 for x, y in zip(parent1.solution, parent2.solution)]
    return Solution(child1, None, modified=True), Solution(child2, None, modified=True)

def uniform_mutation(individual: Solution, 
                    mutation_rate: float = 0.1, 
                    value_range: tuple = (0, 1),
                    **kwargs) -> Solution:
    """
    Uniform mutation for continuous values
    
    Args:
        individual: Solution to mutate
        mutation_rate: Probability of mutation per gene
        value_range: Tuple specifying (min, max) possible values
        
    Returns:
        Solution: Mutated solution
    """
    mutated = [
        random.uniform(*value_range) if random.random() < mutation_rate else x
        for x in individual.solution
    ]
    return Solution(mutated, None, modified=True)

def permutation_mutation(individual: Solution,
                        mutation_rate: float = 0.1,
                        **kwargs) -> Solution:
    """
    Swap mutation for combinatorial problems
    
    Args:
        individual: Solution to mutate
        mutation_rate: Probability of mutation occurring
        
    Returns:
        Solution: Mutated solution (or original if no mutation occurred)
    """
    if random.random() > mutation_rate or len(individual.solution) < 2:
        return individual
        
    idx1, idx2 = random.sample(range(len(individual.solution)), 2)
    mutated = deepcopy(individual.solution)
    mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
    return Solution(mutated, None, modified=True)

def create_genetic_operations(
    selection_func: Callable = tournament_selection,
    crossover_func: Callable = single_point_crossover,
    mutation_func: Callable = uniform_mutation,
    elitism: bool = True
) -> Callable:
    """
    Factory function to create customizable genetic operations pipeline
    
    Args:
        selection_func: Selection operator function
        crossover_func: Crossover operator function
        mutation_func: Mutation operator function
        elitism: Whether to preserve best individual
        
    Returns:
        Callable: Configured genetic operations function
    """
    def genetic_operations(population: List[Solution], 
                          elite: Solution, 
                          **kwargs: dict) -> List[Solution]:
        """
        Executes genetic operations pipeline
        
        Args:
            population: Current generation solutions
            elite: Best solution from previous generation
            args: Algorithm parameters dictionary containing:
                - optimization: 'max' or 'min'
                - population_size: Target population size
                - crossover_probability: Chance of crossover (0-100)
                - mutation_probability: Chance of mutation (0-1)
                
        Returns:
            List[Solution]: New generation of solutions
        """

        new_population = selection_func(population, **kwargs)
        pop_size = kwargs['population_size']

        # Crossover
        for i in range(0, pop_size, 2):
            if random.randint(0, 100) < kwargs.get('crossover_probability',0.8):
                parent1 = new_population[i]
                parent2 = new_population[i + 1] if i + 1 < pop_size else new_population[i]
                
                child1, child2 = crossover_func(parent1, parent2, **kwargs)
                child1.modified = True
                child2.modified = True 
                new_population[i] = child1
                if i + 1 < pop_size:
                    new_population[i + 1] = child2
            
        # Mutation
        for i in range(len(new_population)):
            if random.random() < kwargs.get('mutation_probability', 0.1):
                child = mutation_func(new_population[i], **kwargs)
                child.modified = True
                new_population[i] = child
        
        return new_population[:pop_size]  # Ensure correct population size
    
    return genetic_operations

# Preconfigured operations
default_genetic_operations = create_genetic_operations()
combinatorial_operations = create_genetic_operations(
    mutation_func=permutation_mutation
)