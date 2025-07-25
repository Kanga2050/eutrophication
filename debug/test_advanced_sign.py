import sys
import os
# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#!/usr/bin/env python3
"""
Enhanced test script to demonstrate sign analysis case reduction.
"""
from sympy import symbols, parse_expr, pi, exp
from solver import solve_rational_ineq_full

def test_advanced_sign_analysis():
    """Test sign analysis with expressions that should show clear case reduction."""
    x = symbols('x')
    
    test_cases = [
        # Expression with always positive denominator
        ("(x - 1) / (x**2 + 4)", "<="),  # x^2 + 4 is always > 0
        
        # Expression with mathematical constants
        ("(x - pi) / (exp(x))", ">="),  # exp(x) is always positive
        
        # Expression where numerator is always positive
        ("(x**2 + 1) / (x - 2)", ">"),  # x^2 + 1 is always > 0
        
        # Expression with always negative numerator and positive denominator
        ("(-3) / (x**2 + 1)", "<"),  # Numerator negative, denominator always positive
    ]
    
    print("=== Advanced Sign Analysis Test ===\n")
    
    for expr_str, op in test_cases:
        print(f"Testing: {expr_str} {op} 0")
        print("-" * 50)
        
        expr = parse_expr(expr_str)
        
        # Test with sign analysis enabled
        print("WITH sign analysis:")
        try:
            cases_with = solve_rational_ineq_full(expr, x, op, use_sign_analysis=True)
            print(f"  Number of cases: {len(cases_with)}")
            for i, case in enumerate(cases_with, 1):
                print(f"  Case {i}: {case[:100]}...")
        except Exception as e:
            print(f"  Error: {e}")
        
        print("\nWITHOUT sign analysis:")
        try:
            cases_without = solve_rational_ineq_full(expr, x, op, use_sign_analysis=False)
            print(f"  Number of cases: {len(cases_without)}")
            for i, case in enumerate(cases_without, 1):
                print(f"  Case {i}: {case[:100]}...")
        except Exception as e:
            print(f"  Error: {e}")
        
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    test_advanced_sign_analysis()
