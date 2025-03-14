"""
Main entry point for the Genetic Algorithm Number Guessing Game.

This module serves as the entry point for the application, coordinating
the genetic algorithm components and game flow.
"""

import os
import sys
import argparse
import time
from typing import Dict, Any, Optional

# Import game components
from game.game_manager import GameManager
from game.display import Display

# Import genetic algorithm components
from genetic_algorithm.individual import Individual
from genetic_algorithm.population import Population
from genetic_algorithm.selection import Selection
from genetic_algorithm.crossover import Crossover
from genetic_algorithm.mutation import Mutation
from genetic_algorithm.fitness import FitnessCalculator

# Import utility components
from utils.config import Config, DEFAULT_CONFIG
from utils.statistics import StatisticsTracker


def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Genetic Algorithm Number Guessing Game')
    
    parser.add_argument('--min', type=int, default=DEFAULT_CONFIG['MIN_NUMBER'],
                       help='Minimum number in the range')
    
    parser.add_argument('--max', type=int, default=DEFAULT_CONFIG['MAX_NUMBER'],
                       help='Maximum number in the range')
    
    parser.add_argument('--population', type=int, default=DEFAULT_CONFIG['POPULATION_SIZE'],
                       help='Population size')
    
    parser.add_argument('--crossover-rate', type=float, default=DEFAULT_CONFIG['CROSSOVER_RATE'],
                       help='Crossover rate (0.0-1.0)')
    
    parser.add_argument('--mutation-rate', type=float, default=DEFAULT_CONFIG['MUTATION_RATE'],
                       help='Mutation rate (0.0-1.0)')
    
    parser.add_argument('--elitism', type=int, default=DEFAULT_CONFIG['ELITISM_COUNT'],
                       help='Number of elite individuals to preserve')
    
    parser.add_argument('--max-generations', type=int, default=DEFAULT_CONFIG['MAX_GENERATIONS'],
                       help='Maximum number of generations')
    
    parser.add_argument('--secret', type=int, default=None,
                       help='Secret number (if not provided, will prompt user)')
    
    parser.add_argument('--selection', type=str, default=DEFAULT_CONFIG['SELECTION_METHOD'],
                       choices=['tournament', 'roulette', 'rank'],
                       help='Selection method')
    
    parser.add_argument('--crossover', type=str, default=DEFAULT_CONFIG['CROSSOVER_METHOD'],
                       choices=['arithmetic', 'average', 'binary', 'binary_two_point', 'adaptive'],
                       help='Crossover method')
    
    parser.add_argument('--mutation', type=str, default=DEFAULT_CONFIG['MUTATION_METHOD'],
                       choices=['random', 'bit_flip', 'boundary', 'gaussian', 'adaptive'],
                       help='Mutation method')
    
    parser.add_argument('--fitness', type=str, default=DEFAULT_CONFIG['FITNESS_METHOD'],
                       choices=['linear', 'inverse', 'exponential', 'combined', 'hot_cold'],
                       help='Fitness calculation method')
    
    parser.add_argument('--config', type=str, default=None,
                       help='Path to config file')
    
    parser.add_argument('--save-config', type=str, default=None,
                       help='Save configuration to file')
    
    parser.add_argument('--save-stats', type=str, default=None,
                       help='Save statistics to file')
    
    parser.add_argument('--no-color', action='store_true',
                       help='Disable colored output')
    
    parser.add_argument('--quiet', action='store_true',
                       help='Run in quiet mode with minimal output')
    
    return parser.parse_args()


