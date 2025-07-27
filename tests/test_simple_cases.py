"""
Simple Test Case for Manual Verification
Let's start with a purely linear system that we can verify completely.
"""

from variable_eliminator import solve_with_variable_elimination

def test_simple_linear():
    """Test with a simple linear system we can solve by hand."""
    
    print("=" * 80)
    print("SIMPLE LINEAR TEST")
    print("=" * 80)
    
    # Very simple system
    inequalities = [
        'x1 + x2 <= 5',     # x1 <= 5 - x2
        'x1 - x2 >= 1',     # x1 >= x2 + 1
    ]
    
    print("Test System:")
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    print()
    
    print("Manual Analysis:")
    print("From x1 + x2 <= 5: x1 <= 5 - x2")
    print("From x1 - x2 >= 1: x1 >= x2 + 1")
    print("Elimination constraint: x2 + 1 <= 5 - x2")
    print("Simplifying: 2*x2 <= 4, so x2 <= 2")
    print("Expected final result: x2 <= 2")
    print()
    
    # Run our solver
    result = solve_with_variable_elimination(
        inequalities, 
        ['x1'], 
        use_sign_analysis=True,
        save_latex=True,
        output_filename='simple_linear_test'
    )
    
    print("\n" + "=" * 80)
    print("COMPARISON WITH SOLVER OUTPUT")
    print("=" * 80)
    
    print("Final inequalities after elimination:")
    for lhs, op, rhs in result['final_inequalities']:
        print(f"  {lhs} {op} {rhs}")
    
    print("\nExpected: x2 <= 2")
    print("Do they match?")
    
    return result

def test_with_parameter():
    """Test with a system involving a parameter."""
    
    print("\n" + "=" * 80)
    print("PARAMETER TEST")
    print("=" * 80)
    
    # System with parameter
    inequalities = [
        'x1 + x2 <= a',     # x1 <= a - x2
        'x1 >= b',          # x1 >= b
    ]
    
    print("Test System:")
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    print()
    
    print("Manual Analysis:")
    print("From x1 + x2 <= a: x1 <= a - x2")
    print("From x1 >= b: x1 >= b")
    print("Elimination constraint: b <= a - x2")
    print("Simplifying: x2 <= a - b")
    print("Expected final result: x2 <= a - b")
    print()
    
    # Run our solver
    result = solve_with_variable_elimination(
        inequalities, 
        ['x1'], 
        use_sign_analysis=True,
        save_latex=True,
        output_filename='parameter_test'
    )
    
    print("Final inequalities after elimination:")
    for lhs, op, rhs in result['final_inequalities']:
        print(f"  {lhs} {op} {rhs}")
    
    print("\nExpected: x2 <= a - b")
    
    return result

if __name__ == "__main__":
    test_simple_linear()
    test_with_parameter()
