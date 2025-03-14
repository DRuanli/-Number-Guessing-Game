"""
Utilities module for the Genetic Algorithm Number Guessing Game.

This module provides utility components for configuration management
and statistics tracking for the genetic algorithm.
"""

from .config import Config, DEFAULT_CONFIG
from .statistics import StatisticsTracker

__all__ = ['Config', 'DEFAULT_CONFIG', 'StatisticsTracker']