def configure_from_args(args) -> Config:
    """
    Create configuration from command-line arguments.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Config: Configuration object
    """
    # Start with default or file-based config
    if args.config and os.path.exists(args.config):
        config = Config.load(args.config)
    else:
        config = Config()
    
    # Override with command-line arguments
    config_dict = {
        'MIN_NUMBER': args.min,
        'MAX_NUMBER': args.max,
        'POPULATION_SIZE': args.population,
        'CROSSOVER_RATE': args.crossover_rate,
        'MUTATION_RATE': args.mutation_rate,
        'ELITISM_COUNT': args.elitism,
        'MAX_GENERATIONS': args.max_generations,
        'SELECTION_METHOD': args.selection,
        'CROSSOVER_METHOD': args.crossover,
        'MUTATION_METHOD': args.mutation,
        'FITNESS_METHOD': args.fitness,
        'USE_COLORS': not args.no_color,
        'VERBOSE': not args.quiet
    }
    
    # Update config with arguments
    config.update({k: v for k, v in config_dict.items() if v is not None})
    
    # Save config if requested
    if args.save_config:
        config.save(args.save_config)
    
    return config


def main():
    """
    Main entry point for the application.
    """
    # Parse command-line arguments
    args = parse_arguments()
    
    # Configure the game
    config = configure_from_args(args)
    
    # Create display
    display = Display(verbose=config.get('VERBOSE'), use_colors=config.get('USE_COLORS'))
    
    # Create statistics tracker
    stats_tracker = StatisticsTracker()
    
    # Create game manager
    game_manager = GameManager(display, config.as_dict())
    
    try:
        # Set up the game
        game_manager.setup_game()
        
        # Get the secret number (either from setup or args)
        secret_number = args.secret if args.secret is not None else game_manager.secret_number
        
        # Start tracking statistics
        stats_tracker.start_tracking(config.as_dict(), secret_number)
        
        # Initialize genetic algorithm components
        population = Population(config.as_dict())
        
        # Patch the game manager with the population
        game_manager.population = population
        
        # Define a hook to record statistics after each generation
        def after_generation_hook():
            # Get population statistics
            pop_stats = population.get_statistics()
            
            # Add some additional data
            gen_data = {
                'generation': game_manager.current_generation,
                'best_guess': pop_stats['best_guess'],
                'best_fitness': pop_stats['best_fitness'],
                'avg_fitness': pop_stats['avg_fitness'],
                'diversity': population.get_value_diversity(),
                'population_size': len(population)
            }
            
            # Record in the statistics tracker
            stats_tracker.record_generation(gen_data)
        
        # Patch the GameManager._run_generation method to use our GA components
        original_run_generation = game_manager._run_generation
        
        def patched_run_generation():
            # Evaluate fitness
            population.evaluate_fitness(secret_number)
            
            # Get the best individual
            best_individual = population.get_best_individual()
            best_fitness = best_individual.fitness
            
            # Record this generation's results
            generation_record = {
                'generation': game_manager.current_generation,
                'best_fitness': best_fitness,
                'best_guess': best_individual.value,
                'avg_fitness': population.get_average_fitness(),
            }
            game_manager.generation_history.append(generation_record)
            
            # Update best individual tracking
            game_manager.best_fitness = best_fitness
            game_manager.best_individual = best_individual
            
            # Check if the solution is found
            solution_found = best_fitness >= 99.99
            
            # If not found, create the next generation
            if not solution_found:
                population.create_next_generation()
            
            # Call the after-generation hook
            after_generation_hook()
            
            return solution_found
        
        # Replace the method
        game_manager._run_generation = patched_run_generation
        
        # Run the game
        game_manager.run_game()
        
        # End tracking statistics
        best_guess = population.get_best_individual().value if population else None
        stats_tracker.end_tracking(
            success=game_manager.best_fitness >= 99.99, 
            found_number=best_guess
        )
        
        # Save statistics if requested
        if args.save_stats:
            stats_tracker.save_to_file(args.save_stats)
            display.show_message(f"Statistics saved to {args.save_stats}", 'GREEN')
        
        # Display detailed statistics report if in verbose mode
        if config.get('VERBOSE'):
            print("\n" + stats_tracker.generate_text_report())
    
    except KeyboardInterrupt:
        display.show_message("\nGame terminated by user.", 'YELLOW')
        sys.exit(0)
    except Exception as e:
        display.show_error(f"An error occurred: {str(e)}")
        if config.get('VERBOSE'):
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()