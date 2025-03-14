"""
Individual module for the Genetic Algorithm.

This module defines the Individual class, which represents a single guess
in the population of the genetic algorithm.
"""

import random
from typing import Optional, List, Tuple, Union


class Individual:
    """
    Represents a single individual (guess) in the genetic algorithm population.
    
    Each individual has a value (the guess) and a fitness score that determines
    how close it is to the target secret number.
    """
    
    def __init__(self, value: Optional[int] = None, min_value: int = 1, max_value: int = 100):
        """
        Initialize a new individual with an optional predefined value.
        
        Args:
            value: The value for this individual (guess number). If None, a random value is generated.
            min_value: The minimum possible value
            max_value: The maximum possible value
        """
        self.min_value = min_value
        self.max_value = max_value
        
        # Generate a random value if none is provided
        if value is None:
            self.value = random.randint(min_value, max_value)
        else:
            # Ensure the provided value is within the valid range
            self.value = max(min_value, min(value, max_value))
        
        self.fitness = 0.0
    
    def calculate_fitness(self, secret_number: int) -> float:
        """
        Calculate the fitness of this individual based on how close it is to the secret number.
        
        Args:
            secret_number: The target number to guess
            
        Returns:
            float: The calculated fitness value (higher is better)
        """
        # Calculate the distance from the secret number
        distance = abs(secret_number - self.value)
        
        # Calculate fitness - higher when closer to the secret number
        # Max fitness (100) is assigned when the guess is correct
        if distance == 0:
            self.fitness = 100.0
        else:
            # Fitness formula: MAX_NUMBER - abs(secret_number - guess)
            # This gives higher fitness to closer guesses
            range_size = self.max_value - self.min_value + 1
            self.fitness = max(0.0, range_size - distance)
            
            # Normalize to a 0-100 scale for better readability
            self.fitness = (self.fitness / range_size) * 100.0
        
        return self.fitness
    
    def crossover(self, partner: 'Individual') -> Tuple['Individual', 'Individual']:
        """
        Perform binary crossover with another individual to create two offspring.
        
        This method implements a specialized integer crossover appropriate for the
        number guessing problem, which ensures valid numeric values.
        
        Args:
            partner: Another individual to crossover with
            
        Returns:
            Tuple[Individual, Individual]: Two new individuals created by crossover
        """
        # Calculate average and difference between the two values
        average = (self.value + partner.value) // 2
        difference = abs(self.value - partner.value)
        
        # If the values are identical, create slightly varied offspring
        if difference == 0:
            # Add small random variations to create diversity
            child1_value = max(self.min_value, min(self.value + random.randint(1, 3), self.max_value))
            child2_value = max(self.min_value, min(self.value - random.randint(1, 3), self.max_value))
        else:
            # Create two children that explore the range between and around the parents
            # Child 1: Explore around the average
            child1_value = max(self.min_value, min(average + random.randint(-difference, difference), self.max_value))
            
            # Child 2: Explore a different region around the average
            offset = random.randint(-difference, difference)
            # Ensure the second child is different from the first
            while average + offset == child1_value:
                offset = random.randint(-difference, difference)
            child2_value = max(self.min_value, min(average + offset, self.max_value))
        
        # Create and return the new individuals
        child1 = Individual(child1_value, self.min_value, self.max_value)
        child2 = Individual(child2_value, self.min_value, self.max_value)
        
        return child1, child2
    
    def mutate(self, mutation_range: Optional[int] = None, mutation_probability: float = 1.0) -> None:
        """
        Apply mutation to this individual, modifying its value with some probability.
        
        Args:
            mutation_range: The maximum range of mutation (default: 10% of the value range)
            mutation_probability: The probability of mutation occurring (0.0 to 1.0)
        """
        # Check if mutation should occur
        if random.random() > mutation_probability:
            return
        
        # Calculate default mutation range if not provided
        if mutation_range is None:
            value_range = self.max_value - self.min_value
            mutation_range = max(1, value_range // 10)
        
        # Generate a random change amount
        change = random.randint(-mutation_range, mutation_range)
        
        # Ensure the change isn't zero (no mutation)
        while change == 0:
            change = random.randint(-mutation_range, mutation_range)
        
        # Apply the change and ensure the value stays within range
        self.value = max(self.min_value, min(self.value + change, self.max_value))
    
    def __str__(self) -> str:
        """
        Get a string representation of this individual.
        
        Returns:
            str: String representation with value and fitness
        """
        return f"Individual(value={self.value}, fitness={self.fitness:.2f})"
    
    def __repr__(self) -> str:
        """
        Get a detailed string representation of this individual.
        
        Returns:
            str: Detailed string representation
        """
        return f"Individual(value={self.value}, fitness={self.fitness:.2f}, range={self.min_value}-{self.max_value})"
    
    def clone(self) -> 'Individual':
        """
        Create a copy of this individual.
        
        Returns:
            Individual: A new individual with the same properties
        """
        clone = Individual(self.value, self.min_value, self.max_value)
        clone.fitness = self.fitness
        return clone