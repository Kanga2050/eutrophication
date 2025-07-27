"""
Test the sign analysis behavior specifically
"""

from solver import solve_rational_ineq_full
from sympy import symbols

def test_sign_analysis_behavior():
    """Test how sign analysis handles rational expressions."""
    
    print("=" * 60)
    print("TESTING SIGN ANALYSIS BEHAVIOR")
    print("=" * 60)
    
    x1, x2 = symbols('x1 x2')
    expr = x1/(x2 + 2)  # Our rational expression
    variable = x1
    op = '>='
    
    print(f"Expression: {expr} {op} 0")
    print(f"Variable: {variable}")
    print()
    
    # Test with sign analysis
    print("WITH SIGN ANALYSIS:")
    print("-" * 30)
    result_with_sign = solve_rational_ineq_full(expr, variable, op, use_sign_analysis=True)
    print("Result:")
    for i, case in enumerate(result_with_sign):
        print(f"  Case {i+1}: {repr(case)}")
    print()
    
    # Test without sign analysis
    print("WITHOUT SIGN ANALYSIS:")
    print("-" * 30)
    result_without_sign = solve_rational_ineq_full(expr, variable, op, use_sign_analysis=False)
    print("Result:")
    for i, case in enumerate(result_without_sign):
        print(f"  Case {i+1}: {repr(case)}")
    print()
    
    # Let's also test a simpler case for comparison
    print("=" * 60)
    print("COMPARISON: SIMPLE LINEAR CASE")
    print("=" * 60)
    
    simple_expr = x1 - x2
    print(f"Expression: {simple_expr} {op} 1")
    
    print("WITH SIGN ANALYSIS:")
    simple_with_sign = solve_rational_ineq_full(simple_expr, variable, op, use_sign_analysis=True)
    for case in simple_with_sign:
        print(f"  {repr(case)}")
    
    print("WITHOUT SIGN ANALYSIS:")
    simple_without_sign = solve_rational_ineq_full(simple_expr, variable, op, use_sign_analysis=False)
    for case in simple_without_sign:
        print(f"  {repr(case)}")

if __name__ == "__main__":
    test_sign_analysis_behavior()
