"""
Configuration module for the Genetic Algorithm Number Guessing Game.

This module provides configuration management for the game, including default 
settings, validation, and configuration file handling.
"""

import json
import os
from typing import Dict, Any, Optional, List


# Default configuration values
DEFAULT_CONFIG = {
    # Game parameters
    'MIN_NUMBER': 1,
    'MAX_NUMBER': 100,
    'MAX_GENERATIONS': 1000,
    'DISPLAY_INTERVAL': 5,
    
    # Genetic algorithm parameters
    'POPULATION_SIZE': 20,
    'CROSSOVER_RATE': 0.8,
    'MUTATION_RATE': 0.1,
    'MUTATION_RANGE': None,  # Auto-calculated based on number range
    'ELITISM_COUNT': 2,
    
    # Selection parameters
    'SELECTION_METHOD': 'tournament',  # Options: 'tournament', 'roulette', 'rank'
    'TOURNAMENT_SIZE': 3,
    
    # Crossover parameters
    'CROSSOVER_METHOD': 'adaptive',  # Options: 'arithmetic', 'average', 'binary', 'binary_two_point', 'adaptive'
    
    # Mutation parameters
    'MUTATION_METHOD': 'adaptive',  # Options: 'random', 'bit_flip', 'boundary', 'gaussian', 'adaptive'
    
    # Fitness parameters
    'FITNESS_METHOD': 'linear',  # Options: 'linear', 'inverse', 'exponential', 'combined', 'hot_cold'
    
    # Display parameters
    'VERBOSE': True,
    'USE_COLORS': True,
    
    # Advanced parameters
    'CONVERGENCE_THRESHOLD': 5,  # Number of generations with no improvement before considering converged
    'RESTART_ON_CONVERGENCE': False,  # Whether to restart the population when converged
    'ADAPTIVE_MUTATION': True,  # Whether to increase mutation when converged
}


