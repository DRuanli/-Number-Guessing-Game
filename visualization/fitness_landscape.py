"""
Fitness landscape visualization for the genetic algorithm.

This module visualizes the fitness function and the population's position
on the fitness landscape.
"""

import pygame
from typing import Dict, Any, List, Tuple, Optional
import math

from genetic_algorithm.fitness import FitnessCalculator
from .themes import get_fitness_color


class FitnessLandscape:
    """
    Visualizes the fitness landscape and population distribution.
    
    This component displays the fitness function as a curve and plots
    the individuals of the population on the landscape.
    """
    
    def __init__(self, rect: pygame.Rect, min_value: int, max_value: int,
                secret_number: int, fitness_method: str = 'linear', 
                theme: Dict[str, Any] = None):
        """
        Initialize the fitness landscape visualization.
        
        Args:
            rect: The component's rectangle on the screen
            min_value: The minimum possible individual value
            max_value: The maximum possible individual value
            secret_number: The target number to find
            fitness_method: The fitness calculation method
            theme: Dictionary containing theme parameters
        """
        self.rect = rect
        self.min_value = min_value
        self.max_value = max_value
        self.secret_number = secret_number
        self.fitness_method = fitness_method
        self.theme = theme or {}
        
        # Fitness calculation method
        self.fitness_func = self._get_fitness_function(fitness_method)
        
        # Visualization parameters
        self.padding = self.theme.get('padding', 10)
        self.line_width = self.theme.get('fitness_landscape_line_width', 2)
        
        # Font for labels
        font_name = self.theme.get('font_name', 'Arial')
        font_size = self.theme.get('font_size', 16)
        self.font = pygame.font.SysFont(font_name, font_size)
        
        # Pre-calculate fitness landscape
        self.landscape_points = self._calculate_landscape()
        
        # Current population
        self.population = None
    
    def _get_fitness_function(self, method: str):
        """
        Get the fitness calculation function based on method name.
        
        Args:
            method: The fitness calculation method name
            
        Returns:
            function: The fitness calculation function
        """
        # Map method names to FitnessCalculator methods
        fitness_methods = {
            'linear': FitnessCalculator.linear_distance,
            'inverse': FitnessCalculator.inverse_distance,
            'exponential': FitnessCalculator.exponential_decay,
            'combined': FitnessCalculator.combined_fitness,
            'hot_cold': lambda g, s, min_v, max_v: FitnessCalculator.hot_cold_guidance(g, s, min_v, max_v, None)
        }
        
        return fitness_methods.get(method, FitnessCalculator.linear_distance)
    
    def _calculate_landscape(self) -> List[Tuple[int, int]]:
        """
        Calculate the points for the fitness landscape curve.
        
        Returns:
            List[Tuple[int, int]]: List of (x, y) coordinate pairs
        """
        points = []
        value_range = self.max_value - self.min_value
        
        # Number of points to calculate (more for smoother curve)
        num_points = min(300, value_range + 1)
        
        # Content area inside padding
        content_width = self.rect.width - 2 * self.padding
        content_height = self.rect.height - 2 * self.padding - 30  # Extra 30px for title
        
        # Calculate points across the range
        for i in range(num_points):
            # Calculate the value at this point
            value = self.min_value + (i / (num_points - 1)) * value_range
            
            # Calculate fitness
            fitness = self.fitness_func(value, self.secret_number, self.min_value, self.max_value)
            
            # Map to screen coordinates
            x = self.rect.left + self.padding + (i / (num_points - 1)) * content_width
            y = self.rect.bottom - self.padding - (fitness / 100) * content_height
            
            points.append((x, y))
        
        return points
    
    def update_population(self, population) -> None:
        """
        Update with a new population state.
        
        Args:
            population: The current Population object
        """
        self.population = population
    
    def _value_to_x(self, value: int) -> int:
        """
        Convert a value to an x-coordinate on the screen.
        
        Args:
            value: The value to convert
            
        Returns:
            int: The x-coordinate
        """
        value_range = self.max_value - self.min_value
        if value_range == 0:
            return self.rect.left + self.rect.width // 2
        
        normalized_pos = (value - self.min_value) / value_range
        content_width = self.rect.width - 2 * self.padding
        x_pos = self.rect.left + self.padding + normalized_pos * content_width
        return int(x_pos)
    
    def _fitness_to_y(self, fitness: float) -> int:
        """
        Convert a fitness value to a y-coordinate on the screen.
        
        Args:
            fitness: The fitness value (0-100)
            
        Returns:
            int: The y-coordinate
        """
        content_height = self.rect.height - 2 * self.padding - 30  # Extra 30px for title
        y_pos = self.rect.bottom - self.padding - (fitness / 100) * content_height
        return int(y_pos)
    
    def render(self, surface, population) -> None:
        """
        Render the fitness landscape to a surface.
        
        Args:
            surface: The pygame surface to render to
            population: The current Population object
        """
        # Update population if provided
        if population and self.population != population:
            self.update_population(population)
        
        # Background
        bg_color = self.theme.get('panel_color', (220, 220, 230))
        border_color = self.theme.get('border_color', (180, 180, 190))
        
        # Draw panel background
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, border_color, self.rect, 1, border_radius=5)
        
        # Draw title
        title_font = pygame.font.SysFont(
            self.theme.get('font_name', 'Arial'),
            self.theme.get('title_font_size', 20)
        )
        method_name = self.fitness_method.capitalize().replace('_', ' ')
        title_text = title_font.render(f"Fitness Landscape ({method_name})", True,
                                      self.theme.get('text_color', (20, 20, 30)))
        title_rect = title_text.get_rect(midtop=(self.rect.centerx, self.rect.top + 5))
        surface.blit(title_text, title_rect)
        
        # Draw axes
        content_left = self.rect.left + self.padding
        content_bottom = self.rect.bottom - self.padding
        content_right = self.rect.right - self.padding
        content_top = self.rect.top + self.padding + 30  # Extra 30px for title
        
        # X-axis (value)
        pygame.draw.line(
            surface,
            self.theme.get('text_color', (20, 20, 30)),
            (content_left, content_bottom),
            (content_right, content_bottom),
            1
        )
        
        # Y-axis (fitness)
        pygame.draw.line(
            surface,
            self.theme.get('text_color', (20, 20, 30)),
            (content_left, content_bottom),
            (content_left, content_top),
            1
        )
        
        # X-axis labels
        label_font = pygame.font.SysFont(
            self.theme.get('font_name', 'Arial'),
            self.theme.get('small_font_size', 12)
        )
        
        # X-axis label
        x_label = label_font.render("Value", True, 
                                   self.theme.get('text_color', (20, 20, 30)))
        x_label_rect = x_label.get_rect(midtop=(
            content_left + (content_right - content_left) // 2,
            content_bottom + 5
        ))
        surface.blit(x_label, x_label_rect)
        
        # X-axis ticks and values
        num_ticks = 5
        for i in range(num_ticks):
            tick_value = self.min_value + (i / (num_ticks - 1)) * (self.max_value - self.min_value)
            tick_x = content_left + (i / (num_ticks - 1)) * (content_right - content_left)
            
            # Draw tick
            pygame.draw.line(
                surface,
                self.theme.get('text_color', (20, 20, 30)),
                (tick_x, content_bottom),
                (tick_x, content_bottom + 5),
                1
            )
            
            # Draw value
            value_label = label_font.render(str(int(tick_value)), True,
                                          self.theme.get('text_color', (20, 20, 30)))
            value_rect = value_label.get_rect(midtop=(tick_x, content_bottom + 5))
            surface.blit(value_label, value_rect)
        
        # Y-axis label
        y_label = label_font.render("Fitness", True,
                                   self.theme.get('text_color', (20, 20, 30)))
        y_label_rect = y_label.get_rect(center=(
            content_left - 25,
            content_top + (content_bottom - content_top) // 2
        ))
        
        # Rotate and blit Y-axis label
        rotated_y_label = pygame.transform.rotate(y_label, 90)
        surface.blit(rotated_y_label, 
                   (y_label_rect.x - rotated_y_label.get_width() // 2, 
                    y_label_rect.y - rotated_y_label.get_height() // 2))
        
        # Y-axis ticks and values
        num_ticks = 5
        for i in range(num_ticks):
            tick_fitness = i * (100 / (num_ticks - 1))
            tick_y = content_bottom - (i / (num_ticks - 1)) * (content_bottom - content_top)
            
            # Draw tick
            pygame.draw.line(
                surface,
                self.theme.get('text_color', (20, 20, 30)),
                (content_left - 5, tick_y),
                (content_left, tick_y),
                1
            )
            
            # Draw value
            fitness_label = label_font.render(f"{tick_fitness:.0f}", True,
                                            self.theme.get('text_color', (20, 20, 30)))
            fitness_rect = fitness_label.get_rect(midright=(content_left - 7, tick_y))
            surface.blit(fitness_label, fitness_rect)
        
        # Draw fitness landscape curve
        if self.landscape_points:
            pygame.draw.lines(
                surface,
                self.theme.get('highlight_color', (70, 130, 180)),
                False,
                self.landscape_points,
                self.line_width
            )
        
        # Draw secret number line
        secret_x = self._value_to_x(self.secret_number)
        pygame.draw.line(
            surface,
            self.theme.get('secret_color', (70, 20, 170)),
            (secret_x, content_top),
            (secret_x, content_bottom),
            1
        )
        
        # Secret number label
        secret_label = label_font.render("Target", True,
                                       self.theme.get('secret_color', (70, 20, 170)))
        secret_rect = secret_label.get_rect(midbottom=(secret_x, content_top - 5))
        surface.blit(secret_label, secret_rect)
        
        # Draw population individuals on the landscape
        if self.population:
            for individual in self.population.individuals:
                x = self._value_to_x(individual.value)
                y = self._fitness_to_y(individual.fitness)
                
                # Draw individual as circle with color based on fitness
                color = get_fitness_color(self.theme, individual.fitness)
                pygame.draw.circle(surface, color, (x, y), 4)
                
                # For best individual, add highlight
                if individual.fitness == self.population.get_best_individual().fitness:
                    pygame.draw.circle(surface, self.theme.get('highlight_color', (70, 130, 180)),
                                     (x, y), 6, 2)