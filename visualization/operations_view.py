"""
Genetic operations visualization for the genetic algorithm.

This module visualizes the selection, crossover, and mutation operations
that occur during the genetic algorithm's evolution process.
"""

import pygame
from typing import Dict, Any, List, Tuple, Optional
import math
import random

from .themes import get_fitness_color


class OperationsView:
    """
    Visualizes the genetic operations of selection, crossover, and mutation.
    
    This component shows how individuals are selected, how crossover combines
    their genetic material, and how mutation introduces variation.
    """
    
    def __init__(self, rect: pygame.Rect, min_value: int, max_value: int,
                theme: Dict[str, Any] = None):
        """
        Initialize the operations visualization.
        
        Args:
            rect: The component's rectangle on the screen
            min_value: The minimum possible individual value
            max_value: The maximum possible individual value
            theme: Dictionary containing theme parameters
        """
        self.rect = rect
        self.min_value = min_value
        self.max_value = max_value
        self.theme = theme or {}
        
        # Visualization parameters
        self.padding = self.theme.get('padding', 10)
        self.arrow_width = self.theme.get('operations_arrow_width', 3)
        
        # Font for labels
        font_name = self.theme.get('font_name', 'Arial')
        font_size = self.theme.get('font_size', 16)
        self.font = pygame.font.SysFont(font_name, font_size)
        
        # Operation state tracking
        self.current_population = None
        self.selected_parents = []
        self.crossover_results = []
        self.mutated_individuals = []
        
        # Animation state
        self.animation_phase = 'none'  # 'none', 'selection', 'crossover', 'mutation'
        self.animation_progress = 0.0
        
        # Visualization layouts
        self._setup_layouts()
    
    def _setup_layouts(self):
        """Set up the layout for different operation visualizations."""
        self.layouts = {
            'selection': pygame.Rect(
                self.rect.left + self.padding,
                self.rect.top + 30,  # Space for title
                self.rect.width // 3 - self.padding * 2,
                self.rect.height - 40  # Space for title and bottom margin
            ),
            'crossover': pygame.Rect(
                self.rect.left + self.rect.width // 3 + self.padding,
                self.rect.top + 30,
                self.rect.width // 3 - self.padding * 2,
                self.rect.height - 40
            ),
            'mutation': pygame.Rect(
                self.rect.left + 2 * self.rect.width // 3 + self.padding,
                self.rect.top + 30,
                self.rect.width // 3 - self.padding * 2,
                self.rect.height - 40
            )
        }
    
    def prepare_new_generation(self, population) -> None:
        """
        Prepare for visualizing a new generation.
        
        Args:
            population: The current Population object
        """
        self.current_population = population
        
        # Reset operation tracking
        self.selected_parents = []
        self.crossover_results = []
        self.mutated_individuals = []
        
        # Reset animation
        self.animation_phase = 'selection'
        self.animation_progress = 0.0
    
    def prepare_genetic_operations(self, population) -> None:
        """
        Prepare to visualize genetic operations before they occur.
        
        Args:
            population: The Population object before operations
        """
        if not self.current_population or self.current_population != population:
            self.current_population = population
        
        # Simulate selection (in a real implementation, we'd get the actual selected parents)
        if not self.selected_parents and population.individuals:
            num_parents = min(4, len(population.individuals))
            self.selected_parents = random.sample(population.individuals, num_parents)
            self.animation_phase = 'selection'
            self.animation_progress = 0.0
    
    def prepare_crossover(self) -> None:
        """Simulate crossover operations with selected parents."""
        if len(self.selected_parents) >= 2:
            # Clear previous results
            self.crossover_results = []
            
            # Create pairs of parents
            for i in range(0, len(self.selected_parents) - 1, 2):
                parent1 = self.selected_parents[i]
                parent2 = self.selected_parents[i + 1]
                
                # Simulate crossover
                child1, child2 = parent1.crossover(parent2)
                
                # Store parents and children
                self.crossover_results.append({
                    'parents': (parent1, parent2),
                    'children': (child1, child2)
                })
            
            # Start crossover animation
            self.animation_phase = 'crossover'
            self.animation_progress = 0.0
    
    def prepare_mutation(self) -> None:
        """Simulate mutation operations after crossover."""
        self.mutated_individuals = []
        
        # Collect all children from crossover
        children = []
        for result in self.crossover_results:
            children.extend(result['children'])
        
        # Store pre-mutation values
        for child in children:
            pre_value = child.value
            
            # Apply mutation (for visualization only)
            mutation_range = max(1, (self.max_value - self.min_value) // 10)
            if random.random() < 0.3:  # 30% chance of mutation
                change = random.randint(-mutation_range, mutation_range)
                while change == 0:
                    change = random.randint(-mutation_range, mutation_range)
                
                # Record the mutation but don't actually apply it
                # (it would be applied by the actual algorithm)
                post_value = max(self.min_value, min(pre_value + change, self.max_value))
                
                self.mutated_individuals.append({
                    'individual': child,
                    'pre_value': pre_value,
                    'post_value': post_value
                })
        
        # Start mutation animation
        self.animation_phase = 'mutation'
        self.animation_progress = 0.0
    
    def finish_genetic_operations(self, population) -> None:
        """
        Finish visualization of genetic operations.
        
        Args:
            population: The Population object after operations
        """
        self.current_population = population
        self.animation_phase = 'none'
    
    def update_animation(self) -> None:
        """Update animation progress and transition between phases."""
        if self.animation_phase == 'none':
            return
        
        # Update animation progress
        self.animation_progress += self.theme.get('animation_speed', 0.3)
        
        # Check for phase transition
        if self.animation_progress >= 1.0:
            self.animation_progress = 0.0
            
            # Transition to next phase
            if self.animation_phase == 'selection':
                self.prepare_crossover()
            elif self.animation_phase == 'crossover':
                self.prepare_mutation()
            elif self.animation_phase == 'mutation':
                self.animation_phase = 'none'
    
    def render(self, surface, population) -> None:
        """
        Render the operations visualization to a surface.
        
        Args:
            surface: The pygame surface to render to
            population: The current Population object
        """
        # Update population reference if needed
        if population and self.current_population != population:
            self.current_population = population
        
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
        title_text = title_font.render("Genetic Operations", True,
                                      self.theme.get('text_color', (20, 20, 30)))
        title_rect = title_text.get_rect(midtop=(self.rect.centerx, self.rect.top + 5))
        surface.blit(title_text, title_rect)
        
        # Draw operation sections
        self._draw_selection(surface)
        self._draw_crossover(surface)
        self._draw_mutation(surface)
        
        # Update animation state
        self.update_animation()
    
    def _draw_selection(self, surface) -> None:
        """
        Draw the selection operation visualization.
        
        Args:
            surface: The pygame surface to render to
        """
        section_rect = self.layouts['selection']
        
        # Section title
        section_font = pygame.font.SysFont(
            self.theme.get('font_name', 'Arial'),
            self.theme.get('font_size', 16)
        )
        section_text = section_font.render("Selection", True,
                                         self.theme.get('text_color', (20, 20, 30)))
        section_rect_text = section_text.get_rect(midtop=(section_rect.centerx, section_rect.top))
        surface.blit(section_text, section_rect_text)
        
        # Draw selected parents
        if self.selected_parents:
            y_step = section_rect.height // (len(self.selected_parents) + 1)
            
            for i, parent in enumerate(self.selected_parents):
                y_pos = section_rect.top + (i + 1) * y_step
                
                # Determine if this parent should be highlighted based on animation
                highlight = self.animation_phase == 'selection' and \
                          self.animation_progress > (i / len(self.selected_parents))
                
                self._draw_individual(
                    surface,
                    section_rect.centerx,
                    y_pos,
                    parent.value,
                    parent.fitness,
                    highlight
                )
    
    def _draw_crossover(self, surface) -> None:
        """
        Draw the crossover operation visualization.
        
        Args:
            surface: The pygame surface to render to
        """
        section_rect = self.layouts['crossover']
        
        # Section title
        section_font = pygame.font.SysFont(
            self.theme.get('font_name', 'Arial'),
            self.theme.get('font_size', 16)
        )
        section_text = section_font.render("Crossover", True,
                                         self.theme.get('text_color', (20, 20, 30)))
        section_rect_text = section_text.get_rect(midtop=(section_rect.centerx, section_rect.top))
        surface.blit(section_text, section_rect_text)
        
        # Draw crossover operations
        if self.crossover_results:
            y_step = section_rect.height // (len(self.crossover_results) + 1)
            
            for i, result in enumerate(self.crossover_results):
                y_pos = section_rect.top + (i + 1) * y_step
                
                # Parent positions
                parent1, parent2 = result['parents']
                p1_x = section_rect.left + section_rect.width * 0.25
                p2_x = section_rect.left + section_rect.width * 0.75
                
                # Child positions
                child1, child2 = result['children']
                c1_x = section_rect.left + section_rect.width * 0.25
                c2_x = section_rect.left + section_rect.width * 0.75
                
                # Determine animation state
                if self.animation_phase == 'crossover':
                    # Animate the crossover process
                    # Draw parents at the top
                    self._draw_individual(surface, p1_x, y_pos - 20, parent1.value, parent1.fitness)
                    self._draw_individual(surface, p2_x, y_pos - 20, parent2.value, parent2.fitness)
                    
                    # Draw children below with animation
                    if self.animation_progress > 0.5:
                        # Fade in children
                        alpha = min(255, int((self.animation_progress - 0.5) * 2 * 255))
                        self._draw_individual(surface, c1_x, y_pos + 20, child1.value, child1.fitness, opacity=alpha)
                        self._draw_individual(surface, c2_x, y_pos + 20, child2.value, child2.fitness, opacity=alpha)
                    
                    # Draw connecting lines with animation
                    crossover_point = self.animation_progress
                    
                    # Only draw connections if animation has started
                    if crossover_point > 0:
                        # Connection lines
                        pygame.draw.line(
                            surface,
                            self.theme.get('highlight_color', (70, 130, 180)),
                            (p1_x, y_pos - 20),
                            (c1_x, y_pos + 20),
                            self.arrow_width
                        )
                        pygame.draw.line(
                            surface,
                            self.theme.get('highlight_color', (70, 130, 180)),
                            (p2_x, y_pos - 20),
                            (c2_x, y_pos + 20),
                            self.arrow_width
                        )
                else:
                    # Static display after animation
                    # Draw parents and children
                    self._draw_individual(surface, p1_x, y_pos - 20, parent1.value, parent1.fitness)
                    self._draw_individual(surface, p2_x, y_pos - 20, parent2.value, parent2.fitness)
                    self._draw_individual(surface, c1_x, y_pos + 20, child1.value, child1.fitness)
                    self._draw_individual(surface, c2_x, y_pos + 20, child2.value, child2.fitness)
                    
                    # Connection lines
                    pygame.draw.line(
                        surface,
                        self.theme.get('highlight_color', (70, 130, 180)),
                        (p1_x, y_pos - 20),
                        (c1_x, y_pos + 20),
                        self.arrow_width
                    )
                    pygame.draw.line(
                        surface,
                        self.theme.get('highlight_color', (70, 130, 180)),
                        (p2_x, y_pos - 20),
                        (c2_x, y_pos + 20),
                        self.arrow_width
                    )
    
    def _draw_mutation(self, surface) -> None:
        """
        Draw the mutation operation visualization.
        
        Args:
            surface: The pygame surface to render to
        """
        section_rect = self.layouts['mutation']
        
        # Section title
        section_font = pygame.font.SysFont(
            self.theme.get('font_name', 'Arial'),
            self.theme.get('font_size', 16)
        )
        section_text = section_font.render("Mutation", True,
                                         self.theme.get('text_color', (20, 20, 30)))
        section_rect_text = section_text.get_rect(midtop=(section_rect.centerx, section_rect.top))
        surface.blit(section_text, section_rect_text)
        
        # Draw mutation operations
        if self.mutated_individuals:
            y_step = section_rect.height // (len(self.mutated_individuals) + 1)
            
            for i, mutation in enumerate(self.mutated_individuals):
                y_pos = section_rect.top + (i + 1) * y_step
                
                # Individual
                individual = mutation['individual']
                pre_value = mutation['pre_value']
                post_value = mutation['post_value']
                
                # Positions
                pre_x = section_rect.left + section_rect.width * 0.3
                post_x = section_rect.left + section_rect.width * 0.7
                
                # Determine animation state
                if self.animation_phase == 'mutation':
                    # Animate the mutation process
                    # Draw pre-mutation state
                    self._draw_individual(surface, pre_x, y_pos, pre_value, individual.fitness)
                    
                    # Draw post-mutation state with animation
                    if self.animation_progress > 0.5:
                        # Transition from pre to post value
                        transition = min(1.0, (self.animation_progress - 0.5) * 2)
                        current_value = int(pre_value + (post_value - pre_value) * transition)
                        
                        # Fade in post-mutation individual
                        alpha = min(255, int((self.animation_progress - 0.5) * 2 * 255))
                        self._draw_individual(surface, post_x, y_pos, current_value, 
                                            individual.fitness, opacity=alpha, with_spark=True)
                        
                        # Draw arrow
                        pygame.draw.line(
                            surface,
                            self.theme.get('highlight_color', (70, 130, 180)),
                            (pre_x + 15, y_pos),
                            (post_x - 15, y_pos),
                            self.arrow_width
                        )
                        
                        # Draw arrowhead
                        arrowhead_points = [
                            (post_x - 15, y_pos),
                            (post_x - 25, y_pos - 5),
                            (post_x - 25, y_pos + 5)
                        ]
                        pygame.draw.polygon(
                            surface,
                            self.theme.get('highlight_color', (70, 130, 180)),
                            arrowhead_points
                        )
                else:
                    # Static display after animation
                    # Draw pre and post mutation states
                    self._draw_individual(surface, pre_x, y_pos, pre_value, individual.fitness)
                    self._draw_individual(surface, post_x, y_pos, post_value, 
                                        individual.fitness, with_spark=True)
                    
                    # Draw arrow
                    pygame.draw.line(
                        surface,
                        self.theme.get('highlight_color', (70, 130, 180)),
                        (pre_x + 15, y_pos),
                        (post_x - 15, y_pos),
                        self.arrow_width
                    )
                    
                    # Draw arrowhead
                    arrowhead_points = [
                        (post_x - 15, y_pos),
                        (post_x - 25, y_pos - 5),
                        (post_x - 25, y_pos + 5)
                    ]
                    pygame.draw.polygon(
                        surface,
                        self.theme.get('highlight_color', (70, 130, 180)),
                        arrowhead_points
                    )
                    
                    # Draw value change
                    value_diff = post_value - pre_value
                    if value_diff != 0:
                        diff_text = f"{'+' if value_diff > 0 else ''}{value_diff}"
                        diff_color = self.theme.get('success_color', (0, 150, 0)) if value_diff > 0 else \
                                  self.theme.get('error_color', (200, 0, 0))
                        
                        diff_font = pygame.font.SysFont(
                            self.theme.get('font_name', 'Arial'),
                            self.theme.get('small_font_size', 12)
                        )
                        diff_surface = diff_font.render(diff_text, True, diff_color)
                        diff_rect = diff_surface.get_rect(midtop=(
                            (pre_x + post_x) / 2,
                            y_pos - 20
                        ))
                        surface.blit(diff_surface, diff_rect)
    
    def _draw_individual(self, surface, x: int, y: int, value: int, fitness: float,
                       highlight: bool = False, opacity: int = 255, with_spark: bool = False) -> None:
        """
        Draw an individual as a circle with value text.
        
        Args:
            surface: The pygame surface to render to
            x: X-coordinate
            y: Y-coordinate
            value: The individual's value
            fitness: The individual's fitness
            highlight: Whether to highlight the individual
            opacity: Opacity (0-255)
            with_spark: Whether to draw a "mutation spark" effect
        """
        # Determine radius based on fitness
        base_radius = 15
        fitness_factor = (fitness / 100) * 0.5 + 0.5  # Scale factor 0.5-1.0
        radius = int(base_radius * fitness_factor)
        
        # Get color from fitness
        color = get_fitness_color(self.theme, fitness)
        
        # Apply opacity
        color_with_alpha = (*color, opacity)
        
        # Create a surface with per-pixel alpha
        individual_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        
        # Draw circle
        pygame.draw.circle(individual_surface, color_with_alpha, (radius, radius), radius)
        
        # Draw highlight if needed
        if highlight:
            highlight_color = self.theme.get('highlight_color', (70, 130, 180))
            pygame.draw.circle(individual_surface, highlight_color, (radius, radius), radius, 2)
        
        # Draw value text
        font = pygame.font.SysFont(
            self.theme.get('font_name', 'Arial'),
            self.theme.get('small_font_size', 12)
        )
        
        text_surface = font.render(str(value), True, (255, 255, 255, opacity))
        text_rect = text_surface.get_rect(center=(radius, radius))
        individual_surface.blit(text_surface, text_rect)
        
        # Blit to main surface
        surface.blit(individual_surface, (x - radius, y - radius))
        
        # Draw mutation spark if requested
        if with_spark:
            spark_points = []
            
            # Generate random spark points
            num_sparks = 5
            for _ in range(num_sparks):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(radius * 0.8, radius * 1.5)
                end_x = x + math.cos(angle) * distance
                end_y = y + math.sin(angle) * distance
                spark_points.append((x, y, end_x, end_y))
            
            # Draw sparks
            for start_x, start_y, end_x, end_y in spark_points:
                pygame.draw.line(
                    surface,
                    (255, 255, 0, opacity),  # Yellow spark
                    (start_x, start_y),
                    (end_x, end_y),
                    2
                )