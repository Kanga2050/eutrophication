"""
Example Library for Rational Inequality Solver

This module provides a comprehensive collection of test cases and example problems
that demonstrate the capabilities of the rational inequality solver. Examples range
from simple polynomial inequalities to complex rational expressions with multiple
parameters, showcasing different features and use cases.

Example Categories:
- **Simple Examples**: Basic polynomial and linear inequalities  
- **Rational Function Examples**: Complex rational expressions with singularities
- **Parametric Examples**: Systems involving symbolic parameters
- **Multi-variable Examples**: Systems requiring variable elimination
- **Edge Cases**: Boundary conditions and special mathematical scenarios

Functions:
- get_[type]_example(): Return specific example types
- run_example(): Execute and display results for named examples
- run_all_examples(): Comprehensive demonstration of all example types

Usage:
    from examples import run_example, get_simple_quadratic_example
    
    # Run a specific example
    run_example('quadratic')
    
    # Get example data for custom processing
    ineqs = get_simple_quadratic_example()

For multi-variable elimination examples, see:
- variable_eliminator.py (VariableEliminationSolver.demo() method)  
- main.py (complete demonstrations)

Author: Rational Inequality Solver Team
Version: Comprehensive Example Library
"""
from sympy import symbols


def get_complex_example():
    """
    Return the complex multi-parameter rational inequality example.
    
    This example demonstrates the solver's ability to handle sophisticated
    rational expressions involving multiple symbolic parameters. It represents
    one of the most challenging test cases for the solver system.
    
    Mathematical Structure:
    - **Complex Rational Expression**: Multi-term rational function with nested operations
    - **Multiple Parameters**: Uses symbols a, b, c, d, e, f, g as parameters
    - **Mixed Operations**: Combines addition, subtraction, multiplication, division
    - **Parameter Constraints**: Includes constraints not involving the main variable
    
    System Components:
    1. **Primary Inequality**: Complex rational expression ≤ 0
       - Numerator: (a*x - c + b - 1) with parameter scaling
       - Denominator: (a*b*d) with nested parameter products
       - Additional terms: Multiple rational components
    
    2. **Secondary Inequality**: (x + 1)*(x - 2)/(x + 3) ≥ 0
       - Simpler rational form for comparison
       - Clear factored structure
    
    3. **Parameter Constraint**: a + b ≤ c
       - Establishes relationships between parameters
       - Tests parameter handling in case analysis
    
    Returns:
        list: List of inequality tuples in (expression, operator) or (lhs, operator, rhs) format
        
    Use Cases:
        - Testing complex rational expression parsing
        - Demonstrating multi-parameter case analysis
        - Validating LaTeX output for complex expressions
        - Benchmarking solver performance on challenging inputs
    """
    x, a, b, c, d, e, f, g = symbols('x a b c d e f g')
    
    return [
        # Complex rational inequality
        ((a*x - c + b - 1)/(a*b*d) - b/a + 1/a + (b*d*c)/a - 
         (x - e*f*c + (b - 1 - b*d*c)*(e*f + g*x)) / (g*c + 1 - c*f*a - g*x), "<="),
        
        # Simple rational inequality
        ((x + 1)*(x - 2)/(x + 3), ">="),
        
        # Constraint not involving x
        (a + b, "<=", c),
    ]


def get_simple_quadratic_example():
    """Returns a simple quadratic inequality example."""
    x = symbols('x')
    
    return [
        (x**2 - 4, ">=", 0),  # x >= 2 or x <= -2
        (x + 1, ">", 0),      # x > -1
    ]


def get_rational_function_example():
    """Returns a rational function inequality example."""
    x = symbols('x')
    
    return [
        ((x - 1)/(x + 2), "<=", 0),  # Rational inequality
        (x, "!=", -2),               # Exclude singularity
    ]


def get_polynomial_example():
    """Returns a polynomial inequality example."""
    x = symbols('x')
    
    return [
        (x**3 - x, ">", 0),     # Cubic polynomial
        (x**2 - 9, "<=", 0),    # Quadratic constraint
    ]


