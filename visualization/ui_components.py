"""
UI Components for the genetic algorithm visualization.

This module provides reusable UI components like buttons and sliders
for the visualization interface.
"""

import pygame
from typing import Callable, Optional, Tuple, Dict, Any
import math


class Button:
    """A clickable button UI component."""
    
    def __init__(self, rect: pygame.Rect, text: str, 
                callback: Callable = None, theme: Dict[str, Any] = None,
                disabled: bool = False):
        """
        Initialize a button.
        
        Args:
            rect: The button's rectangle
            text: The button's label text
            callback: Function to call when the button is clicked
            theme: Dictionary containing theme parameters
            disabled: Whether the button is initially disabled
        """
        self.rect = rect
        self.text = text
        self.callback = callback
        self.theme = theme or {}
        self.disabled = disabled
        self.hovered = False
        
        # Set up font
        font_name = self.theme.get('font_name', 'Arial')
        font_size = self.theme.get('font_size', 16)
        self.font = pygame.font.SysFont(font_name, font_size)
    
    def handle_event(self, event, mouse_pos, mouse_buttons):
        """
        Handle pygame events.
        
        Args:
            event: The pygame event
            mouse_pos: Current mouse position
            mouse_buttons: Current mouse button states
        """
        if self.disabled:
            return
        
        # Check if mouse is over button
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Check for click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            if self.callback:
                self.callback()
    
    def render(self, surface):
        """
        Render the button to a surface.
        
        Args:
            surface: The pygame surface to render to
        """
        # Determine button color
        if self.disabled:
            color = self.theme.get('button_disabled_color', (150, 150, 150))
        elif self.hovered:
            color = self.theme.get('button_hover_color', (90, 150, 200))
        else:
            color = self.theme.get('button_color', (70, 130, 180))
        
        # Button background
        border_radius = self.theme.get('border_radius', 5)
        pygame.draw.rect(surface, color, self.rect, border_radius=border_radius)
        
        # Button text
        text_color = self.theme.get('button_text_color', (255, 255, 255))
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class ToggleButton(Button):
    """A button that toggles between two states."""
    
    def __init__(self, rect: pygame.Rect, text_on: str, text_off: str,
                callback: Callable = None, theme: Dict[str, Any] = None,
                initial_state: bool = False):
        """
        Initialize a toggle button.
        
        Args:
            rect: The button's rectangle
            text_on: The button's label text when on
            text_off: The button's label text when off
            callback: Function to call when the button is toggled
            theme: Dictionary containing theme parameters
            initial_state: Initial toggle state (True=on, False=off)
        """
        super().__init__(rect, text_on if initial_state else text_off, callback, theme)
        self.text_on = text_on
        self.text_off = text_off
        self.state = initial_state
    
    def toggle(self):
        """Toggle the button state."""
        self.state = not self.state
        self.text = self.text_on if self.state else self.text_off
        
        if self.callback:
            self.callback()
    
    def handle_event(self, event, mouse_pos, mouse_buttons):
        """
        Handle pygame events.
        
        Args:
            event: The pygame event
            mouse_pos: Current mouse position
            mouse_buttons: Current mouse button states
        """
        if self.disabled:
            return
        
        # Check if mouse is over button
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Check for click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            self.toggle()


