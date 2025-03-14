"""
Fitness calculation module for the Genetic Algorithm.

This module provides different fitness functions for evaluating
individuals in the genetic algorithm.
"""

from typing import Optional, Callable, List
from .individual import Individual


class FitnessCalculator:
    """
    Provides different fitness calculation methods for the genetic algorithm.
    
    This class implements various strategies for evaluating how close
    a guess is to the secret number.
    """
    
    @staticmethod
    def linear_distance(guess: int, secret_number: int, min_value: int, max_value: int) -> float:
        """
        Calculate fitness based on linear distance from the secret number.
        
        This is the default fitness function that gives higher fitness to closer guesses.
        
        Args:
            guess: The guessed number
            secret_number: The target number
            min_value: The minimum possible value
            max_value: The maximum possible value
            
        Returns:
            float: The calculated fitness value (0-100)
        """
        # Calculate the distance from the secret number
        distance = abs(secret_number - guess)
        
        # Calculate fitness - higher when closer to the secret number
        # Max fitness (100) is assigned when the guess is correct
        if distance == 0:
            return 100.0
        else:
            # Fitness formula: MAX_NUMBER - abs(secret_number - guess)
            # This gives higher fitness to closer guesses
            range_size = max_value - min_value + 1
            fitness = max(0.0, range_size - distance)
            
            # Normalize to a 0-100 scale for better readability
            return (fitness / range_size) * 100.0
    
    @staticmethod
    def inverse_distance(guess: int, secret_number: int, min_value: int, max_value: int) -> float:
        """
        Calculate fitness based on inverse distance from the secret number.
        
        This fitness function gives higher differentiation between close guesses.
        
        Args:
            guess: The guessed number
            secret_number: The target number
            min_value: The minimum possible value
            max_value: The maximum possible value
            
        Returns:
            float: The calculated fitness value (0-100)
        """
        # Calculate the distance from the secret number
        distance = abs(secret_number - guess)
        
        # Calculate fitness - higher when closer to the secret number
        if distance == 0:
            return 100.0
        else:
            # Range of possible values
            range_size = max_value - min_value + 1
            
            # Calculate inverse distance
            inverse_distance = 1.0 / distance
            
            # Scale to 0-99 range (100 is reserved for exact match)
            max_inverse = 1.0  # when distance = 1
            min_inverse = 1.0 / range_size
            
            # Normalize to 0-99 scale
            normalized = ((inverse_distance - min_inverse) / 
                         (max_inverse - min_inverse)) * 99.0
            
            return normalized
    
    @staticmethod
    def exponential_decay(guess: int, secret_number: int, min_value: int, max_value: int) -> float:
        """
        Calculate fitness using exponential decay based on distance.
        
        This fitness function heavily rewards very close guesses.
        
        Args:
            guess: The guessed number
            secret_number: The target number
            min_value: The minimum possible value
            max_value: The maximum possible value
            
        Returns:
            float: The calculated fitness value (0-100)
        """
        # Calculate the distance from the secret number
        distance = abs(secret_number - guess)
        
        # Calculate fitness - higher when closer to the secret number
        if distance == 0:
            return 100.0
        else:
            # Range of possible values
            range_size = max_value - min_value + 1
            
            # Scale factor for exponential decay (adjust as needed)
            scale_factor = 5.0 / range_size
            
            # Calculate exponential decay
            fitness = 99.0 * (2.718 ** (-scale_factor * distance))
            
            return fitness
    
    @staticmethod
    def combined_fitness(guess: int, secret_number: int, min_value: int, max_value: int) -> float:
        """
        Calculate fitness using a combination of methods for a balanced approach.
        
        This fitness function combines linear and exponential methods.
        
        Args:
            guess: The guessed number
            secret_number: The target number
            min_value: The minimum possible value
            max_value: The maximum possible value
            
        Returns:
            float: The calculated fitness value (0-100)
        """
        # Calculate the distance from the secret number
        distance = abs(secret_number - guess)
        
        # Calculate fitness - higher when closer to the secret number
        if distance == 0:
            return 100.0
        else:
            # Calculate linear component
            range_size = max_value - min_value + 1
            linear_fitness = max(0.0, range_size - distance) / range_size
            
            # Calculate exponential component
            scale_factor = 5.0 / range_size
            exp_fitness = 2.718 ** (-scale_factor * distance)
            
            # Combine with weights (60% linear, 40% exponential)
            combined = (0.6 * linear_fitness + 0.4 * exp_fitness) * 99.0
            
            return combined
    
    @staticmethod
    def hot_cold_guidance(guess: int, secret_number: int, min_value: int, max_value: int, 
                         previous_guess: Optional[int] = None) -> float:
        """
        Calculate fitness with hot/cold guidance based on previous guess.
        
        This fitness function gives bonus fitness when moving in the right direction.
        
        Args:
            guess: The guessed number
            secret_number: The target number
            min_value: The minimum possible value
            max_value: The maximum possible value
            previous_guess: The previous guess (if any)
            
        Returns:
            float: The calculated fitness value (0-100)
        """
        # Calculate the distance from the secret number
        distance = abs(secret_number - guess)
        
        # Calculate baseline fitness - higher when closer to the secret number
        if distance == 0:
            return 100.0
        
        # Calculate basic fitness
        range_size = max_value - min_value + 1
        basic_fitness = max(0.0, range_size - distance) / range_size * 90.0
        
        # If we have a previous guess, provide directional guidance
        direction_bonus = 0.0
        if previous_guess is not None:
            prev_distance = abs(secret_number - previous_guess)
            
            # Bonus for moving in the right direction
            if distance < prev_distance:
                # Moving closer - give bonus
                direction_bonus = 10.0
            elif distance > prev_distance:
                # Moving away - give penalty
                direction_bonus = -5.0
        
        return max(0.0, min(99.0, basic_fitness + direction_bonus))
    
    @staticmethod
    def evaluate_population(population: List[Individual], secret_number: int, 
                           fitness_function: Callable = None) -> None:
        """
        Evaluate fitness for all individuals in a population.
        
        Args:
            population: List of individuals to evaluate
            secret_number: The target number
            fitness_function: The fitness function to use (defaults to linear_distance)
        """
        # Use default fitness function if none provided
        if fitness_function is None:
            fitness_function = FitnessCalculator.linear_distance
        
        # Calculate fitness for each individual
        for individual in population:
            if fitness_function == FitnessCalculator.linear_distance:
                # Use the individual's built-in method for the default function
                individual.calculate_fitness(secret_number)
            else:
                # Use the provided custom fitness function
                individual.fitness = fitness_function(
                    individual.value, 
                    secret_number, 
                    individual.min_value, 
                    individual.max_value
                )