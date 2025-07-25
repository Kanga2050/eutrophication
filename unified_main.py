"""
Unified Rational Inequality Solver with Variable Elimination.

This script provides both the original rational inequality solving functionality
and the new enhanced variable elimination capabilities in one integrated interface.
"""
from sympy import symbols
from datetime import datetime

# Import original functionality
from solver import solve_rational_ineq_full
from case_processor import generate_case_labeled_bounds
from input_processor import process_inequalities, validate_processed_inequalities
from latex_processor import process_and_save_latex, generate_summary_report

# Import new variable elimination functionality
from variable_eliminator import solve_with_variable_elimination


def demonstrate_original_solver():
    """Demonstrate the original solver functionality."""
    print("=" * 80)
    print("ORIGINAL RATIONAL INEQUALITY SOLVER")
    print("=" * 80)
    
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
    
    print("Processing inequalities with original solver...")
    
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
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            saved_files = process_and_save_latex(results, f"original_solver_{timestamp}")
            summary = generate_summary_report(results, saved_files)
            
            print("\n" + "="*80)
            print("ORIGINAL SOLVER COMPLETED")
            print("="*80)
            print(summary)
            print()
            
        except Exception as latex_error:
            print(f"LaTeX processing error: {latex_error}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def demonstrate_variable_elimination():
    """Demonstrate the enhanced variable elimination functionality."""
    print("=" * 80)
    print("ENHANCED VARIABLE ELIMINATION SOLVER")  
    print("=" * 80)
    
    # Example system for variable elimination
    inequalities = [
        # Multi-variable system
        "x1**2 + x2 - 4 >= 0",
        "x1 + 2*x2 + x3 >= 1",
        "x2 - x3 <= 2",
        "x1 - x3 >= -1",
        
        # Parameter constraints (will be preserved)
        "a + b <= c",
        "d*e >= f"
    ]
    
    # Variables to eliminate in order
    variables_to_eliminate = ['x1', 'x2', 'x3']
    
    print("Input System:")
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    
    print(f"\nVariables to eliminate: {variables_to_eliminate}")
    print()
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = solve_with_variable_elimination(
            inequalities=inequalities,
            variables_to_eliminate=variables_to_eliminate,
            use_sign_analysis=True,
            save_latex=True,
            output_filename=f"variable_elimination_{timestamp}"
        )
        
        print("\n" + "="*60)
        print("VARIABLE ELIMINATION COMPLETED")
        print("="*60)
        
        print(f"Total elimination steps: {result['total_steps']}")
        print(f"Final inequalities: {len(result['final_inequalities'])}")
        print()
        
        if result['final_inequalities']:
            print("Final constraint system (no x1, x2, x3):")
            for i, (lhs, op, rhs) in enumerate(result['final_inequalities'], 1):
                print(f"  {i}. {lhs} {op} {rhs}")
        else:
            print("All variables eliminated - system reduced to feasibility check")
        
        print()
        print("Benefits of Variable Elimination:")
        print("• Systematic dimensional reduction")
        print("• Complete step-by-step documentation")
        print("• Preservation of parameter constraints")
        print("• Useful for optimization and constraint analysis")
        
        return True
        
    except Exception as e:
        print(f"Error during variable elimination: {e}")
        return False


def demonstrate_comparison():
    """Show a direct comparison between approaches."""
    print("\n" + "=" * 80)
    print("COMPARISON: ORIGINAL vs VARIABLE ELIMINATION")
    print("=" * 80)
    
    # Simple system for comparison
    simple_system = [
        "x + y >= 0",
        "x - y <= 1",
        "a + b <= c"
    ]
    
    print("Test system:")
    for ineq in simple_system:
        print(f"  {ineq}")
    print()
    
    print("ORIGINAL APPROACH:")
    print("- Isolates one variable (x) and creates min/max expressions")
    print("- Shows solution in terms of x and other variables")
    print()
    
    print("VARIABLE ELIMINATION APPROACH:")
    print("- Eliminates x AND y sequentially")  
    print("- Shows complete 4-step process for each elimination")
    print("- Final result contains only parameter constraints")
    print()
    
    # Run variable elimination on simple system
    print("Running variable elimination on test system...")
    result = solve_with_variable_elimination(
        simple_system, 
        ['x', 'y'], 
        save_latex=False
    )
    
    print(f"Result: {len(result['final_inequalities'])} final inequalities")
    if result['final_inequalities']:
        print("Final system:")
        for lhs, op, rhs in result['final_inequalities']:
            print(f"  {lhs} {op} {rhs}")
    else:
        print("All variables eliminated successfully")


def show_usage_options():
    """Show different ways to use the unified solver."""
    print("\n" + "=" * 80)
    print("USAGE OPTIONS")
    print("=" * 80)
    
    print("1. ORIGINAL SOLVER (solve for one variable):")
    print("   from solver import solve_rational_ineq_full")
    print("   from case_processor import generate_case_labeled_bounds")
    print()
    
    print("2. VARIABLE ELIMINATION (eliminate multiple variables):")
    print("   from variable_eliminator import solve_with_variable_elimination")
    print("   result = solve_with_variable_elimination(inequalities, variables)")
    print()
    
    print("3. UNIFIED INTERFACE (this script):")
    print("   python unified_main.py")
    print()
    
    print("Choose the approach based on your needs:")
    print("• Original solver: When you need min/max expressions for one variable")
    print("• Variable elimination: When you want to remove multiple variables systematically")
    print("• Unified interface: To see both approaches and compare results")


def main():
    """Main function demonstrating both original and enhanced functionality."""
    print("UNIFIED RATIONAL INEQUALITY SOLVER")
    print("Combining Original Solver + Enhanced Variable Elimination")
    print("=" * 80)
    print()
    
    # Demonstrate original functionality
    print("Part 1: Original Solver Demonstration")
    original_success = demonstrate_original_solver()
    
    print("\n" + "=" * 80)
    print()
    
    # Demonstrate variable elimination
    print("Part 2: Variable Elimination Demonstration")  
    elimination_success = demonstrate_variable_elimination()
    
    # Show comparison
    demonstrate_comparison()
    
    # Show usage options
    show_usage_options()
    
    print("\n" + "=" * 80)
    print("UNIFIED SOLVER DEMONSTRATION COMPLETE")
    print("=" * 80)
    
    if original_success and elimination_success:
        print("✅ Both original and enhanced solvers working correctly")
        print()
        print("Generated files:")
        print("• output/ - Original solver LaTeX and summaries")
        print("• output_final/ - Complete variable elimination documentation")
        print()
        print("Next steps:")
        print("• Use the original solver for single-variable analysis")
        print("• Use variable elimination for multi-variable systems")
        print("• Both approaches complement each other perfectly")
        
    else:
        print("⚠️ Some functionality may need debugging")
        print("Check error messages above for details")


if __name__ == "__main__":
    main()