class Slider:
    """A draggable slider UI component."""
    
    def __init__(self, rect: pygame.Rect, min_value: float, max_value: float, 
                initial_value: float, callback: Callable = None, 
                theme: Dict[str, Any] = None, step: float = None):
        """
        Initialize a slider.
        
        Args:
            rect: The slider's rectangle
            min_value: Minimum value
            max_value: Maximum value
            initial_value: Initial value
            callback: Function to call when the value changes
            theme: Dictionary containing theme parameters
            step: Step size (None for continuous)
        """
        self.rect = rect
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.callback = callback
        self.theme = theme or {}
        self.step = step
        self.dragging = False
        
        # Calculate handle position
        self._update_handle_pos()
    
    def _update_handle_pos(self):
        """Update the handle position based on the current value."""
        normalized = (self.value - self.min_value) / (self.max_value - self.min_value)
        self.handle_pos = self.rect.left + int(normalized * self.rect.width)
    
    def _update_value_from_pos(self, pos_x):
        """Update the value based on the handle position."""
        normalized = max(0, min(1, (pos_x - self.rect.left) / self.rect.width))
        value = self.min_value + normalized * (self.max_value - self.min_value)
        
        # Apply step if specified
        if self.step:
            value = round(value / self.step) * self.step
        
        # Only update if value changed
        if value != self.value:
            self.value = value
            if self.callback:
                self.callback(self.value)
    
    def handle_event(self, event, mouse_pos, mouse_buttons):
        """
        Handle pygame events.
        
        Args:
            event: The pygame event
            mouse_pos: Current mouse position
            mouse_buttons: Current mouse button states
        """
        # Check for mouse down on handle
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_rect = pygame.Rect(self.handle_pos - 10, self.rect.top, 20, self.rect.height)
            if handle_rect.collidepoint(mouse_pos):
                self.dragging = True
        
        # Check for mouse up (stop dragging)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        
        # Check for mouse movement while dragging
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_value_from_pos(mouse_pos[0])
            self._update_handle_pos()
    
    def render(self, surface):
        """
        Render the slider to a surface.
        
        Args:
            surface: The pygame surface to render to
        """
        # Update handle position
        self._update_handle_pos()
        
        # Track
        track_rect = pygame.Rect(self.rect.left, self.rect.centery - 2, 
                               self.rect.width, 4)
        track_color = self.theme.get('slider_track_color', (200, 200, 210))
        pygame.draw.rect(surface, track_color, track_rect, border_radius=2)
        
        # Handle
        handle_radius = 8
        handle_color = self.theme.get('slider_handle_color', (70, 130, 180))
        pygame.draw.circle(surface, handle_color, 
                         (self.handle_pos, self.rect.centery), handle_radius)
        
        # Value text
        font_name = self.theme.get('font_name', 'Arial')
        font_size = self.theme.get('small_font_size', 12)
        font = pygame.font.SysFont(font_name, font_size)
        
        value_text = str(int(self.value) if self.value == int(self.value) else f"{self.value:.1f}")
        text_surface = font.render(value_text, True, self.theme.get('text_color', (20, 20, 30)))
        text_rect = text_surface.get_rect(midtop=(self.handle_pos, self.rect.bottom - 15))
        surface.blit(text_surface, text_rect)


class TextBox:
    """A non-interactive text display component."""
    
    def __init__(self, rect: pygame.Rect, text: str, theme: Dict[str, Any] = None,
                 align: str = 'center', background: bool = False):
        """
        Initialize a text box.
        
        Args:
            rect: The text box's rectangle
            text: The text to display
            theme: Dictionary containing theme parameters
            align: Text alignment ('left', 'center', 'right')
            background: Whether to draw a background
        """
        self.rect = rect
        self.text = text
        self.theme = theme or {}
        self.align = align
        self.background = background
        
        # Set up font
        font_name = self.theme.get('font_name', 'Arial')
        font_size = self.theme.get('font_size', 16)
        self.font = pygame.font.SysFont(font_name, font_size)
    
    def render(self, surface):
        """
        Render the text box to a surface.
        
        Args:
            surface: The pygame surface to render to
        """
        # Background
        if self.background:
            bg_color = self.theme.get('panel_color', (220, 220, 230))
            border_radius = self.theme.get('border_radius', 5)
            pygame.draw.rect(surface, bg_color, self.rect, border_radius=border_radius)
        
        # Text
        text_color = self.theme.get('text_color', (20, 20, 30))
        text_surface = self.font.render(self.text, True, text_color)
        
        # Position based on alignment
        if self.align == 'left':
            text_pos = (self.rect.left + self.theme.get('padding', 5), self.rect.centery)
            text_rect = text_surface.get_rect(midleft=text_pos)
        elif self.align == 'right':
            text_pos = (self.rect.right - self.theme.get('padding', 5), self.rect.centery)
            text_rect = text_surface.get_rect(midright=text_pos)
        else:  # center
            text_rect = text_surface.get_rect(center=self.rect.center)
        
        surface.blit(text_surface, text_rect)


