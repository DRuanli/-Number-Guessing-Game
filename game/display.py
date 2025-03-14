"""
Display module for the Number Guessing Game with Genetic Algorithm.

This module handles all user interface interactions, formatting, and
presentation of the game state and progress to the user.
"""

import os
import time
from typing import Dict, Any, List, Optional, Tuple, Union
import sys


class Display:
    """
    Handles the display and user interaction aspects of the game.
    
    This class manages all terminal output, formatting, and user input
    for the genetic algorithm number guessing game.
    """
    
    def __init__(self, verbose: bool = True, use_colors: bool = True):
        """
        Initialize the Display object with display preferences.
        
        Args:
            verbose: Whether to show detailed information
            use_colors: Whether to use colored output in the terminal
        """
        self.verbose = verbose
        self.use_colors = use_colors and self._supports_color()
        
        # ANSI color codes
        if self.use_colors:
            self.COLORS = {
                'RESET': '\033[0m',
                'BOLD': '\033[1m',
                'RED': '\033[91m',
                'GREEN': '\033[92m',
                'YELLOW': '\033[93m',
                'BLUE': '\033[94m',
                'MAGENTA': '\033[95m',
                'CYAN': '\033[96m',
            }
        else:
            self.COLORS = {k: '' for k in ['RESET', 'BOLD', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN']}
    
    def _supports_color(self) -> bool:
        """
        Check if the terminal supports color output.
        
        Returns:
            bool: True if the terminal supports color, False otherwise
        """
        # Simple check for color support
        if os.name == 'nt':  # Windows
            return 'ANSICON' in os.environ or 'WT_SESSION' in os.environ
        else:  # macOS, Linux, etc.
            return sys.stdout.isatty()
    
    def _color_text(self, text: str, color: str) -> str:
        """
        Apply color formatting to text.
        
        Args:
            text: The text to format
            color: The color to apply (must be a key in self.COLORS)
            
        Returns:
            str: The formatted text
        """
        if color in self.COLORS:
            return f"{self.COLORS[color]}{text}{self.COLORS['RESET']}"
        return text
    
    def clear_screen(self) -> None:
        """
        Clear the terminal screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_welcome(self) -> None:
        """
        Display the welcome message and game instructions.
        """
        self.clear_screen()
        title = "GENETIC ALGORITHM NUMBER GUESSING GAME"
        border = "=" * len(title)
        
        print(self._color_text(border, 'BOLD'))
        print(self._color_text(title, 'BOLD'))
        print(self._color_text(border, 'BOLD'))
        print()
        print("Welcome to the Genetic Algorithm Number Guessing Game!")
        print()
        print("In this game, you'll enter a secret number, and the genetic algorithm")
        print("will attempt to evolve a population of guesses to find your number.")
        print()
        print(self._color_text("How it works:", 'BOLD'))
        print("1. You enter a secret number within a specified range.")
        print("2. The algorithm creates a population of random guesses.")
        print("3. Through selection, crossover, and mutation, the algorithm evolves better guesses.")
        print("4. The process continues until the secret number is found or the maximum number of generations is reached.")
        print()
        print(self._color_text("Let's get started!", 'GREEN'))
        print()
        
        # Wait for user to press enter
        input("Press Enter to continue...")
    
    def get_secret_number(self, min_number: int, max_number: int) -> int:
        """
        Get the secret number from the user.
        
        Args:
            min_number: The minimum allowed number
            max_number: The maximum allowed number
            
        Returns:
            int: The secret number entered by the user
        """
        print()
        prompt = f"Enter your secret number ({min_number}-{max_number}): "
        while True:
            try:
                user_input = input(self._color_text(prompt, 'CYAN'))
                number = int(user_input)
                if min_number <= number <= max_number:
                    return number
                else:
                    print(self._color_text(f"Number must be between {min_number} and {max_number}.", 'RED'))
            except ValueError:
                print(self._color_text("Please enter a valid number.", 'RED'))
    
    def should_customize_parameters(self) -> bool:
        """
        Ask the user if they want to customize game parameters.
        
        Returns:
            bool: True if the user wants to customize, False otherwise
        """
        print()
        print(self._color_text("Game Parameters:", 'BOLD'))
        print("You can use the default parameters or customize them for this game.")
        
        while True:
            response = input(self._color_text("Do you want to customize parameters? (y/n): ", 'CYAN')).lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print(self._color_text("Please enter 'y' or 'n'.", 'RED'))
    
    def get_parameter(self, prompt: str, default: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]) -> Union[int, float]:
        """
        Get a parameter value from the user with validation.
        
        Args:
            prompt: The prompt to display
            default: The default value
            min_val: The minimum allowed value
            max_val: The maximum allowed value
            
        Returns:
            Union[int, float]: The parameter value
        """
        param_type = type(default)
        
        while True:
            try:
                full_prompt = f"{prompt} ({min_val}-{max_val}, default={default}): "
                user_input = input(self._color_text(full_prompt, 'CYAN'))
                
                # Use default if empty input
                if not user_input.strip():
                    return default
                
                # Convert to appropriate type
                if param_type == int:
                    value = int(user_input)
                else:
                    value = float(user_input)
                
                # Validate range
                if min_val <= value <= max_val:
                    return value
                else:
                    print(self._color_text(f"Value must be between {min_val} and {max_val}.", 'RED'))
            except ValueError:
                print(self._color_text(f"Please enter a valid {'integer' if param_type == int else 'number'}.", 'RED'))
    
    def show_game_setup(self, secret_number: int, config: Dict[str, Any]) -> None:
        """
        Display the game setup information.
        
        Args:
            secret_number: The secret number to guess
            config: Dictionary containing configuration parameters
        """
        self.clear_screen()
        print(self._color_text("Game Setup Complete!", 'GREEN'))
        print()
        
        # Only show the secret number if in verbose mode
        if self.verbose:
            print(f"Secret Number: {self._color_text(str(secret_number), 'YELLOW')}")
        
        print()
        print(self._color_text("Game Parameters:", 'BOLD'))
        print(f"- Number Range: {config.get('MIN_NUMBER', 1)}-{config.get('MAX_NUMBER', 100)}")
        print(f"- Population Size: {config.get('POPULATION_SIZE', 20)}")
        print(f"- Crossover Rate: {config.get('CROSSOVER_RATE', 0.8)}")
        print(f"- Mutation Rate: {config.get('MUTATION_RATE', 0.1)}")
        print(f"- Elitism Count: {config.get('ELITISM_COUNT', 2)}")
        print(f"- Maximum Generations: {config.get('MAX_GENERATIONS', 1000)}")
        print()
        
        print(self._color_text("The genetic algorithm will now attempt to guess your number...", 'CYAN'))
        print()
        time.sleep(2)  # Short pause for readability
    
    def show_message(self, message: str, color: str = 'RESET') -> None:
        """
        Display a message to the user.
        
        Args:
            message: The message to display
            color: The color to use (must be a key in self.COLORS)
        """
        print(self._color_text(message, color))
    
    def show_error(self, message: str) -> None:
        """
        Display an error message.
        
        Args:
            message: The error message
        """
        print(self._color_text(f"ERROR: {message}", 'RED'))
    
    def show_generation_header(self) -> None:
        """
        Display the header for generation progress.
        """
        print()
        header = f"{'Gen #':^8} | {'Best Guess':^12} | {'Best Fitness':^12} | {'Avg Fitness':^12}"
        divider = "-" * len(header)
        
        print(self._color_text(divider, 'BOLD'))
        print(self._color_text(header, 'BOLD'))
        print(self._color_text(divider, 'BOLD'))
    
    def show_generation_progress(self, generation: int, best_guess: Union[int, str], best_fitness: float, avg_fitness: float) -> None:
        """
        Display the progress of a specific generation.
        
        Args:
            generation: The generation number
            best_guess: The best guess in the generation
            best_fitness: The fitness of the best individual
            avg_fitness: The average fitness of the population
        """
        # Format the best guess
        if isinstance(best_guess, int):
            best_guess_str = str(best_guess)
        else:
            best_guess_str = best_guess  # Already a string (e.g., '?')
        
        # Format the fitness values
        best_fitness_str = f"{best_fitness:.2f}"
        avg_fitness_str = f"{avg_fitness:.2f}"
        
        # Choose color based on fitness (higher is better)
        if best_fitness >= 90:
            color = 'GREEN'
        elif best_fitness >= 70:
            color = 'YELLOW'
        elif best_fitness >= 50:
            color = 'CYAN'
        else:
            color = 'RESET'
        
        # Format and print the row
        row = f"{generation:^8} | {best_guess_str:^12} | {best_fitness_str:^12} | {avg_fitness_str:^12}"
        print(self._color_text(row, color))
    
    def show_max_generations_reached(self, max_generations: int) -> None:
        """
        Display a message when maximum generations are reached.
        
        Args:
            max_generations: The maximum number of generations
        """
        print()
        print(self._color_text(f"Maximum number of generations ({max_generations}) reached without finding the solution.", 'YELLOW'))
        print(self._color_text("The algorithm failed to guess the exact number.", 'YELLOW'))
        print()
    
    def show_game_results(self, secret_number: int, generations: int, elapsed_time: float, history: List[Dict[str, Any]]) -> None:
        """
        Display the final results of the game.
        
        Args:
            secret_number: The secret number
            generations: The number of generations
            elapsed_time: The elapsed time in seconds
            history: The generation history
        """
        solution_found = generations > 0 and history and history[-1]['best_fitness'] == 100
        
        print()
        print(self._color_text("=" * 50, 'BOLD'))
        
        if solution_found:
            print(self._color_text("SOLUTION FOUND!", 'GREEN'))
        else:
            print(self._color_text("GAME OVER", 'YELLOW'))
        
        print(self._color_text("=" * 50, 'BOLD'))
        print()
        
        print(f"Secret Number: {self._color_text(str(secret_number), 'CYAN')}")
        
        if solution_found:
            print(f"Number found in: {self._color_text(str(generations), 'GREEN')} generations")
            print(f"Time taken: {self._color_text(f'{elapsed_time:.2f}', 'GREEN')} seconds")
        else:
            best_gen = max(history, key=lambda x: x['best_fitness']) if history else None
            best_fitness = best_gen['best_fitness'] if best_gen else 0
            best_guess = best_gen['best_guess'] if best_gen else '?'
            
            print(f"Best guess: {self._color_text(str(best_guess), 'YELLOW')}")
            print(f"Best fitness: {self._color_text(f'{best_fitness:.2f}', 'YELLOW')}")
            print(f"Generations run: {self._color_text(str(generations), 'YELLOW')}")
            print(f"Time taken: {self._color_text(f'{elapsed_time:.2f}', 'YELLOW')} seconds")
        
        print()
        
        # Display additional statistics if in verbose mode
        if self.verbose and solution_found and len(history) > 1:
            self._show_performance_statistics(history)
    
    def _show_performance_statistics(self, history: List[Dict[str, Any]]) -> None:
        """
        Display performance statistics about the genetic algorithm.
        
        Args:
            history: The generation history
        """
        print(self._color_text("Performance Statistics:", 'BOLD'))
        
        # Calculate improvement metrics
        first_fitness = history[0]['best_fitness'] if history else 0
        last_fitness = history[-1]['best_fitness'] if history else 0
        total_improvement = last_fitness - first_fitness
        
        # Find the generation with the biggest improvement
        max_improvement = 0
        max_improvement_gen = 0
        
        for i in range(1, len(history)):
            improvement = history[i]['best_fitness'] - history[i-1]['best_fitness']
            if improvement > max_improvement:
                max_improvement = improvement
                max_improvement_gen = history[i]['generation']
        
        print(f"- Initial best fitness: {first_fitness:.2f}")
        print(f"- Total fitness improvement: {total_improvement:.2f}")
        
        if max_improvement > 0:
            print(f"- Biggest improvement: {max_improvement:.2f} at generation {max_improvement_gen}")
        
        # Calculate convergence metrics if solution was found
        if last_fitness == 100:
            gen_90 = None
            gen_95 = None
            gen_99 = None
            
            for entry in history:
                fitness = entry['best_fitness']
                gen = entry['generation']
                
                if fitness >= 90 and gen_90 is None:
                    gen_90 = gen
                if fitness >= 95 and gen_95 is None:
                    gen_95 = gen
                if fitness >= 99 and gen_99 is None:
                    gen_99 = gen
            
            if gen_90:
                print(f"- Reached 90% fitness at generation: {gen_90}")
            if gen_95:
                print(f"- Reached 95% fitness at generation: {gen_95}")
            if gen_99:
                print(f"- Reached 99% fitness at generation: {gen_99}")
        
        print()