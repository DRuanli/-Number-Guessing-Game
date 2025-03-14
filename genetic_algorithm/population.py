"""
Population module for the Genetic Algorithm.

This module defines the Population class, which manages a collection of individuals
and controls the evolutionary process of the genetic algorithm.
"""

import random
import statistics
from typing import List, Dict, Any, Tuple, Optional, Callable

from .individual import Individual


class Population:
    """
    Manages a population of individuals in the genetic algorithm.
    
    This class handles population initialization, selection, crossover, mutation,
    and generation advancement for the genetic algorithm.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize a new population with configuration parameters.
        
        Args:
            config: Dictionary containing configuration parameters
        """
        # Store configuration parameters
        self.min_value = config.get('MIN_NUMBER', 1)
        self.max_value = config.get('MAX_NUMBER', 100)
        self.population_size = config.get('POPULATION_SIZE', 20)
        self.crossover_rate = config.get('CROSSOVER_RATE', 0.8)
        self.mutation_rate = config.get('MUTATION_RATE', 0.1)
        self.elitism_count = config.get('ELITISM_COUNT', 2)
        
        # Calculate mutation range based on the number range
        value_range = self.max_value - self.min_value
        self.mutation_range = max(1, value_range // 10)  # 10% of the range by default
        
        # Initialize population with random individuals
        self.individuals = [
            Individual(None, self.min_value, self.max_value)
            for _ in range(self.population_size)
        ]
        
        # Keep track of the best individual
        self.best_individual = None
        
        # Statistics for the current generation
        self.generation_stats = {
            'avg_fitness': 0.0,
            'best_fitness': 0.0,
            'best_guess': None,
            'fitness_std_dev': 0.0,
            'unique_values': 0
        }
    
    def evaluate_fitness(self, secret_number: int) -> None:
        """
        Evaluate the fitness of all individuals in the population.
        
        Args:
            secret_number: The target number to guess
        """
        # Calculate fitness for each individual
        for individual in self.individuals:
            individual.calculate_fitness(secret_number)
        
        # Sort individuals by fitness (highest first)
        self.individuals.sort(key=lambda ind: ind.fitness, reverse=True)
        
        # Update the best individual
        self.best_individual = self.individuals[0].clone()
        
        # Calculate statistics
        self._calculate_statistics()
    
    def _calculate_statistics(self) -> None:
        """
        Calculate various statistics about the current population.
        """
        # Extract fitness values
        fitness_values = [ind.fitness for ind in self.individuals]
        
        # Calculate unique values
        unique_values = len(set(ind.value for ind in self.individuals))
        
        # Calculate statistics
        self.generation_stats = {
            'avg_fitness': statistics.mean(fitness_values),
            'best_fitness': self.best_individual.fitness,
            'best_guess': self.best_individual.value,
            'fitness_std_dev': statistics.stdev(fitness_values) if len(fitness_values) > 1 else 0.0,
            'unique_values': unique_values
        }
    
    def create_next_generation(self) -> None:
        """
        Create the next generation of individuals through selection, crossover, and mutation.
        """
        new_population = []
        
        # Add elite individuals directly to the new population (if enabled)
        if self.elitism_count > 0:
            # Add copies of the best individuals
            new_population.extend([
                ind.clone() for ind in self.individuals[:self.elitism_count]
            ])
        
        # Fill the rest of the population with offspring
        while len(new_population) < self.population_size:
            # Select parents using tournament selection
            parent1 = self._tournament_selection(3)  # Tournament size of 3
            parent2 = self._tournament_selection(3)
            
            # Ensure parents are different if possible
            attempts = 0
            while parent1.value == parent2.value and attempts < 5:
                parent2 = self._tournament_selection(3)
                attempts += 1
            
            # Perform crossover with some probability
            if random.random() < self.crossover_rate:
                child1, child2 = parent1.crossover(parent2)
            else:
                # No crossover, just clone the parents
                child1, child2 = parent1.clone(), parent2.clone()
            
            # Apply mutation
            child1.mutate(self.mutation_range, self.mutation_rate)
            child2.mutate(self.mutation_range, self.mutation_rate)
            
            # Add children to the new population
            new_population.append(child1)
            if len(new_population) < self.population_size:
                new_population.append(child2)
        
        # Replace the old population with the new one
        self.individuals = new_population
    
    def _tournament_selection(self, tournament_size: int) -> Individual:
        """
        Select an individual using tournament selection.
        
        Args:
            tournament_size: The number of individuals to include in the tournament
            
        Returns:
            Individual: The selected individual
        """
        # Select random individuals for the tournament
        tournament = random.sample(self.individuals, min(tournament_size, len(self.individuals)))
        
        # Return the individual with the highest fitness
        return max(tournament, key=lambda ind: ind.fitness)
    
    def _roulette_wheel_selection(self) -> Individual:
        """
        Select an individual using roulette wheel selection.
        
        Returns:
            Individual: The selected individual
        """
        # Calculate total fitness
        total_fitness = sum(ind.fitness for ind in self.individuals)
        
        # Handle case where all individuals have zero fitness
        if total_fitness == 0:
            return random.choice(self.individuals)
        
        # Generate a random value between 0 and the total fitness
        selection_point = random.uniform(0, total_fitness)
        
        # Find the individual at the selection point
        current_sum = 0
        for individual in self.individuals:
            current_sum += individual.fitness
            if current_sum >= selection_point:
                return individual
        
        # Fallback (should not reach here)
        return self.individuals[-1]
    
    def get_best_individual(self) -> Individual:
        """
        Get the best individual in the current population.
        
        Returns:
            Individual: The individual with the highest fitness
        """
        if self.best_individual is None:
            # If best_individual hasn't been set yet, find it now
            self.best_individual = max(self.individuals, key=lambda ind: ind.fitness)
        
        return self.best_individual
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the current population.
        
        Returns:
            Dict[str, Any]: Dictionary containing population statistics
        """
        return self.generation_stats
    
    def get_average_fitness(self) -> float:
        """
        Get the average fitness of the population.
        
        Returns:
            float: The average fitness
        """
        return self.generation_stats['avg_fitness']
    
    def get_fitness_diversity(self) -> float:
        """
        Get a measure of the genetic diversity in the population.
        
        Returns:
            float: The standard deviation of fitness values (higher means more diverse)
        """
        return self.generation_stats['fitness_std_dev']
    
    def get_value_diversity(self) -> float:
        """
        Get a measure of the diversity of values in the population.
        
        Returns:
            float: The percentage of unique values in the population
        """
        return self.generation_stats['unique_values'] / self.population_size if self.population_size > 0 else 0.0
    
    def __str__(self) -> str:
        """
        Get a string representation of the population.
        
        Returns:
            str: A string summary of the population
        """
        return (f"Population(size={len(self.individuals)}, "
                f"avg_fitness={self.generation_stats['avg_fitness']:.2f}, "
                f"best_fitness={self.generation_stats['best_fitness']:.2f})")
    
    def __len__(self) -> int:
        """
        Get the size of the population.
        
        Returns:
            int: The number of individuals in the population
        """
        return len(self.individuals)