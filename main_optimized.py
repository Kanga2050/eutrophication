"""
Optimized main application script using the new architecture.
"""
import time
from pathlib import Path

from rational_inequality_solver import solve_inequality_system, DEFAULT_CONFIG
from rational_inequality_solver.examples import get_example, list_examples, print_example_info
from rational_inequality_solver.core import SolverEngine, InequalitySystem
from rational_inequality_solver.output import LaTeXFormatter, ConsoleFormatter
from config.settings import ApplicationConfig, load_config_from_file


def run_example_with_new_architecture(example_name: str, config: ApplicationConfig = None):
    """
    Run an example using the new optimized architecture.
    
    Args:
        example_name: Name of the example to run
        config: Optional configuration (uses default if None)
    """
    if config is None:
        config = ApplicationConfig()
    
    print(f"Running example: {example_name}")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Get example system
        system = get_example(example_name)
        print(f"Loaded system with {len(system)} inequalities")
        print(f"Primary variable: {system.primary_variable}")
        print(f"Variable terms: {len(system.variable_terms)}")
        print(f"Constraint terms: {len(system.constraint_terms)}")
        print()
        
        # Create solver with configuration
        solver = SolverEngine(
            use_sign_analysis=config.solver.use_sign_analysis,
            enable_caching=config.solver.cache_results,
            max_recursion_depth=config.solver.max_recursion_depth,
            timeout_seconds=config.solver.timeout_seconds
        )
        
        # Solve system
        results = solver.solve(system)
        solving_time = time.time() - start_time
        
        print(f"Solving completed in {solving_time:.3f} seconds")
        print(f"Generated {len(results)} case(s)")
        print()
        
        # Format and save outputs based on configuration
        if config.output.latex_enabled:
            latex_formatter = LaTeXFormatter(
                output_directory=config.output.output_directory,
                line_length=config.output.latex_line_length
            )
            
            saved_files = latex_formatter.format_and_save(
                results, 
                f"optimized_{example_name}",
                f"Optimized Solutions - {example_name}"
            )
            
            summary = latex_formatter.generate_summary_report(results, saved_files)
            print("LATEX OUTPUT:")
            print("-" * 40)
            print(summary)
            print()
        
        if config.output.console_enabled:
            console_formatter = ConsoleFormatter(
                line_length=config.output.console_line_length
            )
            
            formatted_output = console_formatter.format_results(results, show_details=True)
            print("CONSOLE OUTPUT:")
            print("-" * 40)
            print(formatted_output)
            print()
            
            # Show summary
            summary = console_formatter.format_summary(
                num_cases=len(results),
                num_variables=len(system.variable_terms),
                num_constraints=len(system.constraint_terms),
                processing_time=solving_time
            )
            print(summary)
            print()
        
        # Show performance statistics
        stats = solver.get_performance_stats()
        print("PERFORMANCE STATISTICS:")
        print("-" * 30)
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"Error running example '{example_name}': {e}")
        return False


def run_performance_comparison():
    """Compare performance between old and new implementations."""
    print("PERFORMANCE COMPARISON")
    print("=" * 60)
    
    # Test examples of increasing complexity
    test_examples = ['quadratic_simple', 'rational_basic', 'mixed_types', 'parametric_linear']
    
    for example_name in test_examples:
        print(f"\\nTesting: {example_name}")
        print("-" * 30)
        
        try:
            system = get_example(example_name)
            
            # Test with different configurations
            configs = {
                'optimized': ApplicationConfig(),
                'no_cache': ApplicationConfig()
            }
            configs['no_cache'].solver.cache_results = False
            
            for config_name, config in configs.items():
                solver = SolverEngine(
                    use_sign_analysis=config.solver.use_sign_analysis,
                    enable_caching=config.solver.cache_results,
                )
                
                start_time = time.time()
                results = solver.solve(system)
                end_time = time.time()
                
                stats = solver.get_performance_stats()
                
                print(f"{config_name:12}: {end_time - start_time:.4f}s, "
                      f"{len(results)} cases, "
                      f"cache hits: {stats['cache_hits']}")
                
        except Exception as e:
            print(f"Error with {example_name}: {e}")


def demonstrate_configuration_system():
    """Demonstrate the configuration system."""
    print("CONFIGURATION SYSTEM DEMO")
    print("=" * 60)
    
    # Create custom configuration
    custom_config = ApplicationConfig()
    custom_config.solver.use_sign_analysis = False
    custom_config.solver.cache_results = True
    custom_config.output.latex_line_length = 60
    custom_config.output.console_line_length = 80
    
    print("Custom configuration:")
    print("-" * 30)
    config_dict = custom_config.to_dict()
    for section, settings in config_dict.items():
        print(f"{section}:")
        for key, value in settings.items():
            print(f"  {key}: {value}")
    print()
    
    # Save and reload configuration
    config_file = Path("config/demo_config.json")
    config_file.parent.mkdir(exist_ok=True)
    
    from config.settings import save_config_to_file, load_config_from_file
    save_config_to_file(custom_config, str(config_file))
    print(f"Configuration saved to: {config_file}")
    
    # Load and use configuration
    loaded_config = load_config_from_file(str(config_file))
    print("Configuration loaded successfully")
    
    # Test with custom configuration
    print("\\nTesting with custom configuration:")
    run_example_with_new_architecture('quadratic_simple', loaded_config)


def main():
    """Main demonstration function."""
    print("RATIONAL INEQUALITY SOLVER v2.0")
    print("Optimized Architecture Demonstration")
    print("=" * 80)
    
    # Show available examples
    print("\\nAVAILABLE EXAMPLES:")
    print_example_info()
    print()
    
    # Run a simple example with new architecture
    print("\\n" + "="*80)
    print("RUNNING SIMPLE EXAMPLE")
    print("="*80)
    success = run_example_with_new_architecture('quadratic_simple')
    
    if success:
        # Run performance comparison
        print("\\n" + "="*80)
        print("PERFORMANCE COMPARISON")
        print("="*80)
        run_performance_comparison()
        
        # Demonstrate configuration system
        print("\\n" + "="*80)
        print("CONFIGURATION SYSTEM")
        print("="*80)
        demonstrate_configuration_system()
        
        # Run complex example
        print("\\n" + "="*80)
        print("COMPLEX EXAMPLE")
        print("="*80)
        run_example_with_new_architecture('mixed_types')
    
    print("\\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print("="*80)
    print("Check the 'output/' directory for generated files.")


if __name__ == "__main__":
    main()
