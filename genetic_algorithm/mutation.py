"""
Mutation module for the Genetic Algorithm.

This module provides different mutation methods for introducing variation
into individuals in the genetic algorithm.
"""

import random
from typing import Optional

from .individual import Individual


class Mutation:
    """
    Provides different mutation methods for the genetic algorithm.
    
    This class implements various strategies for modifying individuals to 
    introduce genetic diversity and prevent premature convergence.
    """
    
    @staticmethod
    def random_mutation(individual: Individual, mutation_range: Optional[int] = None, 
                        mutation_probability: float = 1.0) -> None:
        """
        Apply random value mutation to an individual.
        
        This method increases or decreases the individual's value by a random amount.
        
        Args:
            individual: The individual to mutate
            mutation_range: The maximum range of mutation
            mutation_probability: The probability of mutation occurring
        """
        # Check if mutation should occur
        if random.random() > mutation_probability:
            return
        
        # Calculate default mutation range if not provided
        if mutation_range is None:
            value_range = individual.max_value - individual.min_value
            mutation_range = max(1, value_range // 10)  # 10% of the range by default
        
        # Generate a random change amount
        change = random.randint(-mutation_range, mutation_range)
        
        # Ensure the change isn't zero (no mutation)
        while change == 0:
            change = random.randint(-mutation_range, mutation_range)
        
        # Apply the change and ensure the value stays within range
        individual.value = max(individual.min_value, 
                              min(individual.value + change, individual.max_value))
    
    @staticmethod
    def bit_flip_mutation(individual: Individual, mutation_probability: float = 0.1) -> None:
        """
        Apply bit flip mutation to an individual.
        
        This method flips random bits in the binary representation of the individual's value.
        
        Args:
            individual: The individual to mutate
            mutation_probability: The probability of each bit being flipped
        """
        # Convert value to binary
        max_bits = len(bin(individual.max_value)) - 2  # -2 to remove '0b' prefix
        value_bits = format(individual.value, f'0{max_bits}b')
        
        # Flip bits with the given probability
        result_bits = ''
        for bit in value_bits:
            if random.random() < mutation_probability:
                # Flip the bit
                result_bits += '1' if bit == '0' else '0'
            else:
                # Keep the bit unchanged
                result_bits += bit
        
        # Convert back to integer
        new_value = int(result_bits, 2)
        
        # Ensure the value stays within range
        individual.value = max(individual.min_value, 
                              min(new_value, individual.max_value))
    
    @staticmethod
    def boundary_mutation(individual: Individual, mutation_probability: float = 0.05) -> None:
        """
        Apply boundary mutation to an individual.
        
        This method occasionally sets the individual's value to either the minimum or maximum boundary.
        It helps explore the extreme values in the search space.
        
        Args:
            individual: The individual to mutate
            mutation_probability: The probability of mutation occurring
        """
        # Check if mutation should occur
        if random.random() > mutation_probability:
            return
        
        # Set to either min or max value
        if random.random() < 0.5:
            individual.value = individual.min_value
        else:
            individual.value = individual.max_value
    
    @staticmethod
    def gaussian_mutation(individual: Individual, mutation_probability: float = 0.3, 
                         sigma: Optional[float] = None) -> None:
        """
        Apply Gaussian mutation to an individual.
        
        This method adds a random value from a normal (Gaussian) distribution
        to the individual's value, which tends to make smaller changes more likely
        than larger ones.
        
        Args:
            individual: The individual to mutate
            mutation_probability: The probability of mutation occurring
            sigma: Standard deviation for the Gaussian distribution
        """
        # Check if mutation should occur
        if random.random() > mutation_probability:
            return
        
        # Calculate default sigma if not provided
        if sigma is None:
            value_range = individual.max_value - individual.min_value
            sigma = value_range * 0.05  # 5% of the range by default
        
        # Generate change from Gaussian distribution
        change = int(random.gauss(0, sigma))
        
        # Ensure the change isn't zero (no mutation)
        while change == 0:
            change = int(random.gauss(0, sigma))
        
        # Apply the change and ensure the value stays within range
        individual.value = max(individual.min_value, 
                              min(individual.value + change, individual.max_value))
    
    @staticmethod
    def adaptive_mutation(individual: Individual, fitness: float, 
                         max_fitness: float = 100.0, generation: int = 0) -> None:
        """
        Apply adaptive mutation that adjusts based on fitness and generation.
        
        This method increases mutation strength when fitness is low or
        when many generations have passed with little improvement.
        
        Args:
            individual: The individual to mutate
            fitness: The current fitness of the individual
            max_fitness: The maximum possible fitness
            generation: The current generation number
        """
        # Calculate mutation probability based on fitness
        # Lower fitness = higher mutation probability
        fitness_ratio = fitness / max_fitness
        base_probability = 0.1 + (1.0 - fitness_ratio) * 0.4
        
        # Increase probability slightly based on generation
        # (to avoid stagnation in later generations)
        generation_factor = min(0.3, generation / 1000)
        mutation_probability = min(0.9, base_probability + generation_factor)
        
        # Calculate mutation range based on fitness
        # Lower fitness = larger mutation range
        value_range = individual.max_value - individual.min_value
        mutation_factor = 1.0 - (fitness_ratio ** 2)  # Squared to emphasize differences
        mutation_range = max(1, int(value_range * 0.05 * (1 + 3 * mutation_factor)))
        
        # Apply mutation
        Mutation.random_mutation(individual, mutation_range, mutation_probability)