class Config:
    """
    Configuration manager for the genetic algorithm number guessing game.
    
    This class handles loading, saving, validating, and accessing configuration
    parameters for the game.
    """
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize the configuration with optional custom values.
        
        Args:
            config_dict: Custom configuration dictionary to override defaults
        """
        # Start with default configuration
        self.config = DEFAULT_CONFIG.copy()
        
        # Override with custom configuration if provided
        if config_dict:
            self.update(config_dict)
        
        # Validate the configuration
        self.validate()
    
    def update(self, config_dict: Dict[str, Any]) -> None:
        """
        Update the configuration with new values.
        
        Args:
            config_dict: Dictionary containing configuration values to update
        """
        for key, value in config_dict.items():
            if key in self.config:
                self.config[key] = value
    
    def validate(self) -> None:
        """
        Validate the configuration values and adjust if necessary.
        """
        # Validate numeric ranges
        self._validate_range('MIN_NUMBER', 1, 1000000)
        self._validate_range('MAX_NUMBER', self.config['MIN_NUMBER'], 1000000)
        self._validate_range('MAX_GENERATIONS', 1, 100000)
        self._validate_range('DISPLAY_INTERVAL', 1, 1000)
        
        # Validate genetic algorithm parameters
        self._validate_range('POPULATION_SIZE', 2, 1000)
        self._validate_range('CROSSOVER_RATE', 0.0, 1.0)
        self._validate_range('MUTATION_RATE', 0.0, 1.0)
        self._validate_range('ELITISM_COUNT', 0, self.config['POPULATION_SIZE'] // 2)
        
        # Validate selection parameters
        valid_selection_methods = ['tournament', 'roulette', 'rank']
        if self.config['SELECTION_METHOD'] not in valid_selection_methods:
            self.config['SELECTION_METHOD'] = 'tournament'
        
        self._validate_range('TOURNAMENT_SIZE', 2, 10)
        
        # Validate crossover parameters
        valid_crossover_methods = ['arithmetic', 'average', 'binary', 'binary_two_point', 'adaptive']
        if self.config['CROSSOVER_METHOD'] not in valid_crossover_methods:
            self.config['CROSSOVER_METHOD'] = 'adaptive'
        
        # Validate mutation parameters
        valid_mutation_methods = ['random', 'bit_flip', 'boundary', 'gaussian', 'adaptive']
        if self.config['MUTATION_METHOD'] not in valid_mutation_methods:
            self.config['MUTATION_METHOD'] = 'adaptive'
        
        # Validate fitness parameters
        valid_fitness_methods = ['linear', 'inverse', 'exponential', 'combined', 'hot_cold']
        if self.config['FITNESS_METHOD'] not in valid_fitness_methods:
            self.config['FITNESS_METHOD'] = 'linear'
        
        # Validate boolean parameters
        for key in ['VERBOSE', 'USE_COLORS', 'RESTART_ON_CONVERGENCE', 'ADAPTIVE_MUTATION']:
            if not isinstance(self.config[key], bool):
                self.config[key] = DEFAULT_CONFIG[key]
        
        # Calculate mutation range if not set
        if self.config['MUTATION_RANGE'] is None:
            value_range = self.config['MAX_NUMBER'] - self.config['MIN_NUMBER']
            self.config['MUTATION_RANGE'] = max(1, value_range // 10)  # 10% of the range
        
        # Validate convergence parameters
        self._validate_range('CONVERGENCE_THRESHOLD', 1, 100)
    
    def _validate_range(self, key: str, min_val: Any, max_val: Any) -> None:
        """
        Validate that a configuration value is within a specified range.
        
        Args:
            key: The configuration key to validate
            min_val: The minimum allowed value
            max_val: The maximum allowed value
        """
        if key in self.config:
            value = self.config[key]
            try:
                # Convert to appropriate type if needed
                if isinstance(min_val, int) and not isinstance(value, int):
                    value = int(value)
                elif isinstance(min_val, float) and not isinstance(value, float):
                    value = float(value)
                
                # Enforce range
                self.config[key] = max(min_val, min(value, max_val))
            except (ValueError, TypeError):
                # If conversion fails, use default value
                self.config[key] = DEFAULT_CONFIG[key]
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: The configuration key to retrieve
            default: The default value to return if the key doesn't exist
            
        Returns:
            Any: The configuration value
        """
        return self.config.get(key, default)
    
    def save(self, filepath: str) -> bool:
        """
        Save the configuration to a JSON file.
        
        Args:
            filepath: The path to save the configuration to
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception:
            return False
    
    @classmethod
    def load(cls, filepath: str) -> 'Config':
        """
        Load configuration from a JSON file.
        
        Args:
            filepath: The path to load the configuration from
            
        Returns:
            Config: A new Config object with the loaded values
        """
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    config_dict = json.load(f)
                return cls(config_dict)
        except Exception:
            pass
        
        # Return default configuration if loading fails
        return cls()
    
    def as_dict(self) -> Dict[str, Any]:
        """
        Get the configuration as a dictionary.
        
        Returns:
            Dict[str, Any]: The configuration dictionary
        """
        return self.config.copy()
    
    def __getitem__(self, key: str) -> Any:
        """
        Get a configuration value using dictionary-like syntax.
        
        Args:
            key: The configuration key to retrieve
            
        Returns:
            Any: The configuration value
            
        Raises:
            KeyError: If the key doesn't exist
        """
        return self.config[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set a configuration value using dictionary-like syntax.
        
        Args:
            key: The configuration key to set
            value: The value to set
        """
        if key in self.config:
            self.config[key] = value
            self.validate()  # Re-validate to ensure consistency
    
    def __str__(self) -> str:
        """
        Get a string representation of the configuration.
        
        Returns:
            str: A formatted string representation
        """
        sections = {
            "Game Parameters": ['MIN_NUMBER', 'MAX_NUMBER', 'MAX_GENERATIONS', 'DISPLAY_INTERVAL'],
            "Genetic Algorithm": ['POPULATION_SIZE', 'CROSSOVER_RATE', 'MUTATION_RATE', 'MUTATION_RANGE', 'ELITISM_COUNT'],
            "Selection": ['SELECTION_METHOD', 'TOURNAMENT_SIZE'],
            "Crossover": ['CROSSOVER_METHOD'],
            "Mutation": ['MUTATION_METHOD'],
            "Fitness": ['FITNESS_METHOD'],
            "Display": ['VERBOSE', 'USE_COLORS'],
            "Advanced": ['CONVERGENCE_THRESHOLD', 'RESTART_ON_CONVERGENCE', 'ADAPTIVE_MUTATION']
        }
        
        result = "Configuration:\n"
        for section, keys in sections.items():
            result += f"\n{section}:\n"
            for key in keys:
                if key in self.config:
                    result += f"  {key}: {self.config[key]}\n"
        
        return result