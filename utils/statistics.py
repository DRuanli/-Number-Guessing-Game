"""
Statistics module for the Genetic Algorithm Number Guessing Game.

This module provides functionality to track, analyze, and visualize
the performance of the genetic algorithm.
"""

import json
import os
import time
from typing import Dict, List, Any, Optional, Tuple
import statistics as stats


class StatisticsTracker:
    """
    Tracks and analyzes statistics for the genetic algorithm.
    
    This class collects, processes, and visualizes performance data
    to evaluate the effectiveness of the genetic algorithm.
    """
    
    def __init__(self):
        """
        Initialize the statistics tracker.
        """
        # Game configuration
        self.config = {}
        
        # Game result
        self.secret_number = None
        self.found_number = None
        self.success = False
        
        # Performance metrics
        self.start_time = None
        self.end_time = None
        self.total_time = None
        self.generations = 0
        self.evaluations = 0
        
        # Generation history
        self.generation_history = []
        
        # Convergence tracking
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.best_guess_history = []
        self.diversity_history = []
        
        # Performance analysis
        self.analysis_results = {}
    
    def start_tracking(self, config: Dict[str, Any], secret_number: int) -> None:
        """
        Start tracking statistics for a new game.
        
        Args:
            config: The game configuration
            secret_number: The secret number to guess
        """
        self.config = config.copy()
        self.secret_number = secret_number
        self.start_time = time.time()
        self.generations = 0
        self.evaluations = 0
        self.generation_history = []
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.best_guess_history = []
        self.diversity_history = []
        self.analysis_results = {}
        self.success = False
    
    def end_tracking(self, success: bool, found_number: Optional[int] = None) -> None:
        """
        End tracking and finalize statistics.
        
        Args:
            success: Whether the algorithm successfully found the secret number
            found_number: The final guess if successful
        """
        self.end_time = time.time()
        self.total_time = self.end_time - self.start_time
        self.success = success
        self.found_number = found_number
        
        # Run analysis
        self._analyze_performance()
    
    def record_generation(self, generation_data: Dict[str, Any]) -> None:
        """
        Record statistics for a single generation.
        
        Args:
            generation_data: Dictionary containing generation statistics
        """
        self.generations += 1
        
        # Add timestamp
        generation_data['timestamp'] = time.time()
        
        # Record generation data
        self.generation_history.append(generation_data)
        
        # Update tracking histories
        if 'best_fitness' in generation_data:
            self.best_fitness_history.append(generation_data['best_fitness'])
        
        if 'avg_fitness' in generation_data:
            self.avg_fitness_history.append(generation_data['avg_fitness'])
        
        if 'best_guess' in generation_data:
            self.best_guess_history.append(generation_data['best_guess'])
        
        if 'diversity' in generation_data:
            self.diversity_history.append(generation_data['diversity'])
        
        # Update evaluations counter
        if 'population_size' in generation_data:
            self.evaluations += generation_data['population_size']
        elif 'population_size' in self.config:
            self.evaluations += self.config['POPULATION_SIZE']
    
    def _analyze_performance(self) -> None:
        """
        Analyze the algorithm's performance.
        """
        analysis = {}
        
        # Basic performance metrics
        analysis['success'] = self.success
        analysis['generations'] = self.generations
        analysis['evaluations'] = self.evaluations
        analysis['total_time'] = self.total_time
        analysis['evaluations_per_second'] = self.evaluations / self.total_time if self.total_time > 0 else 0
        
        # Fitness progression
        if self.best_fitness_history:
            analysis['initial_best_fitness'] = self.best_fitness_history[0]
            analysis['final_best_fitness'] = self.best_fitness_history[-1]
            analysis['best_fitness_improvement'] = analysis['final_best_fitness'] - analysis['initial_best_fitness']
        
        # Convergence analysis
        if self.success and len(self.best_fitness_history) > 1:
            # Find generations to reach certain fitness thresholds
            gen_50 = self._generations_to_reach(50)
            gen_90 = self._generations_to_reach(90)
            gen_95 = self._generations_to_reach(95)
            gen_99 = self._generations_to_reach(99)
            
            analysis['generations_to_50_percent'] = gen_50
            analysis['generations_to_90_percent'] = gen_90
            analysis['generations_to_95_percent'] = gen_95
            analysis['generations_to_99_percent'] = gen_99
            
            # Calculate improvement rate
            if gen_90 is not None and gen_90 > 0:
                analysis['improvement_rate_to_90'] = 90 / gen_90
            
            # Identify plateaus (periods of no improvement)
            plateaus = self._identify_plateaus(5)  # Plateau defined as 5+ generations with no improvement
            analysis['plateau_count'] = len(plateaus)
            analysis['longest_plateau'] = max(plateaus, key=lambda x: x[1] - x[0])[1] - max(plateaus, key=lambda x: x[1] - x[0])[0] if plateaus else 0
            analysis['plateau_generations'] = sum(p[1] - p[0] for p in plateaus)
        
        # Diversity analysis
        if self.diversity_history:
            analysis['initial_diversity'] = self.diversity_history[0]
            analysis['final_diversity'] = self.diversity_history[-1]
            analysis['avg_diversity'] = stats.mean(self.diversity_history) if self.diversity_history else 0
            analysis['diversity_loss'] = analysis['initial_diversity'] - analysis['final_diversity']
        
        # Store the analysis results
        self.analysis_results = analysis
    
    def _generations_to_reach(self, fitness_threshold: float) -> Optional[int]:
        """
        Calculate how many generations it took to reach a fitness threshold.
        
        Args:
            fitness_threshold: The fitness threshold to check
            
        Returns:
            Optional[int]: The number of generations, or None if not reached
        """
        for i, fitness in enumerate(self.best_fitness_history):
            if fitness >= fitness_threshold:
                return i + 1
        return None
    
    def _identify_plateaus(self, min_length: int) -> List[Tuple[int, int]]:
        """
        Identify plateaus in the fitness progression.
        
        Args:
            min_length: The minimum number of generations to consider a plateau
            
        Returns:
            List[Tuple[int, int]]: List of plateau intervals (start_gen, end_gen)
        """
        plateaus = []
        
        if len(self.best_fitness_history) < min_length:
            return plateaus
        
        plateau_start = None
        prev_fitness = self.best_fitness_history[0]
        
        for i in range(1, len(self.best_fitness_history)):
            curr_fitness = self.best_fitness_history[i]
            
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
            plateau_length = len(self.best_fitness_history) - plateau_start
            if plateau_length >= min_length:
                plateaus.append((plateau_start, len(self.best_fitness_history) - 1))
        
        return plateaus
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the statistics.
        
        Returns:
            Dict[str, Any]: Dictionary containing summary statistics
        """
        summary = {
            'secret_number': self.secret_number,
            'found_number': self.found_number,
            'success': self.success,
            'generations': self.generations,
            'evaluations': self.evaluations,
            'total_time': self.total_time,
        }
        
        if self.best_fitness_history:
            summary['initial_fitness'] = self.best_fitness_history[0]
            summary['final_fitness'] = self.best_fitness_history[-1]
        
        # Add key analysis results
        for key in ['generations_to_90_percent', 'generations_to_99_percent', 
                   'improvement_rate_to_90', 'plateau_count']:
            if key in self.analysis_results:
                summary[key] = self.analysis_results[key]
        
        return summary
    
    def get_detailed_analysis(self) -> Dict[str, Any]:
        """
        Get a detailed analysis of the statistics.
        
        Returns:
            Dict[str, Any]: Dictionary containing detailed analysis
        """
        # Include all analysis results
        analysis = self.analysis_results.copy()
        
        # Add improvement tracking
        if len(self.best_fitness_history) > 1:
            improvements = []
            prev_fitness = self.best_fitness_history[0]
            
            for i, fitness in enumerate(self.best_fitness_history[1:], 1):
                if fitness > prev_fitness:
                    improvement = fitness - prev_fitness
                    improvements.append({
                        'generation': i,
                        'improvement': improvement,
                        'from': prev_fitness,
                        'to': fitness
                    })
                prev_fitness = fitness
            
            analysis['improvements'] = improvements
            
            if improvements:
                max_improvement = max(improvements, key=lambda x: x['improvement'])
                analysis['largest_improvement'] = max_improvement
        
        return analysis
    
    def get_generation_data(self, generation: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get data for a specific generation or all generations.
        
        Args:
            generation: The generation number, or None for all generations
            
        Returns:
            List[Dict[str, Any]]: List of generation data dictionaries
        """
        if generation is None:
            return self.generation_history
        
        if 0 <= generation < len(self.generation_history):
            return [self.generation_history[generation]]
        
        return []
    
    def save_to_file(self, filepath: str) -> bool:
        """
        Save statistics to a JSON file.
        
        Args:
            filepath: The file path to save to
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = {
                'config': self.config,
                'secret_number': self.secret_number,
                'found_number': self.found_number,
                'success': self.success,
                'start_time': self.start_time,
                'end_time': self.end_time,
                'total_time': self.total_time,
                'generations': self.generations,
                'evaluations': self.evaluations,
                'generation_history': self.generation_history,
                'analysis': self.analysis_results
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            
            return True
        except Exception:
            return False
    
    @classmethod
    def load_from_file(cls, filepath: str) -> Optional['StatisticsTracker']:
        """
        Load statistics from a JSON file.
        
        Args:
            filepath: The file path to load from
            
        Returns:
            Optional[StatisticsTracker]: A new StatisticsTracker object, or None if loading fails
        """
        try:
            if not os.path.exists(filepath):
                return None
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            tracker = cls()
            
            # Load basic data
            tracker.config = data.get('config', {})
            tracker.secret_number = data.get('secret_number')
            tracker.found_number = data.get('found_number')
            tracker.success = data.get('success', False)
            tracker.start_time = data.get('start_time')
            tracker.end_time = data.get('end_time')
            tracker.total_time = data.get('total_time')
            tracker.generations = data.get('generations', 0)
            tracker.evaluations = data.get('evaluations', 0)
            
            # Load generation history
            tracker.generation_history = data.get('generation_history', [])
            
            # Extract tracking histories from generation history
            for gen_data in tracker.generation_history:
                if 'best_fitness' in gen_data:
                    tracker.best_fitness_history.append(gen_data['best_fitness'])
                
                if 'avg_fitness' in gen_data:
                    tracker.avg_fitness_history.append(gen_data['avg_fitness'])
                
                if 'best_guess' in gen_data:
                    tracker.best_guess_history.append(gen_data['best_guess'])
                
                if 'diversity' in gen_data:
                    tracker.diversity_history.append(gen_data['diversity'])
            
            # Load analysis results
            tracker.analysis_results = data.get('analysis', {})
            
            return tracker
        except Exception:
            return None
    
    def generate_text_report(self) -> str:
        """
        Generate a text-based report of the statistics.
        
        Returns:
            str: A formatted text report
        """
        report = []
        
        # Header
        report.append("=" * 60)
        report.append("GENETIC ALGORITHM PERFORMANCE REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Basic information
        report.append("Basic Information:")
        report.append(f"  Secret Number: {self.secret_number}")
        report.append(f"  Success: {'Yes' if self.success else 'No'}")
        if self.success:
            report.append(f"  Number Found: {self.found_number}")
        report.append(f"  Generations Run: {self.generations}")
        report.append(f"  Total Evaluations: {self.evaluations}")
        report.append(f"  Total Time: {self.total_time:.2f} seconds")
        report.append(f"  Evaluations per Second: {self.evaluations / self.total_time if self.total_time > 0 else 0:.2f}")
        report.append("")
        
        # Configuration
        report.append("Configuration:")
        for key, value in self.config.items():
            report.append(f"  {key}: {value}")
        report.append("")
        
        # Performance analysis
        if self.analysis_results:
            report.append("Performance Analysis:")
            
            if 'initial_best_fitness' in self.analysis_results:
                report.append(f"  Initial Best Fitness: {self.analysis_results['initial_best_fitness']:.2f}")
            
            if 'final_best_fitness' in self.analysis_results:
                report.append(f"  Final Best Fitness: {self.analysis_results['final_best_fitness']:.2f}")
            
            if 'best_fitness_improvement' in self.analysis_results:
                report.append(f"  Fitness Improvement: {self.analysis_results['best_fitness_improvement']:.2f}")
            
            if 'generations_to_90_percent' in self.analysis_results:
                if self.analysis_results['generations_to_90_percent'] is not None:
                    report.append(f"  Generations to 90% Fitness: {self.analysis_results['generations_to_90_percent']}")
                else:
                    report.append("  90% Fitness Level Not Reached")
            
            if 'generations_to_99_percent' in self.analysis_results:
                if self.analysis_results['generations_to_99_percent'] is not None:
                    report.append(f"  Generations to 99% Fitness: {self.analysis_results['generations_to_99_percent']}")
                else:
                    report.append("  99% Fitness Level Not Reached")
            
            if 'plateau_count' in self.analysis_results:
                report.append(f"  Number of Plateaus: {self.analysis_results['plateau_count']}")
            
            if 'longest_plateau' in self.analysis_results:
                report.append(f"  Longest Plateau: {self.analysis_results['longest_plateau']} generations")
            
            if 'avg_diversity' in self.analysis_results:
                report.append(f"  Average Population Diversity: {self.analysis_results['avg_diversity']:.2f}")
            
            report.append("")
        
        # Convergence visualization (simple ASCII chart)
        if self.best_fitness_history:
            report.append("Fitness Convergence:")
            report.append(self._generate_ascii_chart(self.best_fitness_history, 40, 10))
            report.append("")
        
        # Conclusion
        report.append("Conclusion:")
        if self.success:
            report.append(f"  The genetic algorithm successfully found the secret number {self.secret_number}")
            report.append(f"  in {self.generations} generations and {self.total_time:.2f} seconds.")
        else:
            report.append("  The genetic algorithm did not find the exact solution.")
            if self.best_guess_history:
                report.append(f"  Best guess: {self.best_guess_history[-1]} with fitness: {self.best_fitness_history[-1]:.2f}")
        report.append("")
        
        return "\n".join(report)
    
    def _generate_ascii_chart(self, data: List[float], width: int = 40, height: int = 10) -> str:
        """
        Generate a simple ASCII chart of the data.
        
        Args:
            data: The data to visualize
            width: The width of the chart
            height: The height of the chart
            
        Returns:
            str: A formatted ASCII chart
        """
        if not data:
            return "No data to visualize"
        
        # Determine data range
        min_val = min(data)
        max_val = max(data)
        
        # Avoid division by zero
        if max_val == min_val:
            max_val = min_val + 1
        
        # Create the chart
        chart = []
        
        # Add top border
        chart.append("+" + "-" * width + "+")
        
        # Create rows
        for row in range(height):
            threshold = min_val + (max_val - min_val) * (height - row - 1) / height
            
            line = "|"
            for col in range(width):
                data_idx = int(col * len(data) / width)
                
                if data_idx < len(data) and data[data_idx] >= threshold:
                    line += "#"
                else:
                    line += " "
            
            line += "|"
            chart.append(line)
        
        # Add bottom border
        chart.append("+" + "-" * width + "+")
        
        # Add labels
        chart.append(f"0{' ' * (width - 7)}Generations")
        
        # Add a legend
        chart.append(f"Min: {min_val:.2f}, Max: {max_val:.2f}")
        
        return "\n".join(chart)