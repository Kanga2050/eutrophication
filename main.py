"""
Main execution script for the rational inequality solver.
Contains example usage and input definitions.
"""
from sympy import symbols
from solver import solve_rational_ineq_full
from case_processor import generate_case_labeled_bounds
from input_processor import process_inequalities, validate_processed_inequalities
from latex_processor import process_and_save_latex, generate_summary_report


def _simplify_for_console(latex_output):
    """
    Simplify LaTeX output for console display.
    
    Args:
        latex_output: Full LaTeX string
        
    Returns:
        Simplified string for console display
    """
    # Extract case information
    parts = latex_output.split(r'\\[1em]')
    
    if len(parts) < 3:
        return latex_output[:200] + "..." if len(latex_output) > 200 else latex_output
    
    # Get case header
    case_header = parts[0].replace(r'\textbf{', '').replace('}', '').replace(r' \\ ', ' | ')
    
    # Extract constraints and bounds from the bounds expressions
    bounds_part = parts[1] if len(parts) > 1 else ""
    
    # Extract constraint and bound information
    if r'\wedge' in bounds_part:
        constraint_match = bounds_part.split(r'\wedge')[0]
        constraint = constraint_match.replace(r'\left\{', '').replace(r'\text{', '').replace('}', '').strip()
        
        bound_match = bounds_part.split(r'\wedge')[1] if len(bounds_part.split(r'\wedge')) > 1 else ""
        bound = bound_match.replace(r'\right\}', '').replace(r'\left(', '').replace(r'\right)', '').strip()
        
        # Simplify long bounds
        if len(bound) > 100:
            bound = bound[:97] + "..."
        
        if constraint and constraint != '(no additional constraints)':
            return f"Conditions: {constraint}\nBounds: {bound}"
        else:
            return f"Bounds: {bound}"
    
    return latex_output[:150] + "..." if len(latex_output) > 150 else latex_output


def main():
    """Main function demonstrating the inequality solver."""
    # Define symbols
    x, a, b, c, d, e, f, g = symbols('x a b c d e f g')
    
    # Define inequalities in various formats
    ineqs = [
        # Complex rational inequality
        ((a*x - c + b - 1)/(a*b*d) - b/a + 1/a + (b*d*c)/a - 
         (x - e*f*c + (b - 1 - b*d*c)*(e*f + g*x)) / (g*c + 1 - c*f*a - g*x), "<="),
        
        # Simple rational inequality
        ((x + 1)*(x - 2)/(x + 3), ">="),
        
        # Constraint not involving x
        (a + b, "<=", c),
    ]
    
    print("Processing inequalities...")
    
    try:
        # Process inequalities into standard format
        processed_ineqs = process_inequalities(ineqs)
        
        # Validate the processed inequalities
        validate_processed_inequalities(processed_ineqs)
        
        print(f"Successfully processed {len(processed_ineqs)} inequalities")
        
        # Generate case-labeled bounds
        results = generate_case_labeled_bounds(processed_ineqs, x, solve_rational_ineq_full)
        
        # Process and save LaTeX results
        try:
            saved_files = process_and_save_latex(results, "main_example_solutions")
            summary = generate_summary_report(results, saved_files)
            
            print("\n" + "="*80)
            print("LATEX PROCESSING COMPLETED")
            print("="*80)
            print(summary)
            print()
            
        except Exception as latex_error:
            print(f"LaTeX processing error: {latex_error}")
        
        # Print simplified results to console
        print("\n" + "="*80)
        print("INEQUALITY SOLVER RESULTS (Console Summary)")
        print("="*80)
        
        for i, latex_output in enumerate(results):
            print(f"\n--- Case {i+1} ---")
            # Print a simplified version for console readability
            simplified = _simplify_for_console(latex_output)
            print(simplified)
            print()
            
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True


def run_simple_example():
    """Run a simpler example for testing."""
    x = symbols('x')
    
    # Simple quadratic inequality
    simple_ineqs = [
        (x**2 - 4, ">=", 0),
        (x + 1, ">", 0)
    ]
    
    print("Running simple example...")
    
    try:
        processed_ineqs = process_inequalities(simple_ineqs)
        validate_processed_inequalities(processed_ineqs)
        
        results = generate_case_labeled_bounds(processed_ineqs, x, solve_rational_ineq_full)
        
        # Save LaTeX results for simple example
        try:
            saved_files = process_and_save_latex(results, "simple_example_solutions")
            print(f"Simple example LaTeX saved to: {saved_files.get('simple', 'N/A')}")
            print(f"Copy-paste ready file: {saved_files.get('clean', 'N/A')}")
        except Exception as latex_error:
            print(f"Simple example LaTeX error: {latex_error}")
        
        print("\nSimple Example Results (Console):")
        for i, result in enumerate(results):
            print(f"Case {i+1}: {_simplify_for_console(result)}")
            print()
            
    except Exception as e:
        print(f"Simple example error: {e}")


if __name__ == "__main__":
    print("Rational Inequality Solver")
    print("-" * 40)
    
    # Run the main example
    success = main()
    
    if success:
        print("\nRunning additional simple example...")
        run_simple_example()
    
    print("\nDone!")
