"""
PyGame Visualizer for the Genetic Algorithm Number Guessing Game.

This module provides visualization of the genetic algorithm's operation using
Pygame, including population visualization, fitness landscapes, and statistics.
"""

import os
import sys
import time
import pygame
from typing import Dict, Any, List, Tuple, Optional, Union, Callable

# Import visualization components
from visualization.population_view import PopulationView
from visualization.fitness_landscape import FitnessLandscape
from visualization.evolution_chart import EvolutionChart
from visualization.operations_view import OperationsView
from visualization.stats_dashboard import StatsDashboard
from visualization.ui_components import Button, Slider, ToggleButton, TextBox
from visualization.themes import get_theme


class PyGameVisualizer:
    """
    Manages the visualization of the genetic algorithm using Pygame.
    
    This class handles the Pygame window, event processing, and coordinates
    the various visualization components.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the PyGame visualizer with configuration.
        
        Args:
            config: Dictionary containing visualization configuration
        """
        self.config = config
        self.window_width = config.get('WINDOW_WIDTH', 1280)
        self.window_height = config.get('WINDOW_HEIGHT', 720)
        self.fps = config.get('FPS', 60)
        self.speed = config.get('SPEED', 1)
        self.theme_name = config.get('THEME', 'default')
        self.use_animations = config.get('USE_ANIMATIONS', True)
        self.visual_mode = config.get('VISUAL_MODE', 'all')
        
        # Pygame objects
        self.screen = None
        self.clock = None
        self.font = None
        self.theme = None
        
        # Game state
        self.population = None
        self.secret_number = None
        self.running = False
        self.paused = False
        self.evolution_step = 0
        self.generation_data = []
        self.current_generation = 0
        self.solution_found = False
        
        # Visualization components
        self.population_view = None
        self.fitness_landscape = None
        self.evolution_chart = None
        self.operations_view = None
        self.stats_dashboard = None
        
        # UI controls
        self.controls = {}
        self.active_component = None
    
    def initialize(self) -> None:
        """Initialize Pygame and set up the display window."""
        # Initialize pygame
        pygame.init()
        pygame.font.init()
        
        # Create window
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Genetic Algorithm Visualization")
        
        # Initialize clock and theme
        self.clock = pygame.time.Clock()
        self.theme = get_theme(self.theme_name)
        
        # Set up fonts
        self.font = pygame.font.SysFont(self.theme['font_name'], self.theme['font_size'])
        
        # Set icon if available
        icon_path = os.path.join(os.path.dirname(__file__), '../visualization/assets/icon.png')
        if os.path.exists(icon_path):
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
    
    def setup(self, population, secret_number: int, config: Dict[str, Any]) -> None:
        """
        Set up the visualizer with the initial game state.
        
        Args:
            population: The Population object
            secret_number: The secret number to guess
            config: Dictionary containing configuration parameters
        """
        self.population = population
        self.secret_number = secret_number
        
        # Calculate layout based on visual_mode
        self._setup_layout()
        
        # Initialize visualization components
        min_value = config.get('MIN_NUMBER', 1)
        max_value = config.get('MAX_NUMBER', 100)
        
        # Create visualization components based on mode
        if self.visual_mode in ['all', 'population']:
            self.population_view = PopulationView(
                self.layout['population_view'],
                min_value, max_value,
                secret_number,
                self.theme
            )
        
        if self.visual_mode in ['all', 'fitness']:
            self.fitness_landscape = FitnessLandscape(
                self.layout['fitness_landscape'],
                min_value, max_value,
                secret_number,
                config.get('FITNESS_METHOD', 'linear'),
                self.theme
            )
        
        if self.visual_mode in ['all', 'evolution']:
            self.evolution_chart = EvolutionChart(
                self.layout['evolution_chart'],
                config.get('MAX_GENERATIONS', 1000),
                self.theme
            )
        
        if self.visual_mode in ['all', 'operations']:
            self.operations_view = OperationsView(
                self.layout['operations_view'],
                min_value, max_value,
                self.theme
            )
        
        # Stats dashboard is always shown
        self.stats_dashboard = StatsDashboard(
            self.layout['stats_dashboard'],
            min_value, max_value,
            config,
            self.theme
        )
        
        # Set up UI controls
        self._setup_controls()
    
    def _setup_layout(self) -> None:
        """Set up the layout of visualization components based on visual_mode."""
        self.layout = {}
        
        if self.visual_mode == 'all':
            # Full dashboard with all components
            self.layout = {
                'population_view': pygame.Rect(10, 10, self.window_width - 20, 200),
                'fitness_landscape': pygame.Rect(10, 220, (self.window_width - 30) // 2, 200),
                'evolution_chart': pygame.Rect((self.window_width - 30) // 2 + 20, 220, (self.window_width - 30) // 2, 200),
                'operations_view': pygame.Rect(10, 430, self.window_width - 20, 180),
                'stats_dashboard': pygame.Rect(10, 620, self.window_width - 20, 90),
                'controls': pygame.Rect(10, self.window_height - 50, self.window_width - 20, 40)
            }
        elif self.visual_mode == 'population':
            # Focused view on population
            self.layout = {
                'population_view': pygame.Rect(10, 10, self.window_width - 20, self.window_height - 160),
                'stats_dashboard': pygame.Rect(10, self.window_height - 140, self.window_width - 20, 90),
                'controls': pygame.Rect(10, self.window_height - 50, self.window_width - 20, 40)
            }
        elif self.visual_mode == 'fitness':
            # Focused view on fitness landscape
            self.layout = {
                'fitness_landscape': pygame.Rect(10, 10, self.window_width - 20, self.window_height - 160),
                'stats_dashboard': pygame.Rect(10, self.window_height - 140, self.window_width - 20, 90),
                'controls': pygame.Rect(10, self.window_height - 50, self.window_width - 20, 40)
            }
        elif self.visual_mode == 'evolution':
            # Focused view on evolution chart
            self.layout = {
                'evolution_chart': pygame.Rect(10, 10, self.window_width - 20, self.window_height - 160),
                'stats_dashboard': pygame.Rect(10, self.window_height - 140, self.window_width - 20, 90),
                'controls': pygame.Rect(10, self.window_height - 50, self.window_width - 20, 40)
            }
        elif self.visual_mode == 'operations':
            # Focused view on genetic operations
            self.layout = {
                'operations_view': pygame.Rect(10, 10, self.window_width - 20, self.window_height - 160),
                'stats_dashboard': pygame.Rect(10, self.window_height - 140, self.window_width - 20, 90),
                'controls': pygame.Rect(10, self.window_height - 50, self.window_width - 20, 40)
            }
    
    def _setup_controls(self) -> None:
        """Set up the UI controls for interaction."""
        controls_rect = self.layout['controls']
        button_width = 100
        button_height = 30
        slider_width = 150
        padding = 10
        
        # Create buttons
        x_pos = controls_rect.left
        
        # Play/Pause button
        self.controls['play_pause'] = ToggleButton(
            pygame.Rect(x_pos, controls_rect.top, button_width, button_height),
            "Pause", "Play",
            self._toggle_pause,
            self.theme
        )
        x_pos += button_width + padding
        
        # Step button (for stepping through generations when paused)
        self.controls['step'] = Button(
            pygame.Rect(x_pos, controls_rect.top, button_width, button_height),
            "Step",
            self._step_evolution,
            self.theme
        )
        x_pos += button_width + padding
        
        # Reset button
        self.controls['reset'] = Button(
            pygame.Rect(x_pos, controls_rect.top, button_width, button_height),
            "Reset",
            self._reset_evolution,
            self.theme
        )
        x_pos += button_width + padding
        
        # Speed slider
        self.controls['speed_label'] = TextBox(
            pygame.Rect(x_pos, controls_rect.top, 50, button_height),
            "Speed:",
            self.theme
        )
        x_pos += 50 + 5
        
        self.controls['speed'] = Slider(
            pygame.Rect(x_pos, controls_rect.top, slider_width, button_height),
            1, 10, self.speed,
            self._change_speed,
            self.theme
        )
        x_pos += slider_width + padding
        
        # Screenshot button
        self.controls['screenshot'] = Button(
            pygame.Rect(x_pos, controls_rect.top, button_width, button_height),
            "Screenshot",
            self._take_screenshot,
            self.theme
        )
    
    def update_generation_data(self, data: Dict[str, Any]) -> None:
        """
        Update with new generation data.
        
        Args:
            data: Dictionary containing generation statistics
        """
        self.generation_data.append(data)
        self.current_generation = data['generation']
        
        # Update stats dashboard
        if self.stats_dashboard:
            self.stats_dashboard.update_data(data)
        
        # Update evolution chart
        if self.evolution_chart:
            self.evolution_chart.update_data(self.generation_data)
    
    def start_evolution_loop(self, game_manager) -> None:
        """
        Start the main evolution and visualization loop.
        
        Args:
            game_manager: The GameManager object controlling the algorithm
        """
        self.running = True
        self.paused = False
        
        # Main loop
        while self.running:
            # Process events
            self._process_events()
            
            # Update logic (if not paused)
            if not self.paused:
                # Run a generation of the genetic algorithm
                if self.current_generation < self.config.get('MAX_GENERATIONS', 1000) and not self.solution_found:
                    # Run at the specified speed (multiple generations per frame if speed > 1)
                    for _ in range(self.speed):
                        solution_found = game_manager._run_generation()
                        if solution_found or self.current_generation >= self.config.get('MAX_GENERATIONS', 1000):
                            self.solution_found = solution_found
                            break
            
            # Render visualization
            self._render()
            
            # Cap the frame rate
            self.clock.tick(self.fps)
    
    def _process_events(self) -> None:
        """Process pygame events."""
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                self.running = False
            
            # Keyboard events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self._toggle_pause()
                elif event.key == pygame.K_RIGHT and self.paused:
                    self._step_evolution()
                elif event.key == pygame.K_s:
                    self._take_screenshot()
            
            # Mouse events for controls
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                mouse_pos = pygame.mouse.get_pos()
                mouse_buttons = pygame.mouse.get_pressed()
                
                # Pass event to controls
                for control_name, control in self.controls.items():
                    if hasattr(control, 'handle_event'):
                        control.handle_event(event, mouse_pos, mouse_buttons)
    
    def _render(self) -> None:
        """Render all visualization components to the screen."""
        # Clear the screen
        self.screen.fill(self.theme['background_color'])
        
        # Render visualization components if they exist
        if self.population_view and self.population:
            self.population_view.render(self.screen, self.population)
        
        if self.fitness_landscape and self.population:
            self.fitness_landscape.render(self.screen, self.population)
        
        if self.evolution_chart:
            self.evolution_chart.render(self.screen)
        
        if self.operations_view and self.population:
            self.operations_view.render(self.screen, self.population)
        
        if self.stats_dashboard:
            self.stats_dashboard.render(self.screen)
        
        # Render controls
        for control_name, control in self.controls.items():
            control.render(self.screen)
        
        # Show solution found message if applicable
        if self.solution_found:
            font = pygame.font.SysFont(self.theme['font_name'], 32)
            text = font.render("SOLUTION FOUND!", True, self.theme['success_color'])
            text_rect = text.get_rect(center=(self.window_width // 2, 30))
            pygame.draw.rect(self.screen, self.theme['panel_color'], 
                           pygame.Rect(text_rect.left - 10, text_rect.top - 5, 
                                     text_rect.width + 20, text_rect.height + 10))
            self.screen.blit(text, text_rect)
        
        # Update the display
        pygame.display.flip()
    
    def _toggle_pause(self) -> None:
        """Toggle the pause state of the evolution."""
        self.paused = not self.paused
        self.controls['play_pause'].toggle()
    
    def _step_evolution(self) -> None:
        """Advance one generation when in paused state."""
        if self.paused:
            self.evolution_step += 1
    
    def _reset_evolution(self) -> None:
        """Reset the evolution process."""
        self.evolution_step = 0
        self.current_generation = 0
        self.generation_data = []
        
        if self.evolution_chart:
            self.evolution_chart.reset()
        
        if self.stats_dashboard:
            self.stats_dashboard.reset()
        
        # Reset Population would need to be handled by the game_manager
    
    def _change_speed(self, new_speed: int) -> None:
        """
        Change the speed of the evolution.
        
        Args:
            new_speed: The new speed multiplier (1-10)
        """
        self.speed = new_speed
    
    def _take_screenshot(self) -> None:
        """Take a screenshot of the current visualization state."""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"ga_visualization_{timestamp}.png"
        pygame.image.save(self.screen, filename)
        print(f"Screenshot saved as {filename}")
    
    def cleanup(self) -> None:
        """Clean up pygame resources before exiting."""
        pygame.quit()
    
    # Observer pattern methods
    def on_before_generation(self, data) -> None:
        """Handle before_generation event."""
        if self.operations_view:
            self.operations_view.prepare_new_generation(data['population'])
    
    def on_after_fitness_evaluation(self, data) -> None:
        """Handle after_fitness_evaluation event."""
        if self.fitness_landscape:
            self.fitness_landscape.update_population(data['population'])
        
        if self.population_view:
            self.population_view.update_population(data['population'])
    
    def on_before_next_generation(self, data) -> None:
        """Handle before_next_generation event."""
        if self.operations_view:
            self.operations_view.prepare_genetic_operations(data['population'])
    
    def on_after_next_generation(self, data) -> None:
        """Handle after_next_generation event."""
        if self.operations_view:
            self.operations_view.finish_genetic_operations(data['population'])
    
    def on_after_generation(self, data) -> None:
        """Handle after_generation event."""
        if data['solution_found']:
            self.solution_found = True