"""
Statistics dashboard visualization for the genetic algorithm.

This module provides a real-time dashboard of statistics and metrics
about the genetic algorithm's performance.
"""

import pygame
from typing import Dict, Any, List, Tuple, Optional
import time
import math


class StatsDashboard:
    """
    Displays real-time statistics about the genetic algorithm.
    
    This component shows key metrics like best fitness, average fitness,
    diversity, and generation count in a compact dashboard format.
    """
    
    def __init__(self, rect: pygame.Rect, min_value: int, max_value: int,
                config: Dict[str, Any], theme: Dict[str, Any] = None):
        """
        Initialize the statistics dashboard.
        
        Args:
            rect: The component's rectangle on the screen
            min_value: The minimum possible individual value
            max_value: The maximum possible individual value
            config: Dictionary containing configuration parameters
            theme: Dictionary containing theme parameters
        """
        self.rect = rect
        self.min_value = min_value
        self.max_value = max_value
        self.config = config
        self.theme = theme or {}
        
        # Statistics data
        self.generation = 0
        self.best_fitness = 0.0
        self.best_guess = None
        self.avg_fitness = 0.0
        self.diversity = 0.0
        self.population_size = 0
        self.start_time = time.time()
        
        # Performance metrics
        self.evaluations = 0
        self.evaluations_per_second = 0.0
        self.generations_per_second = 0.0
        self.estimated_generations_to_solution = float('inf')
        
        # Visualization parameters
        self.padding = self.theme.get('padding', 10)
        
        # Font for labels
        font_name = self.theme.get('font_name', 'Arial')
        font_size = self.theme.get('font_size', 16)
        self.font = pygame.font.SysFont(font_name, font_size)
        self.small_font = pygame.font.SysFont(
            font_name,
            self.theme.get('small_font_size', 12)
        )
    
    def update_data(self, data: Dict[str, Any]) -> None:
        """
        Update dashboard with new generation data.
        
        Args:
            data: Dictionary containing generation statistics
        """
        # Update basic statistics
        self.generation = data.get('generation', self.generation)
        self.best_fitness = data.get('best_fitness', self.best_fitness)
        self.best_guess = data.get('best_guess', self.best_guess)
        self.avg_fitness = data.get('avg_fitness', self.avg_fitness)
        self.diversity = data.get('diversity', self.diversity)
        self.population_size = data.get('population_size', self.population_size)
        
        # Update performance metrics
        if self.generation > 0:
            elapsed_time = time.time() - self.start_time
            if elapsed_time > 0:
                self.evaluations = self.generation * self.population_size
                self.evaluations_per_second = self.evaluations / elapsed_time
                self.generations_per_second = self.generation / elapsed_time
                
                # Estimate generations to solution
                if self.best_fitness < 99.9 and self.best_fitness > 0:
                    # Simple linear extrapolation based on current progress
                    progress_rate = self.best_fitness / self.generation
                    self.estimated_generations_to_solution = (100 - self.best_fitness) / progress_rate + self.generation
                else:
                    self.estimated_generations_to_solution = self.generation
    
    def reset(self) -> None:
        """Reset the dashboard statistics."""
        self.generation = 0
        self.best_fitness = 0.0
        self.best_guess = None
        self.avg_fitness = 0.0
        self.diversity = 0.0
        self.population_size = 0
        self.start_time = time.time()
        self.evaluations = 0
        self.evaluations_per_second = 0.0
        self.generations_per_second = 0.0
        self.estimated_generations_to_solution = float('inf')
    
    def render(self, surface) -> None:
        """
        Render the statistics dashboard to a surface.
        
        Args:
            surface: The pygame surface to render to
        """
        # Background
        bg_color = self.theme.get('panel_color', (220, 220, 230))
        border_color = self.theme.get('border_color', (180, 180, 190))
        
        # Draw panel background
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, border_color, self.rect, 1, border_radius=5)
        
        # Layout calculation
        metric_width = self.rect.width // 3
        left_metrics_x = self.rect.left + self.padding
        center_metrics_x = left_metrics_x + metric_width
        right_metrics_x = center_metrics_x + metric_width
        
        # Draw generation counter
        generation_text = f"Generation: {self.generation}"
        generation_color = self.theme.get('text_color', (20, 20, 30))
        
        generation_surface = self.font.render(generation_text, True, generation_color)
        generation_rect = generation_surface.get_rect(topleft=(
            left_metrics_x,
            self.rect.top + self.padding
        ))
        surface.blit(generation_surface, generation_rect)
        
        # Draw best fitness with progress bar
        best_fitness_label = "Best Fitness:"
        label_surface = self.small_font.render(best_fitness_label, True, generation_color)
        label_rect = label_surface.get_rect(topleft=(
            left_metrics_x,
            generation_rect.bottom + 8
        ))
        surface.blit(label_surface, label_rect)
        
        # Progress bar background
        bar_width = metric_width - 10
        bar_height = 15
        bar_x = left_metrics_x
        bar_y = label_rect.bottom + 3
        bar_bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(surface, self.theme.get('slider_track_color', (200, 200, 210)), bar_bg_rect, border_radius=3)
        
        # Progress bar fill
        fill_width = int((self.best_fitness / 100) * bar_width)
        fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
        
        # Gradient color based on progress
        progress_color = self.theme.get('best_fitness_color', (0, 120, 0))
        if self.best_fitness < 50:
            progress_color = self.theme.get('avg_fitness_color', (0, 80, 140))
        
        pygame.draw.rect(surface, progress_color, fill_rect, border_radius=3)
        
        # Fitness value on the progress bar
        fitness_text = f"{self.best_fitness:.2f}%"
        fitness_surface = self.small_font.render(fitness_text, True, (255, 255, 255))
        fitness_rect = fitness_surface.get_rect(center=(
            bar_x + fill_width // 2,
            bar_y + bar_height // 2
        ))
        
        # Only show text if it fits in the filled portion
        if fill_width >= fitness_surface.get_width():
            surface.blit(fitness_surface, fitness_rect)
        else:
            # Show text in default color to the right of the bar
            alt_fitness_surface = self.small_font.render(fitness_text, True, generation_color)
            alt_fitness_rect = alt_fitness_surface.get_rect(midleft=(
                bar_x + fill_width + 5,
                bar_y + bar_height // 2
            ))
            surface.blit(alt_fitness_surface, alt_fitness_rect)
        
        # Draw best guess
        if self.best_guess is not None:
            best_guess_text = f"Best Guess: {self.best_guess}"
            guess_surface = self.font.render(best_guess_text, True, generation_color)
            guess_rect = guess_surface.get_rect(topleft=(
                center_metrics_x,
                self.rect.top + self.padding
            ))
            surface.blit(guess_surface, guess_rect)
        
        # Draw average fitness
        avg_fitness_text = f"Avg Fitness: {self.avg_fitness:.2f}%"
        avg_surface = self.small_font.render(avg_fitness_text, True, generation_color)
        avg_rect = avg_surface.get_rect(topleft=(
            center_metrics_x,
            generation_rect.bottom + 8
        ))
        surface.blit(avg_surface, avg_rect)
        
        # Draw diversity
        diversity_text = f"Diversity: {self.diversity * 100:.1f}%"
        diversity_surface = self.small_font.render(diversity_text, True, generation_color)
        diversity_rect = diversity_surface.get_rect(topleft=(
            center_metrics_x,
            avg_rect.bottom + 5
        ))
        surface.blit(diversity_surface, diversity_rect)
        
        # Draw performance metrics on the right
        elapsed_time = time.time() - self.start_time
        time_text = f"Time: {self._format_time(elapsed_time)}"
        time_surface = self.font.render(time_text, True, generation_color)
        time_rect = time_surface.get_rect(topleft=(
            right_metrics_x,
            self.rect.top + self.padding
        ))
        surface.blit(time_surface, time_rect)
        
        # Generations per second
        gen_rate_text = f"Speed: {self.generations_per_second:.1f} gen/s"
        gen_rate_surface = self.small_font.render(gen_rate_text, True, generation_color)
        gen_rate_rect = gen_rate_surface.get_rect(topleft=(
            right_metrics_x,
            time_rect.bottom + 8
        ))
        surface.blit(gen_rate_surface, gen_rate_rect)
        
        # Estimated time to solution
        if self.estimated_generations_to_solution < float('inf') and self.generations_per_second > 0:
            gens_remaining = max(0, self.estimated_generations_to_solution - self.generation)
            time_remaining = gens_remaining / self.generations_per_second
            
            est_text = f"Est. remaining: {self._format_time(time_remaining)}"
            est_surface = self.small_font.render(est_text, True, generation_color)
            est_rect = est_surface.get_rect(topleft=(
                right_metrics_x,
                gen_rate_rect.bottom + 5
            ))
            surface.blit(est_surface, est_rect)
    
    def _format_time(self, seconds: float) -> str:
        """
        Format time in seconds to a readable string.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            str: Formatted time string
        """
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            seconds = seconds % 60
            return f"{minutes}m {int(seconds)}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"