def draw_rounded_rect(surface, rect, color, radius=10, border_width=0, border_color=None):
    """
    Draw a rounded rectangle.
    
    Args:
        surface: Surface to draw on
        rect: Rectangle
        color: Fill color
        radius: Corner radius
        border_width: Border width (0 for filled)
        border_color: Border color (same as fill if None)
    """
    if border_width > 0 and border_color:
        # Draw outer rectangle
        pygame.draw.rect(surface, border_color, rect, border_radius=radius)
        # Draw inner rectangle
        inner_rect = rect.inflate(-border_width*2, -border_width*2)
        pygame.draw.rect(surface, color, inner_rect, border_radius=radius)
    else:
        # Draw filled rectangle
        pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_line_chart(surface, rect, data, color, min_value=0, max_value=100, 
                  line_width=2, theme=None):
    """
    Draw a line chart.
    
    Args:
        surface: Surface to draw on
        rect: Rectangle for the chart
        data: List of values to plot
        color: Line color
        min_value: Minimum value (y-axis)
        max_value: Maximum value (y-axis)
        line_width: Width of the line
        theme: Theme dictionary
    """
    if not data:
        return
    
    # Background
    theme = theme or {}
    bg_color = theme.get('panel_color', (220, 220, 230))
    border_color = theme.get('border_color', (180, 180, 190))
    
    # Draw background
    pygame.draw.rect(surface, bg_color, rect)
    pygame.draw.rect(surface, border_color, rect, 1)
    
    # Calculate points
    points = []
    x_step = rect.width / (len(data) - 1) if len(data) > 1 else rect.width
    
    for i, value in enumerate(data):
        # Normalize value to chart height
        if max_value > min_value:
            normalized = (value - min_value) / (max_value - min_value)
        else:
            normalized = 0.5
        
        normalized = max(0, min(1, normalized))  # Clamp to 0-1
        
        x = rect.left + i * x_step
        y = rect.bottom - normalized * rect.height
        points.append((x, y))
    
    # Draw line
    if len(points) >= 2:
        pygame.draw.lines(surface, color, False, points, line_width)
    
    # Draw points
    point_radius = max(2, line_width)
    for point in points:
        pygame.draw.circle(surface, color, point, point_radius)


def draw_bar_chart(surface, rect, data, color, min_value=0, max_value=100, theme=None):
    """
    Draw a bar chart.
    
    Args:
        surface: Surface to draw on
        rect: Rectangle for the chart
        data: List of values to plot
        color: Bar color
        min_value: Minimum value (y-axis)
        max_value: Maximum value (y-axis)
        theme: Theme dictionary
    """
    if not data:
        return
    
    # Background
    theme = theme or {}
    bg_color = theme.get('panel_color', (220, 220, 230))
    border_color = theme.get('border_color', (180, 180, 190))
    
    # Draw background
    pygame.draw.rect(surface, bg_color, rect)
    pygame.draw.rect(surface, border_color, rect, 1)
    
    # Calculate bar width
    bar_width = rect.width / len(data)
    bar_spacing = max(1, int(bar_width * 0.1))
    bar_width -= bar_spacing
    
    # Draw bars
    for i, value in enumerate(data):
        # Normalize value to chart height
        if max_value > min_value:
            normalized = (value - min_value) / (max_value - min_value)
        else:
            normalized = 0.5
        
        normalized = max(0, min(1, normalized))  # Clamp to 0-1
        
        bar_height = int(normalized * rect.height)
        bar_rect = pygame.Rect(
            rect.left + i * (bar_width + bar_spacing) + bar_spacing // 2,
            rect.bottom - bar_height,
            bar_width,
            bar_height
        )
        
        pygame.draw.rect(surface, color, bar_rect)