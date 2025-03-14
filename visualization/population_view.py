"""
Population visualization component for the genetic algorithm.

This module visualizes the population of individuals on a number line,
with color coding based on fitness.
"""

import pygame
from typing import Dict, Any, List, Tuple, Optional
import math

from .themes import get_fitness_color


class PopulationView:
    """
    Visualizes the population of individuals in the genetic algorithm.
    
    This component displays individuals as circles on a number line,
    with positions based on their values and colors based on fitness.
    """
    
    def __init__(self, rect: pygame.Rect, min_value: int, max_value: int, 
                secret_number: int, theme: Dict[str, Any] = None):
        """
        Initialize the population view.
        
        Args:
            rect: The component's rectangle on the screen
            min_value: The minimum possible individual value
            max_value: The maximum possible individual value
            secret_number: The target number to find
            theme: Dictionary containing theme parameters
        """
        self.rect = rect
        self.min_value = min_value
        self.max_value = max_value
        self.secret_number = secret_number
        self.theme = theme or {}
        
        # Individual visualization parameters
        self.individual_radius = self.theme.get('population_individual_radius', 5)
        self.padding = self.theme.get('padding', 10)
        
        # Font for labels
        font_name = self.theme.get('font_name', 'Arial')
        font_size = self.theme.get('font_size', 16)
        self.font = pygame.font.SysFont(font_name, font_size)
        
        # Previous population state for animations
        self.prev_individuals = []
        self.animation_progress = 1.0  # 0.0-1.0, 1.0 means animation complete
        
        # Best individual tracking
        self.best_individual = None
        self.best_radius_factor = 1.0  # For pulsing animation
        self.pulse_direction = 0.05
    
    def update_population(self, population) -> None:
        """
        Update with a new population state.
        
        Args:
            population: The current Population object
        """
        # Store previous individuals for animation
        self.prev_individuals = self.current_individuals if hasattr(self, 'current_individuals') else []
        
        # Store current population individuals
        self.current_individuals = [
            {
                'value': ind.value,
                'fitness': ind.fitness,
                'position': self._calculate_position(ind.value)
            }
            for ind in population.individuals
        ]
        
        # Find the best individual
        self.best_individual = max(self.current_individuals, key=lambda ind: ind['fitness']) \
            if self.current_individuals else None
        
        # Reset animation
        self.animation_progress = 0.0
    
    def _calculate_position(self, value: int) -> int:
        """
        Calculate the x-position for a value on the number line.
        
        Args:
            value: The individual's value
            
        Returns:
            int: The x-coordinate for the value
        """
        value_range = self.max_value - self.min_value
        if value_range == 0:
            return self.rect.left + self.rect.width // 2
        
        # Linear mapping from value range to pixel range
        normalized_pos = (value - self.min_value) / value_range
        x_pos = self.rect.left + self.padding + normalized_pos * (self.rect.width - 2 * self.padding)
        return int(x_pos)
    
    def _value_at_position(self, x_pos: int) -> int:
        """
        Calculate the value at a given x-position on the number line.
        
        Args:
            x_pos: The x-coordinate
            
        Returns:
            int: The value at that position
        """
        if x_pos <= self.rect.left + self.padding:
            return self.min_value
        if x_pos >= self.rect.right - self.padding:
            return self.max_value
        
        # Linear mapping from pixel range to value range
        normalized_pos = (x_pos - (self.rect.left + self.padding)) / (self.rect.width - 2 * self.padding)
        value = self.min_value + normalized_pos * (self.max_value - self.min_value)
        return int(value)
    
    def render(self, surface, population) -> None:
        """
        Render the population view to a surface.
        
        Args:
            surface: The pygame surface to render to
            population: The current Population object
        """
        # Update animation progress
        if self.animation_progress < 1.0:
            self.animation_progress += self.theme.get('animation_speed', 0.3)
            if self.animation_progress > 1.0:
                self.animation_progress = 1.0
        
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
        title_text = title_font.render("Population Distribution", True,
                                     self.theme.get('text_color', (20, 20, 30)))
        title_rect = title_text.get_rect(midtop=(self.rect.centerx, self.rect.top + 5))
        surface.blit(title_text, title_rect)
        
        # Draw number line
        line_y = self.rect.centery + 20
        line_width = self.rect.width - 2 * self.padding
        pygame.draw.line(
            surface,
            self.theme.get('text_color', (20, 20, 30)),
            (self.rect.left + self.padding, line_y),
            (self.rect.right - self.padding, line_y),
            2
        )
        
        # Draw number line ticks and labels
        tick_count = min(10, self.max_value - self.min_value + 1)
        for i in range(tick_count):
            tick_value = self.min_value + i * ((self.max_value - self.min_value) / (tick_count - 1))
            tick_x = self._calculate_position(tick_value)
            
            # Draw tick
            pygame.draw.line(
                surface,
                self.theme.get('text_color', (20, 20, 30)),
                (tick_x, line_y - 5),
                (tick_x, line_y + 5),
                1
            )
            
            # Draw label
            label_text = str(int(tick_value))
            label_surface = self.font.render(label_text, True, 
                                           self.theme.get('text_color', (20, 20, 30)))
            label_rect = label_surface.get_rect(midtop=(tick_x, line_y + 5))
            surface.blit(label_surface, label_rect)
        
        # Draw secret number marker
        secret_x = self._calculate_position(self.secret_number)
        secret_color = self.theme.get('secret_color', (70, 20, 170))
        
        # Draw triangle pointing down to the secret number
        triangle_points = [
            (secret_x, line_y - 15),
            (secret_x - 10, line_y - 25),
            (secret_x + 10, line_y - 25)
        ]
        pygame.draw.polygon(surface, secret_color, triangle_points)
        
        # Draw "Target" label
        target_text = self.font.render("Target", True, secret_color)
        target_rect = target_text.get_rect(midbottom=(secret_x, line_y - 25))
        surface.blit(target_text, target_rect)
        
        # Draw individuals
        if hasattr(self, 'current_individuals'):
            # Animation for best individual (pulsing)
            if self.best_individual:
                self.best_radius_factor += self.pulse_direction
                if self.best_radius_factor > 1.5 or self.best_radius_factor < 1.0:
                    self.pulse_direction *= -1
            
            # Sort by fitness (low to high) so better individuals are drawn on top
            sorted_individuals = sorted(self.current_individuals, key=lambda x: x['fitness'])
            
            # Draw each individual
            for individual in sorted_individuals:
                # Calculate position with animation
                if self.animation_progress < 1.0 and self.prev_individuals:
                    # Find the same individual in the previous generation
                    prev_individual = next(
                        (p for p in self.prev_individuals if p['value'] == individual['value']),
                        None
                    )
                    
                    # If found, animate movement
                    if prev_individual:
                        x_pos = prev_individual['position'] + (individual['position'] - prev_individual['position']) * self.animation_progress
                    else:
                        # New individual, fade in from the edges
                        if individual['value'] < self.secret_number:
                            start_pos = self.rect.left
                        else:
                            start_pos = self.rect.right
                        x_pos = start_pos + (individual['position'] - start_pos) * self.animation_progress
                else:
                    x_pos = individual['position']
                
                # Determine size based on fitness
                fitness_factor = (individual['fitness'] / 100) * 0.5 + 0.5  # Scale factor 0.5-1.0
                radius = self.individual_radius * (1 + fitness_factor)
                
                # Special treatment for best individual
                is_best = self.best_individual and individual['value'] == self.best_individual['value']
                if is_best:
                    radius *= self.best_radius_factor
                
                # Draw individual
                y_pos = line_y - 20 - radius  # Position above the number line
                color = get_fitness_color(self.theme, individual['fitness'])
                
                # Draw circle
                pygame.draw.circle(surface, color, (x_pos, y_pos), radius)
                
                # For best individual, add outline
                if is_best:
                    pygame.draw.circle(surface, self.theme.get('highlight_color', (70, 130, 180)),
                                     (x_pos, y_pos), radius, 2)
                
                # Add value label for the best individual or individuals with high fitness
                if is_best or individual['fitness'] > 90:
                    value_text = self.font.render(str(individual['value']), True, (255, 255, 255))
                    value_rect = value_text.get_rect(center=(x_pos, y_pos))
                    
                    # Draw shadow for better readability
                    shadow_surface = self.font.render(str(individual['value']), True, (0, 0, 0))
                    shadow_rect = shadow_surface.get_rect(center=(x_pos + 1, y_pos + 1))
                    surface.blit(shadow_surface, shadow_rect)
                    surface.blit(value_text, value_rect)
        
        # Draw population statistics
        if hasattr(population, 'get_statistics'):
            stats = population.get_statistics()
            
            # Prepare stats text
            stats_font = pygame.font.SysFont(
                self.theme.get('font_name', 'Arial'),
                self.theme.get('small_font_size', 12)
            )
            
            stats_text = [
                f"Population Size: {len(population.individuals)}",
                f"Unique Values: {stats.get('unique_values', 0)}",
                f"Best Guess: {stats.get('best_guess', '?')}",
            ]
            
            # Draw stats
            y_offset = self.rect.bottom - 50
            for text in stats_text:
                text_surface = stats_font.render(text, True, 
                                               self.theme.get('text_color', (20, 20, 30)))
                text_rect = text_surface.get_rect(bottomright=(self.rect.right - 10, y_offset))
                surface.blit(text_surface, text_rect)
                y_offset += 15