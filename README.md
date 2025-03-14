# -Number-Guessing-Game
# Genetic Algorithm Number Guessing Game

A Python implementation of a number guessing game that uses genetic algorithms to efficiently find a secret number specified by the user. This project demonstrates evolutionary computation principles by evolving a population of guesses over multiple generations.

## Features

- Interactive command-line interface
- Genetic algorithm implementation with configurable parameters
- Multiple selection, crossover, and mutation methods
- Comprehensive statistics tracking and performance analysis
- Colored terminal output for better visualization
- Configurable via command-line arguments or configuration files

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/genetic-algorithm-number-guessing.git
   cd genetic-algorithm-number-guessing
   ```

2. No additional dependencies are required beyond Python's standard library.

## Usage

### Basic Usage

Run the game with default settings:

```bash
python main.py
```

Follow the prompts to enter a secret number and configure the genetic algorithm parameters.

### Command-Line Options

The game supports numerous command-line options to customize its behavior:

```bash
python main.py --min 1 --max 1000 --population 50 --crossover-rate 0.8 --mutation-rate 0.1
```

#### Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `--min` | Minimum number in range | 1 |
| `--max` | Maximum number in range | 100 |
| `--population` | Population size | 20 |
| `--crossover-rate` | Crossover rate (0.0-1.0) | 0.8 |
| `--mutation-rate` | Mutation rate (0.0-1.0) | 0.1 |
| `--elitism` | Number of elite individuals | 2 |
| `--max-generations` | Maximum generations | 1000 |
| `--secret` | Secret number (skips prompt) | None |
| `--selection` | Selection method (tournament, roulette, rank) | tournament |
| `--crossover` | Crossover method (arithmetic, average, binary, binary_two_point, adaptive) | adaptive |
| `--mutation` | Mutation method (random, bit_flip, boundary, gaussian, adaptive) | adaptive |
| `--fitness` | Fitness method (linear, inverse, exponential, combined, hot_cold) | linear |
| `--config` | Path to config file | None |
| `--save-config` | Save configuration to file | None |
| `--save-stats` | Save statistics to file | None |
| `--no-color` | Disable colored output | False |
| `--quiet` | Run in quiet mode | False |

### Examples

Find a number between 1 and 1000 with a larger population:
```bash
python main.py --min 1 --max 1000 --population 50
```

Use specific genetic algorithm parameters:
```bash
python main.py --selection roulette --crossover binary --mutation gaussian
```

Provide a secret number directly (useful for testing):
```bash
python main.py --secret 42
```

Save statistics for analysis:
```bash
python main.py --save-stats stats.json
```

## How It Works

### Genetic Algorithm Approach

The genetic algorithm works as follows:

1. **Initialization**: Create a random population of individuals (guesses).
2. **Fitness Evaluation**: Calculate how close each guess is to the secret number.
3. **Selection**: Choose the best individuals for reproduction based on fitness.
4. **Crossover**: Combine pairs of individuals to create offspring.
5. **Mutation**: Introduce small random changes to maintain diversity.
6. **Replacement**: Create a new generation from offspring and elite individuals.
7. **Repeat**: Continue evolving until the correct number is found or the maximum generations is reached.

### Fitness Function

The fitness function evaluates how close a guess is to the secret number. The default linear fitness function calculates:

```
fitness = 100 * (range_size - distance) / range_size
```

Where `distance` is the absolute difference between the guess and the secret number, and `range_size` is the size of the possible number range.

## Project Structure

```
genetic_algorithm_number_guessing/
│
├── main.py                  # Entry point
│
├── game/
│   ├── __init__.py
│   ├── game_manager.py      # Game flow management
│   └── display.py           # User interface
│
├── genetic_algorithm/
│   ├── __init__.py
│   ├── individual.py        # Individual representation
│   ├── population.py        # Population management
│   ├── selection.py         # Selection methods
│   ├── crossover.py         # Crossover methods
│   ├── mutation.py          # Mutation methods
│   └── fitness.py           # Fitness calculation
│
└── utils/
    ├── __init__.py
    ├── config.py            # Configuration management
    └── statistics.py        # Statistics tracking
```

## Configuration

You can customize all genetic algorithm parameters either through command-line arguments or by creating a configuration file.

### Sample Configuration File

```json
{
    "MIN_NUMBER": 1,
    "MAX_NUMBER": 1000,
    "POPULATION_SIZE": 50,
    "CROSSOVER_RATE": 0.8,
    "MUTATION_RATE": 0.1,
    "ELITISM_COUNT": 2,
    "SELECTION_METHOD": "tournament",
    "TOURNAMENT_SIZE": 3,
    "CROSSOVER_METHOD": "adaptive",
    "MUTATION_METHOD": "adaptive",
    "FITNESS_METHOD": "linear"
}
```

Load a configuration file with:
```bash
python main.py --config myconfig.json
```

## Statistics

The game can generate detailed statistics about the genetic algorithm's performance. View these in the console (when running in verbose mode) or save them to a file:

```bash
python main.py --save-stats mystats.json
```

The statistics include:
- Generations to find the solution
- Fitness progression over time
- Convergence analysis
- Performance metrics

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project was created as a demonstration of genetic algorithms for educational purposes.
- Inspired by classic genetic algorithm demonstrations and tutorials.