def get_mixed_parameters_example():
    """Returns an example with mixed parameters."""
    x, a, b = symbols('x a b')
    
    return [
        (a*x + b, ">", 0),        # Linear in x with parameters
        (x**2 - a, "<=", b),      # Quadratic with parameters
        (a, ">", 0),              # Parameter constraint
    ]


def get_all_examples():
    """Returns a dictionary of all available examples."""
    return {
        'complex': get_complex_example(),
        'quadratic': get_simple_quadratic_example(),
        'rational': get_rational_function_example(),
        'polynomial': get_polynomial_example(),
        'mixed_params': get_mixed_parameters_example(),
    }


def print_example_info():
    """Prints information about available examples."""
    examples = get_all_examples()
    
    print("Available Examples:")
    print("-" * 40)
    
    descriptions = {
        'complex': "Complex rational inequality with multiple parameters",
        'quadratic': "Simple quadratic inequality system",
        'rational': "Rational function with singularity handling",
        'polynomial': "Polynomial inequalities of different degrees",
        'mixed_params': "Mixed linear/quadratic with parameter constraints",
    }
    
    for name, description in descriptions.items():
        count = len(examples[name])
        print(f"{name:15}: {description} ({count} inequalities)")
    
    print("\nUsage: run_example('example_name')")


def run_example(example_name):
    """
    Run a specific example by name.
    
    Args:
        example_name: Name of the example to run
        
    Returns:
        Results from the inequality solver
    """
    from input_processor import process_inequalities, validate_processed_inequalities
    from case_processor import generate_case_labeled_bounds
    from solver import solve_rational_ineq_full
    from latex_processor import process_and_save_latex, generate_summary_report
    from sympy import symbols
    
    examples = get_all_examples()
    
    if example_name not in examples:
        print(f"Unknown example: {example_name}")
        print_example_info()
        return None
    
    # Get the appropriate variable symbol
    x = symbols('x')
    ineqs = examples[example_name]
    
    print(f"Running example: {example_name}")
    print("=" * 50)
    
    try:
        # Process and solve
        processed_ineqs = process_inequalities(ineqs)
        validate_processed_inequalities(processed_ineqs)
        
        print(f"Processing {len(processed_ineqs)} inequalities...")
        
        results = generate_case_labeled_bounds(processed_ineqs, x, solve_rational_ineq_full)
        
        # Process and save LaTeX results
        try:
            saved_files = process_and_save_latex(results, f"example_{example_name}")
            print(f"\nLaTeX files saved:")
            for file_type, filepath in saved_files.items():
                print(f"  {file_type.capitalize()}: {filepath}")
        except Exception as latex_error:
            print(f"LaTeX processing error: {latex_error}")
        
        # Print simplified results
        print(f"\nResults for {example_name}:")
        for i, result in enumerate(results):
            print(f"\n--- Case {i+1} ---")
            # Extract key information for display
            if r'\wedge' in result and r'\min' in result:
                parts = result.split(r'\wedge')
                if len(parts) >= 2:
                    constraint = parts[0].replace(r'\left\{', '').replace(r'\text{', '').replace('}', '').strip()
                    bounds = parts[1].split(r'\right\}')[0] if r'\right\}' in parts[1] else parts[1]
                    bounds = bounds.replace(r'\min\left(', 'min(').replace(r'\max\left(', 'max(')
                    
                    if constraint and constraint != '(no additional constraints)':
                        print(f"Constraint: {constraint}")
                    print(f"Bounds: {bounds[:100]}{'...' if len(bounds) > 100 else ''}")
                else:
                    print(result[:100] + "..." if len(result) > 100 else result)
            else:
                print(result[:100] + "..." if len(result) > 100 else result)
        
        return results
        
    except Exception as e:
        print(f"Error running example '{example_name}': {e}")
        return None


if __name__ == "__main__":
    print_example_info()
    print("\nRunning simple quadratic example...")
    run_example('quadratic')
