from dataclasses import dataclass
from typing import Any, List
import numpy as np
import copy
@dataclass
class Solution:
    """Representa una solución en el algoritmo genético."""
    solution: Any
    fitness: float = None
    modified: bool = True
    def __copy__(self):
        return type(self)(
            solution=self.solution,
            fitness=self.fitness,
            modified=self.modified
        )

    def __deepcopy__(self, memo):
        return type(self)(
            solution=copy.deepcopy(self.solution, memo),
            fitness=self.fitness,
            modified=self.modified
        )

class GeneticAlgorithmResult:
    """Contenedor para los resultados del algoritmo."""
    def __init__(self, population, best_solution, best_fitness):
        self.population = population
        self.best_solution = best_solution
        self.best_fitness = best_fitness