import sys
import os
# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#!/usr/bin/env python3
"""
Test script for sign analysis integration with the rational inequality solver.
"""
from sympy import symbols, parse_expr
from solver import solve_rational_ineq_full

def test_sign_analysis_integration():
    """Test the sign analysis integration with various expressions."""
    x = symbols('x')
    
    test_cases = [
        # Expression with positive denominator
        ("(x - 1) / (x**2 + 1)", "<="),  # x^2 + 1 is always positive
        
        # Expression with constant numerator
        ("3 / (x - 2)", ">"),  # Numerator is always positive
        
        # Expression with negative constant
        ("(-5) / (x + 1)", "<"),  # Numerator is always negative
        
        # More complex case
        ("(x - 1) / (2*x + 4)", ">="),  # Denominator = 2(x+2), factor 2 is positive
    ]
    
    print("=== Testing Sign Analysis Integration ===\n")
    
    for expr_str, op in test_cases:
        print(f"Testing: {expr_str} {op} 0")
        print("-" * 40)
        
        expr = parse_expr(expr_str)
        
        # Test with sign analysis enabled
        print("WITH sign analysis:")
        try:
            cases_with = solve_rational_ineq_full(expr, x, op, use_sign_analysis=True)
            for i, case in enumerate(cases_with, 1):
                print(f"  Case {i}: {case}")
        except Exception as e:
            print(f"  Error: {e}")
        
        print("\nWITHOUT sign analysis:")
        try:
            cases_without = solve_rational_ineq_full(expr, x, op, use_sign_analysis=False)
            for i, case in enumerate(cases_without, 1):
                print(f"  Case {i}: {case}")
        except Exception as e:
            print(f"  Error: {e}")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    test_sign_analysis_integration()
