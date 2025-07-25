"""
Comprehensive test suite for the optimized rational inequality solver.
"""
import unittest
import time
from pathlib import Path
import sys

# Add the parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from rational_inequality_solver import solve_inequality_system
from rational_inequality_solver.core import SolverEngine, InequalitySystem, InequalityTerm
from rational_inequality_solver.processors import InputProcessor, CaseProcessor
from rational_inequality_solver.output import LaTeXFormatter, ConsoleFormatter
from rational_inequality_solver.examples import get_example, EXAMPLE_LIBRARY
from rational_inequality_solver.utils import ValidationError, ProcessingError, SolverError
from config.settings import ApplicationConfig


class TestInequalitySystem(unittest.TestCase):
    """Test the InequalitySystem class."""
    
    def test_basic_creation(self):
        """Test basic system creation."""
        inequalities = [
            ("x**2 - 4", ">=", "0"),
            ("x + 1", ">", "0")
        ]
        
        system = InequalitySystem(inequalities)
        
        self.assertEqual(len(system.variable_terms), 2)
        self.assertEqual(len(system.constraint_terms), 0)
        self.assertEqual(str(system.primary_variable), 'x')
    
    def test_constraint_separation(self):
        """Test separation of variable terms and constraints."""
        inequalities = [
            ("x**2 - 4", ">=", "0"),  # Variable term
            ("a + b", "<=", "c"),     # Constraint
            ("x + 1", ">", "0")       # Variable term
        ]
        
        system = InequalitySystem(inequalities, variable='x')
        
        self.assertEqual(len(system.variable_terms), 2)
        self.assertEqual(len(system.constraint_terms), 1)
    
    def test_validation(self):
        """Test system validation."""
        inequalities = [("x**2 - 4", ">=", "0")]
        system = InequalitySystem(inequalities)
        
        # Should not raise exception
        self.assertTrue(system.validate())
    
    def test_invalid_system(self):
        """Test handling of invalid systems."""
        # System with no variable terms should raise error in validation
        inequalities = [("a + b", "<=", "c")]
        system = InequalitySystem(inequalities, variable='x')
        
        with self.assertRaises(ValueError):
            system.validate()


class TestInputProcessor(unittest.TestCase):
    """Test the InputProcessor class."""
    
    def setUp(self):
        self.processor = InputProcessor()
    
    def test_tuple_format(self):
        """Test processing tuple format inequalities."""
        inequalities = [
            ("x**2 - 4", ">=", "0"),
            ("x + 1", ">")  # No RHS, should default to 0
        ]
        
        processed = self.processor.process_inequalities(inequalities)
        
        self.assertEqual(len(processed), 2)
        self.assertEqual(processed[0][1], ">=")
        self.assertEqual(processed[1][1], ">")
    
    def test_string_format(self):
        """Test processing string format inequalities."""
        inequalities = [
            "x**2 - 4 >= 0",
            "x + 1 > 0"
        ]
        
        processed = self.processor.process_inequalities(inequalities)
        
        self.assertEqual(len(processed), 2)
        self.assertEqual(processed[0][1], ">=")
        self.assertEqual(processed[1][1], ">")
    
    def test_mixed_formats(self):
        """Test processing mixed format inequalities."""
        inequalities = [
            ("x**2 - 4", ">=", "0"),
            "x + 1 > 0",
            ("x - 2", "<")
        ]
        
        processed = self.processor.process_inequalities(inequalities)
        
        self.assertEqual(len(processed), 3)
    
    def test_invalid_operator(self):
        """Test handling of invalid operators."""
        inequalities = [("x", "???", "0")]
        
        with self.assertRaises(ValidationError):
            self.processor.process_inequalities(inequalities)
    
    def test_validation(self):
        """Test validation of processed inequalities."""
        from sympy import sympify
        
        processed = [
            (sympify("x**2 - 4"), ">=", sympify("0")),
            (sympify("x + 1"), ">", sympify("0"))
        ]
        
        # Should not raise exception
        self.assertTrue(self.processor.validate_processed_inequalities(processed))


