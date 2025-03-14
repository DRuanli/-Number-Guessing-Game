"""
Crossover module for the Genetic Algorithm.

This module provides different crossover methods for combining individuals
to create offspring in the genetic algorithm.
"""

import random
from typing import Tuple, List, Optional

from .individual import Individual


class Crossover:
    """
    Provides different crossover methods for the genetic algorithm.
    
    This class implements various strategies for combining two parent individuals
    to create offspring, specifically adapted for the number guessing problem.
    """
    
    @staticmethod
    def arithmetic_crossover(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """
        Perform arithmetic crossover between two individuals.
        
        This method creates offspring by taking weighted averages of the parent values.
        
        Args:
            parent1: First parent individual
            parent2: Second parent individual
            
        Returns:
            Tuple[Individual, Individual]: Two new offspring individuals
        """
        min_value = parent1.min_value
        max_value = parent1.max_value
        
        # Generate random weights
        weight = random.random()
        
        # Create child values using weighted averages
        child1_value = int(weight * parent1.value + (1 - weight) * parent2.value)
        child2_value = int((1 - weight) * parent1.value + weight * parent2.value)
        
        # Ensure values are within range
        child1_value = max(min_value, min(child1_value, max_value))
        child2_value = max(min_value, min(child2_value, max_value))
        
        # Create and return new individuals
        child1 = Individual(child1_value, min_value, max_value)
        child2 = Individual(child2_value, min_value, max_value)
        
        return child1, child2
    
    @staticmethod
    def average_crossover(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """
        Perform average crossover between two individuals.
        
        This method creates offspring by averaging the parents' values and adding some variation.
        
        Args:
            parent1: First parent individual
            parent2: Second parent individual
            
        Returns:
            Tuple[Individual, Individual]: Two new offspring individuals
        """
        min_value = parent1.min_value
        max_value = parent1.max_value
        
        # Calculate average and difference
        average = (parent1.value + parent2.value) // 2
        difference = abs(parent1.value - parent2.value)
        
        # If parents have identical values, create diversity
        if difference == 0:
            variation1 = random.randint(1, 3)
            variation2 = random.randint(1, 3)
            child1_value = max(min_value, min(average + variation1, max_value))
            child2_value = max(min_value, min(average - variation2, max_value))
        else:
            # Create children that explore around the parents
            variation1 = random.randint(-difference, difference)
            variation2 = random.randint(-difference, difference)
            child1_value = max(min_value, min(average + variation1, max_value))
            child2_value = max(min_value, min(average + variation2, max_value))
        
        # Create and return new individuals
        child1 = Individual(child1_value, min_value, max_value)
        child2 = Individual(child2_value, min_value, max_value)
        
        return child1, child2
    
    @staticmethod
    def binary_crossover(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """
        Perform binary crossover between two individuals.
        
        This method converts the parent values to binary, performs crossover,
        and converts back to integers.
        
        Args:
            parent1: First parent individual
            parent2: Second parent individual
            
        Returns:
            Tuple[Individual, Individual]: Two new offspring individuals
        """
        min_value = parent1.min_value
        max_value = parent1.max_value
        
        # Convert parent values to binary strings
        max_bits = len(bin(max_value)) - 2  # -2 to remove '0b' prefix
        parent1_bits = format(parent1.value, f'0{max_bits}b')
        parent2_bits = format(parent2.value, f'0{max_bits}b')
        
        # Choose a random crossover point
        crossover_point = random.randint(1, max_bits - 1)
        
        # Perform single-point crossover
        child1_bits = parent1_bits[:crossover_point] + parent2_bits[crossover_point:]
        child2_bits = parent2_bits[:crossover_point] + parent1_bits[crossover_point:]
        
        # Convert binary strings back to integers
        child1_value = int(child1_bits, 2)
        child2_value = int(child2_bits, 2)
        
        # Ensure values are within range
        child1_value = max(min_value, min(child1_value, max_value))
        child2_value = max(min_value, min(child2_value, max_value))
        
        # Create and return new individuals
        child1 = Individual(child1_value, min_value, max_value)
        child2 = Individual(child2_value, min_value, max_value)
        
        return child1, child2
    
    @staticmethod
    def binary_two_point_crossover(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """
        Perform binary two-point crossover between two individuals.
        
        This method converts the parent values to binary, performs two-point crossover,
        and converts back to integers.
        
        Args:
            parent1: First parent individual
            parent2: Second parent individual
            
        Returns:
            Tuple[Individual, Individual]: Two new offspring individuals
        """
        min_value = parent1.min_value
        max_value = parent1.max_value
        
        # Convert parent values to binary strings
        max_bits = len(bin(max_value)) - 2  # -2 to remove '0b' prefix
        parent1_bits = format(parent1.value, f'0{max_bits}b')
        parent2_bits = format(parent2.value, f'0{max_bits}b')
        
        # Choose two distinct random crossover points
        point1 = random.randint(1, max_bits - 2)
        point2 = random.randint(point1 + 1, max_bits - 1)
        
        # Perform two-point crossover
        child1_bits = parent1_bits[:point1] + parent2_bits[point1:point2] + parent1_bits[point2:]
        child2_bits = parent2_bits[:point1] + parent1_bits[point1:point2] + parent2_bits[point2:]
        
        # Convert binary strings back to integers
        child1_value = int(child1_bits, 2)
        child2_value = int(child2_bits, 2)
        
        # Ensure values are within range
        child1_value = max(min_value, min(child1_value, max_value))
        child2_value = max(min_value, min(child2_value, max_value))
        
        # Create and return new individuals
        child1 = Individual(child1_value, min_value, max_value)
        child2 = Individual(child2_value, min_value, max_value)
        
        return child1, child2
    
    @staticmethod
    def adaptive_crossover(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """
        Perform adaptive crossover that chooses the most appropriate method.
        
        This method selects the crossover technique based on the characteristics
        of the parents to optimize exploration or exploitation.
        
        Args:
            parent1: First parent individual
            parent2: Second parent individual
            
        Returns:
            Tuple[Individual, Individual]: Two new offspring individuals
        """
        # Calculate difference between parents
        difference = abs(parent1.value - parent2.value)
        range_size = parent1.max_value - parent1.min_value
        
        # Use different strategies based on the parents' similarity
        if difference < range_size * 0.05:  # Very similar parents
            # Use binary crossover to encourage exploration
            return Crossover.binary_crossover(parent1, parent2)
        elif difference < range_size * 0.20:  # Moderately similar parents
            # Use binary two-point crossover for balanced exploration
            return Crossover.binary_two_point_crossover(parent1, parent2)
        else:  # Very different parents
            # Use average crossover to focus the search
            return Crossover.average_crossover(parent1, parent2)