#!/usr/bin/env python3
"""
Main entry point for the Genetic Algorithm Number Guessing Game with Pygame visualization.
"""

import os
import sys
import argparse
import time
from typing import Dict, Any, Optional

# Import game components
from game.game_manager import GameManager
from game.display import Display
from game.pygame_visualizer import PyGameVisualizer

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
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Genetic Algorithm Number Guessing Game with Visualization')
    
    # Standard arguments (same as main.py)
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
    
    # Visualization-specific arguments
    parser.add_argument('--visual-mode', type=str, default='all',
                      choices=['all', 'population', 'fitness', 'evolution', 'operations'],
                      help='Visualization mode to display')
    parser.add_argument('--window-width', type=int, default=1280,
                      help='Visualization window width')
    parser.add_argument('--window-height', type=int, default=720,
                      help='Visualization window height')
    parser.add_argument('--fps', type=int, default=60,
                      help='Frames per second for visualization')
    parser.add_argument('--speed', type=int, default=1,
                      help='Speed multiplier for evolution')
    parser.add_argument('--theme', type=str, default='default',
                      choices=['default', 'dark', 'colorblind'],
                      help='Visualization theme')
    parser.add_argument('--no-animation', action='store_true',
                      help='Disable animations')
    
    return parser.parse_args()


def configure_from_args(args):
    """Create configuration from command-line arguments."""
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
        'USE_COLORS': True,
        'VERBOSE': True
    }
    
    # Add visualization settings
    vis_config = {
        'VISUAL_MODE': args.visual_mode,
        'WINDOW_WIDTH': args.window_width,
        'WINDOW_HEIGHT': args.window_height,
        'FPS': args.fps,
        'SPEED': args.speed,
        'THEME': args.theme,
        'USE_ANIMATIONS': not args.no_animation,
    }
    config_dict.update(vis_config)
    
    # Update config with arguments
    config.update({k: v for k, v in config_dict.items() if v is not None})
    
    # Save config if requested
    if args.save_config:
        config.save(args.save_config)
    
    return config


def main():
    """Main entry point for the visualization application."""
    # Parse command-line arguments
    args = parse_arguments()
    
    # Configure the game
    config = configure_from_args(args)
    
    # Create standard display and statistics tracker
    display = Display(verbose=config.get('VERBOSE'), use_colors=config.get('USE_COLORS'))
    stats_tracker = StatisticsTracker()
    
    # Create pygame visualizer
    visualizer = PyGameVisualizer(config.as_dict())
    
    # Create game manager
    game_manager = GameManager(display, config.as_dict())
    
    # Add visualizer as observer to game manager
    game_manager.add_observer(visualizer)
    
    try:
        # Initialize pygame and display window
        visualizer.initialize()
        
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
        
        # Initialize visualizer with the population and secret number
        visualizer.setup(population, secret_number, config.as_dict())
        
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
            
            # Update visualizer
            visualizer.update_generation_data(gen_data)
        
        # Patch the GameManager._run_generation method to use our GA components
        original_run_generation = game_manager._run_generation
        
        def patched_run_generation():
            # Before generation events
            game_manager.notify_observers('before_generation', {
                'generation': game_manager.current_generation,
                'population': population
            })
            
            # Evaluate fitness
            population.evaluate_fitness(secret_number)
            
            # After fitness evaluation events
            game_manager.notify_observers('after_fitness_evaluation', {
                'population': population
            })
            
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
                # Before next generation creation
                game_manager.notify_observers('before_next_generation', {
                    'population': population
                })
                
                # Create next generation
                population.create_next_generation()
                
                # After next generation creation
                game_manager.notify_observers('after_next_generation', {
                    'population': population
                })
            
            # Call the after-generation hook
            after_generation_hook()
            
            # After generation complete events
            game_manager.notify_observers('after_generation', {
                'generation': game_manager.current_generation,
                'population': population,
                'best_individual': best_individual,
                'solution_found': solution_found
            })
            
            return solution_found
        
        # Replace the method
        game_manager._run_generation = patched_run_generation
        
        # Run the game
        visualizer.start_evolution_loop(game_manager)
        
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
        visualizer.cleanup()
        sys.exit(0)
    except Exception as e:
        display.show_error(f"An error occurred: {str(e)}")
        if config.get('VERBOSE'):
            import traceback
            traceback.print_exc()
        visualizer.cleanup()
        sys.exit(1)
    finally:
        # Clean up pygame resources
        visualizer.cleanup()


if __name__ == "__main__":
    main()