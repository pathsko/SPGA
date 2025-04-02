from dataclasses import dataclass
from typing import Any, List
import numpy as np

@dataclass
class Solution:
    """Representa una solución en el algoritmo genético."""
    solution: Any
    fitness: float = None
    modified: bool = True

class GeneticAlgorithmResult:
    """Contenedor para los resultados del algoritmo."""
    def __init__(self, population, best_solution, best_fitness):
        self.population = population
        self.best_solution = best_solution
        self.best_fitness = best_fitness