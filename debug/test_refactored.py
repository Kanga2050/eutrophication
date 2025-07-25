import sys
import os
# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
Test script to validate the refactored inequality solver.
Demonstrates bug fixes and improved functionality.
"""
import sys
import os
# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples import run_example, get_all_examples
from input_processor import process_inequalities, validate_processed_inequalities
from case_processor import generate_case_labeled_bounds
from solver import solve_rational_ineq_full
from sympy import symbols


def test_input_parsing_improvements():
    """Test improved input parsing that fixes bugs from the original code."""
    print("Testing input parsing improvements:")
    print("-" * 40)
    
    x, a, b = symbols('x a b')
    
    # Test various input formats that might have failed in the original code
    test_cases = [
        # Tuple format (lhs, op, rhs)
        (x**2 - 4, ">=", 0),
        
        # Expression-operator format  
        (x + 1, ">"),
        
        # Mixed formats
        (a*x + b, "<=", x**2),
    ]
    
    try:
        processed = process_inequalities(test_cases)
        validate_processed_inequalities(processed)
        print(f"✓ Successfully processed {len(processed)} inequalities")
        for i, (lhs, op, rhs) in enumerate(processed):
            print(f"  {i+1}: {lhs} {op} {rhs}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()


def test_error_handling():
    """Test improved error handling."""
    print("Testing error handling:")
    print("-" * 40)
    
    # Test invalid input formats
    invalid_cases = [
        ("invalid format",),  # Tuple with wrong length
        "no operator here",   # String without operator
        (None, ">=", 0),      # Invalid expression
    ]
    
    for i, invalid_case in enumerate(invalid_cases):
        try:
            process_inequalities([invalid_case])
            print(f"✗ Case {i+1}: Should have failed but didn't")
        except ValueError as e:
            print(f"✓ Case {i+1}: Correctly caught error - {str(e)[:50]}...")
        except Exception as e:
            print(f"? Case {i+1}: Unexpected error type - {type(e).__name__}")
    
    print()


def test_modular_imports():
    """Test that the modular structure works correctly."""
    print("Testing modular imports:")
    print("-" * 40)
    
    try:
        # Test importing from individual modules
        from solver import solve_rational_ineq_full
        from case_processor import generate_case_labeled_bounds, isolate_cases_from_solver
        from input_processor import process_inequalities
        from solver import solve_rational_ineq_full
        
        print("✓ All module imports successful")
        print("✓ All imports work correctly with refactored structure")
        
        # Test that the function is available
        assert solve_rational_ineq_full is not None
        print("✓ Main solver function is available from solver module")
        
    except Exception as e:
        print(f"✗ Import error: {e}")
    
    print()


def test_all_examples():
    """Test that all examples run without errors."""
    print("Testing all example cases:")
    print("-" * 40)
    
    examples = get_all_examples()
    
    for name in examples.keys():
        try:
            results = run_example(name)
            if results:
                print(f"✓ {name}: Generated {len(results)} cases")
            else:
                print(f"✗ {name}: No results generated")
        except Exception as e:
            print(f"✗ {name}: Error - {str(e)[:50]}...")
    
    print()


def main():
    """Run all tests."""
    print("="*60)
    print("REFACTORED INEQUALITY SOLVER - VALIDATION TESTS")
    print("="*60)
    print()
    
    test_input_parsing_improvements()
    test_error_handling()
    test_modular_imports()
    test_all_examples()
    
    print("="*60)
    print("All tests completed!")
    print("="*60)


if __name__ == "__main__":
    main()