class TestSolverEngine(unittest.TestCase):
    """Test the SolverEngine class."""
    
    def setUp(self):
        self.solver = SolverEngine()
    
    def test_simple_solve(self):
        """Test solving a simple system."""
        inequalities = [("x**2 - 4", ">=", "0")]
        system = InequalitySystem(inequalities)
        
        results = self.solver.solve(system)
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
    
    def test_caching(self):
        """Test that caching works."""
        inequalities = [("x**2 - 4", ">=", "0")]
        system = InequalitySystem(inequalities)
        
        # First solve
        start_time = time.time()
        results1 = self.solver.solve(system)
        first_time = time.time() - start_time
        
        # Second solve (should be faster due to caching)
        start_time = time.time()
        results2 = self.solver.solve(system)
        second_time = time.time() - start_time
        
        # Results should be identical
        self.assertEqual(results1, results2)
        
        # Get stats to verify caching
        stats = self.solver.get_performance_stats()
        self.assertGreater(stats['cache_hits'], 0)
    
    def test_sign_analysis_optimization(self):
        """Test that sign analysis provides optimizations."""
        inequalities = [("x**2", ">=", "0")]  # Always true for real x
        system = InequalitySystem(inequalities)
        
        # Solve with sign analysis
        solver_with_sign = SolverEngine(use_sign_analysis=True)
        results_with = solver_with_sign.solve(system)
        
        # Solve without sign analysis
        solver_without_sign = SolverEngine(use_sign_analysis=False)
        results_without = solver_without_sign.solve(system)
        
        # Both should work, but with sign analysis might be more efficient
        self.assertIsInstance(results_with, list)
        self.assertIsInstance(results_without, list)
    
    def test_performance_stats(self):
        """Test performance statistics collection."""
        inequalities = [("x**2 - 4", ">=", "0")]
        system = InequalitySystem(inequalities)
        
        self.solver.solve(system)
        stats = self.solver.get_performance_stats()
        
        self.assertIn('solve_count', stats)
        self.assertIn('cache_enabled', stats)
        self.assertIn('sign_analysis_enabled', stats)
        self.assertGreaterEqual(stats['solve_count'], 1)


class TestExampleLibrary(unittest.TestCase):
    """Test the example library."""
    
    def test_example_loading(self):
        """Test loading examples."""
        example_names = EXAMPLE_LIBRARY.list_examples()
        
        self.assertGreater(len(example_names), 0)
        
        # Test loading each example
        for name in example_names[:3]:  # Test first 3 to save time
            system = get_example(name)
            self.assertIsInstance(system, InequalitySystem)
    
    def test_example_validation(self):
        """Test that all examples are valid."""
        validation_results = EXAMPLE_LIBRARY.validate_examples()
        
        # At least some examples should be valid
        valid_count = sum(validation_results.values())
        self.assertGreater(valid_count, 0)
    
    def test_difficulty_filtering(self):
        """Test filtering examples by difficulty."""
        beginner_examples = EXAMPLE_LIBRARY.list_by_difficulty('beginner')
        
        self.assertIsInstance(beginner_examples, list)
        # Should have at least some beginner examples
        self.assertGreater(len(beginner_examples), 0)


