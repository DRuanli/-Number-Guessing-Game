# Genetic Algorithm Visualization

This module provides an interactive visualization of the genetic algorithm for the Number Guessing Game using Pygame.

## Features

- Real-time visualization of the genetic algorithm's operation
- Population visualization on a number line
- Fitness landscape representation
- Evolution charts showing fitness and diversity trends
- Genetic operations (selection, crossover, mutation) visualization
- Statistics dashboard with performance metrics
- Interactive controls for pausing, stepping, and adjusting speed
- Screenshot capability

## Requirements

- Python 3.6 or higher
- Pygame 2.0.0 or higher

Install Pygame with:

```bash
pip install pygame
```

## Usage

Run the visualization with:

```bash
python main_visual.py
```

### Command-line Options

All command-line arguments from the original `main.py` are supported, plus additional visualization options:

```bash
python main_visual.py --visual-mode all --window-width 1280 --window-height 720 --theme default
```

#### Visualization-specific options

| Option | Description | Default |
|--------|-------------|---------|
| `--visual-mode` | Visualization mode (`all`, `population`, `fitness`, `evolution`, `operations`) | `all` |
| `--window-width` | Width of the visualization window | `1280` |
| `--window-height` | Height of the visualization window | `720` |
| `--fps` | Frames per second for visualization | `60` |
| `--speed` | Speed multiplier for evolution | `1` |
| `--theme` | Visualization theme (`default`, `dark`, `colorblind`) | `default` |
| `--no-animation` | Disable animations | `False` |

## Visualization Components

### Population View

Displays the population of individuals as circles on a number line:
- Each circle represents an individual in the population
- Position on the line indicates the individual's value (guess)
- Color represents fitness (red = low, green = high)
- Size varies based on fitness
- The target (secret number) is marked with a triangle

### Fitness Landscape

Shows the fitness function as a curve and plots individuals on it:
- X-axis represents the possible values
- Y-axis represents fitness (0-100%)
- Individuals are positioned according to their value and fitness
- The target (secret number) is marked with a vertical line

### Evolution Chart

Displays the progression of key metrics over generations:
- Fitness chart (best fitness and average fitness)
- Diversity chart showing population diversity over time
- Annotations for important events (plateaus, convergence)

### Operations View

Visualizes the genetic operations in action:
- Selection of individuals for reproduction
- Crossover between parents to create offspring
- Mutation of individuals to introduce variation
- Animated transitions between operation stages

### Statistics Dashboard

Provides real-time statistics and performance metrics:
- Generation counter
- Best fitness with progress bar
- Best guess and average fitness
- Population diversity
- Elapsed time and speed (generations per second)
- Estimated time to solution

## Controls

The visualization provides several interactive controls:

### Keyboard Controls

- `Space`: Pause/Resume evolution
- `Right Arrow`: Step forward one generation (when paused)
- `S`: Take screenshot
- `Escape`: Quit

### UI Controls

- Play/Pause button: Toggles the evolution process
- Step button: Advances one generation when paused
- Reset button: Resets the evolution process
- Speed slider: Adjusts the evolution speed (1-10x)
- Screenshot button: Saves the current screen to a file

## Extending the Visualization

The visualization system is designed to be modular and extensible:

1. Add new visualization components by creating classes that render to a Pygame surface
2. Register components with the PyGameVisualizer
3. Subscribe to events using the observer pattern in GameManager

## Themes

The visualization supports multiple themes:

- `default`: Light theme with blue accents
- `dark`: Dark theme with white text and adjusted colors
- `colorblind`: Colorblind-friendly theme with accessible color combinations

You can create custom themes by adding new theme definitions to `themes.py`.