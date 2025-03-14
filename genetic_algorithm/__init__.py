"""
Genetic Algorithm module for the Number Guessing Game.

This module provides the core components for implementing a genetic algorithm
to efficiently search for a secret number through evolutionary methods.
"""

from .individual import Individual
from .population import Population
from .selection import Selection
from .crossover import Crossover
from .mutation import Mutation
from .fitness import FitnessCalculator

__all__ = [
    'Individual', 
    'Population',
    'Selection',
    'Crossover',
    'Mutation',
    'FitnessCalculator'
]