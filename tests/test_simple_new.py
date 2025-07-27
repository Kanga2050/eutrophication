"""
Test the simple linear case with our new approach
"""

from variable_eliminator import solve_with_variable_elimination

def test_simple_linear_new():
    """Test with a simple linear system using the new approach."""
    
    print("=" * 80)
    print("SIMPLE LINEAR TEST WITH NEW APPROACH")
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
    
    # Run our solver
    result = solve_with_variable_elimination(
        inequalities, 
        ['x1'], 
        use_sign_analysis=False,  # Use without sign analysis
        save_latex=True,
        output_filename='simple_linear_new_approach'
    )
    
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    
    print("Final inequalities after elimination:")
    for lhs, op, rhs in result['final_inequalities']:
        print(f"  {lhs} {op} {rhs}")
    
    print("Expected: x2 + 1 <= 5 - x2 (which simplifies to x2 <= 2)")
    
    return result

if __name__ == "__main__":
    test_simple_linear_new()
