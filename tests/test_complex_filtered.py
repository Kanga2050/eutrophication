#!/usr/bin/env python3

"""
Test the case-based variable elimination with complex cases to ensure filtering works properly.
"""

from variable_eliminator import VariableEliminationSolver

def test_complex_system():
    """Test a system that generates conditions requiring filtering."""
    print("="*80)
    print("COMPLEX SYSTEM TEST WITH FILTERING")
    print("="*80)
    
    # System that should generate some trivial conditions
    inequalities = [
        "x1 + 2*x2 <= 10",    # x1 <= 10 - 2*x2
        "x1 >= 3*x2",         # x1 >= 3*x2  
        "x2 >= 1",            # x2 >= 1
        "x2 <= 3"             # x2 <= 3
    ]
    
    print("Test System:")
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    
    print("\n" + "="*80)
    print("ENHANCED VARIABLE ELIMINATION SOLVER")
    print("="*80)
    
    # Create eliminator
    eliminator = VariableEliminationSolver(use_sign_analysis=False)
    
    # Test elimination
    result = eliminator.solve_with_variable_elimination(inequalities, ['x1'])
    
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    print("Final inequalities after elimination:")
    if isinstance(result, dict) and 'final_inequalities' in result:
        for i, ineq in enumerate(result['final_inequalities'], 1):
            print(f"  {i}. {ineq}")
    else:
        for i, ineq in enumerate(result, 1):
            print(f"  {i}. {ineq}")
    
    print(f"\nExpected: Conditions involving only x2")
    print("Should have proper bounds on x2 without trivial conditions like 1 > 0")

if __name__ == "__main__":
    test_complex_system()
