"""
Selection module for the Genetic Algorithm.

This module provides different selection methods for choosing individuals
from the population for reproduction.
"""

import random
from typing import List, Callable, Any

from .individual import Individual


class Selection:
    """
    Provides different selection methods for the genetic algorithm.
    
    This class implements various selection strategies to choose individuals
    from the population based on their fitness.
    """
    
    @staticmethod
    def tournament_selection(population: List[Individual], tournament_size: int = 3) -> Individual:
        """
        Select an individual using tournament selection.
        
        This method selects a random subset of individuals from the population
        and returns the one with the highest fitness.
        
        Args:
            population: List of individuals to select from
            tournament_size: Number of individuals to include in the tournament
            
        Returns:
            Individual: The selected individual
        """
        # Select random individuals for the tournament
        tournament = random.sample(population, min(tournament_size, len(population)))
        
        # Return the individual with the highest fitness
        return max(tournament, key=lambda ind: ind.fitness)
    
    @staticmethod
    def roulette_wheel_selection(population: List[Individual]) -> Individual:
        """
        Select an individual using roulette wheel selection.
        
        This method selects individuals with probability proportional to their fitness.
        
        Args:
            population: List of individuals to select from
            
        Returns:
            Individual: The selected individual
        """
        # Calculate total fitness
        total_fitness = sum(ind.fitness for ind in population)
        
        # Handle case where all individuals have zero fitness
        if total_fitness == 0:
            return random.choice(population)
        
        # Generate a random value between 0 and the total fitness
        selection_point = random.uniform(0, total_fitness)
        
        # Find the individual at the selection point
        current_sum = 0
        for individual in population:
            current_sum += individual.fitness
            if current_sum >= selection_point:
                return individual
        
        # Fallback (should not reach here)
        return population[-1]
    
    @staticmethod
    def rank_selection(population: List[Individual]) -> Individual:
        """
        Select an individual using rank selection.
        
        This method selects individuals based on their rank in the population
        rather than their absolute fitness, which can help maintain diversity.
        
        Args:
            population: List of individuals to select from
            
        Returns:
            Individual: The selected individual
        """
        # Sort population by fitness (highest first)
        sorted_population = sorted(population, key=lambda ind: ind.fitness, reverse=True)
        
        # Calculate selection weights based on rank
        ranks = list(range(1, len(sorted_population) + 1))
        rank_sum = sum(ranks)
        
        # Select based on rank probabilities
        selection_point = random.uniform(0, rank_sum)
        current_sum = 0
        
        for i, individual in enumerate(sorted_population):
            # Lower rank (higher index) means lower probability
            rank = len(sorted_population) - i
            current_sum += rank
            if current_sum >= selection_point:
                return individual
        
        # Fallback (should not reach here)
        return sorted_population[-1]
    
    @staticmethod
    def stochastic_universal_sampling(population: List[Individual], num_selections: int) -> List[Individual]:
        """
        Select multiple individuals using stochastic universal sampling.
        
        This method provides a less biased and more consistent selection
        than repeatedly using roulette wheel selection.
        
        Args:
            population: List of individuals to select from
            num_selections: Number of individuals to select
            
        Returns:
            List[Individual]: The selected individuals
        """
        # Calculate total fitness
        total_fitness = sum(ind.fitness for ind in population)
        
        # Handle case where all individuals have zero fitness
        if total_fitness == 0:
            return random.choices(population, k=num_selections)
        
        # Calculate distance between pointers
        pointer_distance = total_fitness / num_selections
        
        # Generate random start point for first pointer
        start = random.uniform(0, pointer_distance)
        
        # Create pointers
        pointers = [start + i * pointer_distance for i in range(num_selections)]
        
        # Select individuals
        selected = []
        for pointer in pointers:
            current_sum = 0
            for individual in population:
                current_sum += individual.fitness
                if current_sum >= pointer:
                    selected.append(individual)
                    break
            
            # Fallback if no individual was selected (should not happen)
            if len(selected) < len(pointers):
                selected.append(population[-1])
        
        return selected
    
    @staticmethod
    def elitism_selection(population: List[Individual], n: int) -> List[Individual]:
        """
        Select the n best individuals from the population.
        
        This method is typically used to preserve the best individuals
        across generations.
        
        Args:
            population: List of individuals to select from
            n: Number of top individuals to select
            
        Returns:
            List[Individual]: The n best individuals
        """
        # Sort population by fitness (highest first) and select top n
        sorted_population = sorted(population, key=lambda ind: ind.fitness, reverse=True)
        return [ind.clone() for ind in sorted_population[:n]]