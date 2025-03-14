"""
Evolution chart visualization for the genetic algorithm.

This module visualizes the fitness trends and diversity metrics
over generations, showing the algorithm's progress.
"""

import pygame
from typing import Dict, Any, List, Tuple, Optional
import math

from .ui_components import draw_line_chart


class EvolutionChart:
    """
    Visualizes the evolution of fitness and diversity over generations.
    
    This component displays line charts of fitness trends and other metrics
    to show how the genetic algorithm is progressing.
    """
    
    def __init__(self, rect: pygame.Rect, max_generations: int = 100, 
                theme: Dict[str, Any] = None):
        """
        Initialize the evolution chart.
        
        Args:
            rect: The component's rectangle on the screen
            max_generations: The maximum number of generations to display
            theme: Dictionary containing theme parameters
        """
        self.rect = rect
        self.max_generations = max_generations
        self.theme = theme or {}
        
        # Visualization parameters
        self.padding = self.theme.get('padding', 10)
        self.line_width = self.theme.get('evolution_chart_line_width', 2)
        
        # Font for labels
        font_name = self.theme.get('font_name', 'Arial')
        font_size = self.theme.get('font_size', 16)
        self.font = pygame.font.SysFont(font_name, font_size)
        
        # Data storage
        self.best_fitness_data = []
        self.avg_fitness_data = []
        self.diversity_data = []
        self.generation_numbers = []
        
        # Chart dimensions
        self.chart_height = (self.rect.height - 3 * self.padding - 30) // 2  # 30px for title
    
    def update_data(self, generation_data: List[Dict[str, Any]]) -> None:
        """
        Update with new generation data.
        
        Args:
            generation_data: List of generation data dictionaries
        """
        # Clear previous data
        self.best_fitness_data = []
        self.avg_fitness_data = []
        self.diversity_data = []
        self.generation_numbers = []
        
        # Add data from each generation
        for gen_data in generation_data:
            self.generation_numbers.append(gen_data.get('generation', 0))
            self.best_fitness_data.append(gen_data.get('best_fitness', 0))
            self.avg_fitness_data.append(gen_data.get('avg_fitness', 0))
            self.diversity_data.append(gen_data.get('diversity', 0) * 100)  # Convert to percentage
    
    def reset(self) -> None:
        """Reset the chart data."""
        self.best_fitness_data = []
        self.avg_fitness_data = []
        self.diversity_data = []
        self.generation_numbers = []
    
    def render(self, surface) -> None:
        """
        Render the evolution chart to a surface.
        
        Args:
            surface: The pygame surface to render to
        """
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
        title_text = title_font.render("Evolution Progress", True,
                                      self.theme.get('text_color', (20, 20, 30)))
        title_rect = title_text.get_rect(midtop=(self.rect.centerx, self.rect.top + 5))
        surface.blit(title_text, title_rect)
        
        # Calculate chart positions
        top_chart_rect = pygame.Rect(
            self.rect.left + self.padding,
            self.rect.top + self.padding + 30,  # 30px for title
            self.rect.width - 2 * self.padding,
            self.chart_height
        )
        
        bottom_chart_rect = pygame.Rect(
            self.rect.left + self.padding,
            top_chart_rect.bottom + self.padding,
            self.rect.width - 2 * self.padding,
            self.chart_height
        )
        
        # Draw fitness chart (top)
        label_font = pygame.font.SysFont(
            self.theme.get('font_name', 'Arial'),
            self.theme.get('small_font_size', 12)
        )
        
        fitness_label = label_font.render("Fitness", True, 
                                        self.theme.get('text_color', (20, 20, 30)))
        fitness_rect = fitness_label.get_rect(topleft=(top_chart_rect.left, top_chart_rect.top - 15))
        surface.blit(fitness_label, fitness_rect)
        
        # Draw best fitness data
        if self.best_fitness_data:
            draw_line_chart(
                surface,
                top_chart_rect,
                self.best_fitness_data,
                self.theme.get('best_fitness_color', (0, 120, 0)),
                0, 100,
                self.line_width,
                self.theme
            )
        
        # Draw average fitness data
        if self.avg_fitness_data:
            draw_line_chart(
                surface,
                top_chart_rect,
                self.avg_fitness_data,
                self.theme.get('avg_fitness_color', (0, 80, 140)),
                0, 100,
                self.line_width,
                self.theme
            )
        
        # Draw fitness legend
        legend_y = top_chart_rect.top + 10
        
        # Best fitness
        pygame.draw.line(
            surface,
            self.theme.get('best_fitness_color', (0, 120, 0)),
            (self.rect.right - 100, legend_y),
            (self.rect.right - 80, legend_y),
            self.line_width
        )
        best_legend = label_font.render("Best Fitness", True,
                                       self.theme.get('text_color', (20, 20, 30)))
        surface.blit(best_legend, (self.rect.right - 75, legend_y - 5))
        
        # Average fitness
        legend_y += 15
        pygame.draw.line(
            surface,
            self.theme.get('avg_fitness_color', (0, 80, 140)),
            (self.rect.right - 100, legend_y),
            (self.rect.right - 80, legend_y),
            self.line_width
        )
        avg_legend = label_font.render("Avg Fitness", True,
                                      self.theme.get('text_color', (20, 20, 30)))
        surface.blit(avg_legend, (self.rect.right - 75, legend_y - 5))
        
        # Draw diversity chart (bottom)
        diversity_label = label_font.render("Diversity %", True,
                                          self.theme.get('text_color', (20, 20, 30)))
        diversity_rect = diversity_label.get_rect(topleft=(bottom_chart_rect.left, bottom_chart_rect.top - 15))
        surface.blit(diversity_label, diversity_rect)
        
        # Draw diversity data
        if self.diversity_data:
            draw_line_chart(
                surface,
                bottom_chart_rect,
                self.diversity_data,
                self.theme.get('diversity_color', (160, 70, 120)),
                0, 100,
                self.line_width,
                self.theme
            )
        
        # Draw diversity legend
        legend_y = bottom_chart_rect.top + 10
        pygame.draw.line(
            surface,
            self.theme.get('diversity_color', (160, 70, 120)),
            (self.rect.right - 100, legend_y),
            (self.rect.right - 80, legend_y),
            self.line_width
        )
        div_legend = label_font.render("Diversity", True,
                                      self.theme.get('text_color', (20, 20, 30)))
        surface.blit(div_legend, (self.rect.right - 75, legend_y - 5))
        
        # Draw generation count at the bottom
        if self.generation_numbers:
            gen_text = f"Generation: {self.generation_numbers[-1]}"
            gen_label = label_font.render(gen_text, True,
                                        self.theme.get('text_color', (20, 20, 30)))
            gen_rect = gen_label.get_rect(bottomleft=(self.rect.left + self.padding, self.rect.bottom - 5))
            surface.blit(gen_label, gen_rect)
        
        # Calculate improvement if we have enough data
        if len(self.best_fitness_data) >= 2:
            initial = self.best_fitness_data[0]
            current = self.best_fitness_data[-1]
            improvement = current - initial
            
            # Display improvement
            if improvement >= 0:
                improvement_text = f"+{improvement:.2f} fitness"
                improvement_color = self.theme.get('success_color', (0, 150, 0))
            else:
                improvement_text = f"{improvement:.2f} fitness"
                improvement_color = self.theme.get('error_color', (200, 0, 0))
            
            improvement_label = label_font.render(improvement_text, True, improvement_color)
            improvement_rect = improvement_label.get_rect(bottomright=(self.rect.right - self.padding, self.rect.bottom - 5))
            surface.blit(improvement_label, improvement_rect)
        
        # Add annotations for important events (plateaus, convergence, etc.)
        if len(self.best_fitness_data) >= 10:
            self._draw_annotations(surface, top_chart_rect, bottom_chart_rect)
    
    def _draw_annotations(self, surface, top_chart_rect, bottom_chart_rect):
        """
        Draw annotations for important evolutionary events.
        
        Args:
            surface: The pygame surface to render to
            top_chart_rect: Rectangle for the top chart
            bottom_chart_rect: Rectangle for the bottom chart
        """
        label_font = pygame.font.SysFont(
            self.theme.get('font_name', 'Arial'),
            self.theme.get('small_font_size', 12)
        )
        
        # Detect plateaus (periods of no improvement)
        plateaus = self._detect_plateaus(5)  # 5+ generations with no improvement
        
        # Mark plateaus on the chart
        for start, end in plateaus:
            if start >= len(self.generation_numbers) or end >= len(self.generation_numbers):
                continue
                
            # Calculate positions
            chart_width = top_chart_rect.width
            start_x = top_chart_rect.left + (start / (len(self.generation_numbers) - 1)) * chart_width
            end_x = top_chart_rect.left + (end / (len(self.generation_numbers) - 1)) * chart_width
            
            # Draw plateau indicators on both charts
            for chart_rect in [top_chart_rect, bottom_chart_rect]:
                # Draw semi-transparent rectangle
                plateau_rect = pygame.Rect(
                    start_x, chart_rect.top,
                    end_x - start_x, chart_rect.height
                )
                
                # Create a semi-transparent surface
                plateau_surface = pygame.Surface((plateau_rect.width, plateau_rect.height), pygame.SRCALPHA)
                plateau_surface.fill((255, 0, 0, 30))  # Red with 30% alpha
                surface.blit(plateau_surface, plateau_rect)
                
                # Draw outline
                pygame.draw.rect(
                    surface,
                    (255, 0, 0, 128),
                    plateau_rect,
                    1
                )
            
            # Add label for the longest plateau
            longest_plateau = max(plateaus, key=lambda p: p[1] - p[0])
            if start == longest_plateau[0] and end == longest_plateau[1]:
                plateau_label = label_font.render("Plateau", True, (200, 0, 0))
                label_rect = plateau_label.get_rect(midtop=(
                    (start_x + end_x) / 2,
                    top_chart_rect.top + 5
                ))
                surface.blit(plateau_label, label_rect)
        
        # Detect convergence (diversity below threshold)
        low_diversity_threshold = 20  # 20% diversity
        low_diversity_gens = [
            i for i, div in enumerate(self.diversity_data)
            if div < low_diversity_threshold
        ]
        
        if low_diversity_gens:
            first_low_div = min(low_diversity_gens)
            if first_low_div < len(self.generation_numbers):
                # Mark the convergence point
                x_pos = bottom_chart_rect.left + (first_low_div / (len(self.generation_numbers) - 1)) * bottom_chart_rect.width
                y_pos = bottom_chart_rect.centery
                
                # Draw marker
                pygame.draw.line(
                    surface,
                    self.theme.get('warning_color', (200, 150, 0)),
                    (x_pos, bottom_chart_rect.top),
                    (x_pos, bottom_chart_rect.bottom),
                    1
                )
                
                # Add label
                converge_label = label_font.render("Low Diversity", True,
                                                 self.theme.get('warning_color', (200, 150, 0)))
                label_rect = converge_label.get_rect(midtop=(
                    x_pos,
                    bottom_chart_rect.top + 20
                ))
                surface.blit(converge_label, label_rect)
    
    def _detect_plateaus(self, min_length: int = 5) -> List[Tuple[int, int]]:
        """
        Detect plateaus in the fitness progression.
        
        Args:
            min_length: Minimum number of generations to consider a plateau
            
        Returns:
            List[Tuple[int, int]]: List of plateau intervals (start_idx, end_idx)
        """
        plateaus = []
        
        if len(self.best_fitness_data) < min_length:
            return plateaus
        
        # Find periods with no improvement
        plateau_start = None
        prev_fitness = self.best_fitness_data[0]
        
        for i in range(1, len(self.best_fitness_data)):
            curr_fitness = self.best_fitness_data[i]
            
            # Check if we're in a plateau (no improvement)
            if curr_fitness <= prev_fitness:
                # Start a new plateau if we're not in one
                if plateau_start is None:
                    plateau_start = i - 1
            else:
                # End current plateau if we were in one
                if plateau_start is not None:
                    plateau_length = i - plateau_start
                    if plateau_length >= min_length:
                        plateaus.append((plateau_start, i - 1))
                    plateau_start = None
            
            prev_fitness = curr_fitness
        
        # Check if we ended while still in a plateau
        if plateau_start is not None:
            plateau_length = len(self.best_fitness_data) - plateau_start
            if plateau_length >= min_length:
                plateaus.append((plateau_start, len(self.best_fitness_data) - 1))
        
        return plateaus