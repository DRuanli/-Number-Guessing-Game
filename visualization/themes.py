"""
Theme definitions for the genetic algorithm visualization.

This module provides color schemes, fonts, and styling parameters
for the visualization components.
"""

import pygame
from typing import Dict, Any


# Default theme
DEFAULT_THEME = {
    # Colors
    'background_color': (240, 240, 245),
    'panel_color': (220, 220, 230),
    'border_color': (180, 180, 190),
    'text_color': (20, 20, 30),
    'highlight_color': (70, 130, 180),
    'success_color': (0, 150, 0),
    'error_color': (200, 0, 0),
    'warning_color': (200, 150, 0),
    
    # Fitness gradient colors (from low to high)
    'fitness_colors': [
        (200, 0, 0),    # Red (lowest fitness)
        (220, 100, 0),  # Orange
        (220, 200, 0),  # Yellow
        (100, 200, 0),  # Light green
        (0, 150, 0)     # Dark green (highest fitness)
    ],
    
    # Secret number marker color
    'secret_color': (70, 20, 170),
    
    # Chart colors
    'best_fitness_color': (0, 120, 0),
    'avg_fitness_color': (0, 80, 140),
    'diversity_color': (160, 70, 120),
    
    # Button colors
    'button_color': (70, 130, 180),
    'button_hover_color': (90, 150, 200),
    'button_text_color': (255, 255, 255),
    'button_disabled_color': (150, 150, 150),
    
    # Slider colors
    'slider_track_color': (200, 200, 210),
    'slider_handle_color': (70, 130, 180),
    
    # Fonts
    'font_name': 'Arial',
    'font_size': 16,
    'title_font_size': 20,
    'small_font_size': 12,
    
    # Animation parameters
    'animation_speed': 0.3,
    'transition_frames': 20,
    
    # UI parameters
    'padding': 10,
    'border_radius': 5,
    'border_width': 1,
    
    # Component-specific styling
    'population_individual_radius': 5,
    'fitness_landscape_line_width': 2,
    'evolution_chart_line_width': 2,
    'operations_arrow_width': 3
}


# Dark theme
DARK_THEME = {
    # Colors
    'background_color': (30, 30, 35),
    'panel_color': (45, 45, 50),
    'border_color': (70, 70, 75),
    'text_color': (220, 220, 225),
    'highlight_color': (100, 160, 200),
    'success_color': (0, 200, 0),
    'error_color': (220, 60, 60),
    'warning_color': (220, 180, 40),
    
    # Fitness gradient colors (from low to high)
    'fitness_colors': [
        (200, 50, 50),   # Red (lowest fitness)
        (220, 120, 50),  # Orange
        (220, 220, 50),  # Yellow
        (100, 220, 50),  # Light green
        (50, 200, 50)    # Dark green (highest fitness)
    ],
    
    # Secret number marker color
    'secret_color': (180, 100, 240),
    
    # Chart colors
    'best_fitness_color': (80, 220, 80),
    'avg_fitness_color': (80, 160, 220),
    'diversity_color': (220, 120, 200),
    
    # Button colors
    'button_color': (70, 120, 170),
    'button_hover_color': (90, 140, 190),
    'button_text_color': (240, 240, 240),
    'button_disabled_color': (100, 100, 110),
    
    # Slider colors
    'slider_track_color': (60, 60, 70),
    'slider_handle_color': (100, 160, 200),
    
    # Fonts - same as default
    'font_name': 'Arial',
    'font_size': 16,
    'title_font_size': 20,
    'small_font_size': 12,
    
    # Animation parameters
    'animation_speed': 0.3,
    'transition_frames': 20,
    
    # UI parameters
    'padding': 10,
    'border_radius': 5,
    'border_width': 1,
    
    # Component-specific styling
    'population_individual_radius': 5,
    'fitness_landscape_line_width': 2,
    'evolution_chart_line_width': 2,
    'operations_arrow_width': 3
}


# Colorblind-friendly theme
COLORBLIND_THEME = {
    # Colors - same as default
    'background_color': (240, 240, 245),
    'panel_color': (220, 220, 230),
    'border_color': (180, 180, 190),
    'text_color': (20, 20, 30),
    'highlight_color': (0, 120, 180),
    'success_color': (0, 140, 140),
    'error_color': (230, 90, 0),
    'warning_color': (200, 150, 0),
    
    # Colorblind-friendly gradient (blue to orange)
    'fitness_colors': [
        (230, 90, 0),    # Orange (lowest fitness)
        (220, 150, 80),  # Light orange
        (200, 200, 200), # Neutral gray
        (100, 170, 200), # Light blue
        (0, 120, 180)    # Blue (highest fitness)
    ],
    
    # Secret number marker color
    'secret_color': (140, 0, 140),
    
    # Chart colors - colorblind friendly
    'best_fitness_color': (0, 120, 180),
    'avg_fitness_color': (230, 90, 0),
    'diversity_color': (140, 0, 140),
    
    # Button colors
    'button_color': (0, 120, 180),
    'button_hover_color': (30, 150, 210),
    'button_text_color': (255, 255, 255),
    'button_disabled_color': (150, 150, 150),
    
    # Slider colors
    'slider_track_color': (200, 200, 210),
    'slider_handle_color': (0, 120, 180),
    
    # Fonts - same as default
    'font_name': 'Arial',
    'font_size': 16,
    'title_font_size': 20,
    'small_font_size': 12,
    
    # Animation parameters
    'animation_speed': 0.3,
    'transition_frames': 20,
    
    # UI parameters
    'padding': 10,
    'border_radius': 5,
    'border_width': 1,
    
    # Component-specific styling
    'population_individual_radius': 5,
    'fitness_landscape_line_width': 2,
    'evolution_chart_line_width': 2,
    'operations_arrow_width': 3
}


# Theme dictionary
THEMES = {
    'default': DEFAULT_THEME,
    'dark': DARK_THEME,
    'colorblind': COLORBLIND_THEME
}


def get_theme(theme_name: str = 'default') -> Dict[str, Any]:
    """
    Get a theme by name.
    
    Args:
        theme_name: The name of the theme to get
        
    Returns:
        Dict[str, Any]: The theme dictionary
    """
    return THEMES.get(theme_name, DEFAULT_THEME)


def interpolate_color(color1, color2, factor: float):
    """
    Interpolate between two colors.
    
    Args:
        color1: The first color (r, g, b)
        color2: The second color (r, g, b)
        factor: The interpolation factor (0-1)
        
    Returns:
        tuple: The interpolated color
    """
    r = int(color1[0] + (color2[0] - color1[0]) * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * factor)
    return (r, g, b)


def get_fitness_color(theme, fitness: float):
    """
    Get a color for a fitness value.
    
    Args:
        theme: The theme dictionary
        fitness: The fitness value (0-100)
        
    Returns:
        tuple: The color for the fitness value
    """
    fitness_colors = theme['fitness_colors']
    normalized_fitness = max(0, min(1, fitness / 100.0))
    
    # Map the fitness to the color range
    num_colors = len(fitness_colors)
    if num_colors == 1:
        return fitness_colors[0]
    
    # Calculate which segment the fitness falls into
    segment_size = 1.0 / (num_colors - 1)
    segment = int(normalized_fitness / segment_size)
    segment = min(segment, num_colors - 2)
    
    # Calculate interpolation factor within the segment
    factor = (normalized_fitness - segment * segment_size) / segment_size
    
    # Interpolate between the two colors
    return interpolate_color(fitness_colors[segment], fitness_colors[segment + 1], factor)