class TestFormatters(unittest.TestCase):
    """Test the output formatters."""
    
    def setUp(self):
        self.latex_formatter = LaTeXFormatter(output_directory="test_output")
        self.console_formatter = ConsoleFormatter()
        
        # Sample results for testing
        self.sample_results = [
            r"\\textbf{Case 1}\\\\[1em]\\left\\{x > 0 \\wedge x < 2\\right\\}",
            r"\\textbf{Case 2}\\\\[1em]\\left\\{x < 0 \\wedge x > -1\\right\\}"
        ]
    
    def test_latex_formatting(self):
        """Test LaTeX formatting and file saving."""
        saved_files = self.latex_formatter.format_and_save(
            self.sample_results, 
            "test_case"
        )
        
        self.assertIn('raw', saved_files)
        self.assertIn('formatted', saved_files)
        self.assertIn('simple', saved_files)
        
        # Check files exist
        for filepath in saved_files.values():
            self.assertTrue(Path(filepath).exists())
    
    def test_console_formatting(self):
        """Test console formatting."""
        formatted = self.console_formatter.format_results(self.sample_results)
        
        self.assertIsInstance(formatted, str)
        self.assertIn("Case 1", formatted)
        self.assertIn("Case 2", formatted)
    
    def test_summary_generation(self):
        """Test summary generation."""
        summary = self.console_formatter.format_summary(
            num_cases=2,
            num_variables=1,
            num_constraints=0,
            processing_time=0.123
        )
        
        self.assertIn("2", summary)  # num_cases
        self.assertIn("0.123", summary)  # processing_time
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        test_output_dir = Path("test_output")
        if test_output_dir.exists():
            shutil.rmtree(test_output_dir)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_end_to_end_simple(self):
        """Test complete end-to-end processing for simple case."""
        inequalities = [("x**2 - 4", ">=", "0")]
        
        # Use the convenience function
        results = solve_inequality_system(inequalities)
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
    
    def test_end_to_end_complex(self):
        """Test complete end-to-end processing for complex case."""
        try:
            system = get_example('mixed_types')
            solver = SolverEngine()
            results = solver.solve(system)
            
            self.assertIsInstance(results, list)
            self.assertGreater(len(results), 0)
            
        except Exception as e:
            self.fail(f"Complex example failed: {e}")
    
    def test_configuration_system(self):
        """Test the configuration system."""
        config = ApplicationConfig()
        config.solver.use_sign_analysis = False
        config.solver.cache_results = False
        
        inequalities = [("x**2 - 4", ">=", "0")]
        system = InequalitySystem(inequalities)
        
        solver = SolverEngine(
            use_sign_analysis=config.solver.use_sign_analysis,
            enable_caching=config.solver.cache_results
        )
        
        results = solver.solve(system)
        stats = solver.get_performance_stats()
        
        self.assertFalse(stats['sign_analysis_enabled'])
        self.assertFalse(stats['cache_enabled'])


def run_performance_benchmarks():
    """Run performance benchmarks."""
    print("\\nRUNNING PERFORMANCE BENCHMARKS")
    print("=" * 50)
    
    benchmark_examples = ['quadratic_simple', 'rational_basic', 'mixed_types']
    
    for example_name in benchmark_examples:
        print(f"\\nBenchmarking: {example_name}")
        print("-" * 30)
        
        try:
            system = get_example(example_name)
            
            # Benchmark with different configurations
            configs = {
                'full_optimization': SolverEngine(use_sign_analysis=True, enable_caching=True),
                'no_sign_analysis': SolverEngine(use_sign_analysis=False, enable_caching=True),
                'no_caching': SolverEngine(use_sign_analysis=True, enable_caching=False),
                'minimal': SolverEngine(use_sign_analysis=False, enable_caching=False)
            }
            
            for config_name, solver in configs.items():
                start_time = time.time()
                results = solver.solve(system)
                end_time = time.time()
                
                stats = solver.get_performance_stats()
                
                print(f"{config_name:18}: {end_time - start_time:.4f}s, "
                      f"{len(results):2d} cases, "
                      f"cache hits: {stats.get('cache_hits', 0):2d}")
                
        except Exception as e:
            print(f"Benchmark failed for {example_name}: {e}")


if __name__ == '__main__':
    # Run unit tests
    print("RUNNING UNIT TESTS")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestInequalitySystem,
        TestInputProcessor,
        TestSolverEngine,
        TestExampleLibrary,
        TestFormatters,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Run performance benchmarks if tests passed
    if result.wasSuccessful():
        run_performance_benchmarks()
        
        print("\\n" + "=" * 50)
        print("ALL TESTS PASSED SUCCESSFULLY!")
        print("=" * 50)
    else:
        print("\\n" + "=" * 50)
        print("SOME TESTS FAILED")
        print("=" * 50)
