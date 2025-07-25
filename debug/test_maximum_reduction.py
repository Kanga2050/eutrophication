import sys
import os
# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#!/usr/bin/env python3
"""
Test the enhanced sign analysis with expressions that should show maximum case reduction.
"""
from sympy import symbols, parse_expr
from solver import solve_rational_ineq_full

def test_maximum_case_reduction():
    """Test cases where sign analysis should provide maximum benefit."""
    x = symbols('x')
    
    print("=== MAXIMUM CASE REDUCTION TEST ===")
    print("Testing expressions where numerator is always positive")
    print()
    
    test_cases = [
        # Always positive numerator / variable denominator
        ("(x**2 + 1) / (x - 3)", ">"),  # x² + 1 always positive
        ("(a*x**2 + b*y**2) / (x + 2)", ">="),  # sum of positive*squares 
        ("abs(x) / (x - 1)", "<="),  # |x| always non-negative
        ("exp(x) / (x**2 - 4)", ">"),  # e^x always positive
        ("(x + 1)**2 / (x - 5)", ">="),  # (x+1)² always non-negative
    ]
    
    total_with = 0
    total_without = 0
    
    for expr_str, op in test_cases:
        print(f"Testing: {expr_str} {op} 0")
        print("-" * 50)
        
        expr = parse_expr(expr_str)
        
        try:
            # With sign analysis
            cases_with = solve_rational_ineq_full(expr, x, op, use_sign_analysis=True)
            print(f"WITH sign analysis: {len(cases_with)} case(s)")
            total_with += len(cases_with)
            
            # Without sign analysis
            cases_without = solve_rational_ineq_full(expr, x, op, use_sign_analysis=False)
            print(f"WITHOUT sign analysis: {len(cases_without)} case(s)")
            total_without += len(cases_without)
            
            if len(cases_without) > 0:
                reduction = ((len(cases_without) - len(cases_with)) / len(cases_without)) * 100
                print(f"Case reduction: {reduction:.1f}%")
            
        except Exception as e:
            print(f"Error: {e}")
        
        print()
    
    print("=" * 60)
    print("OVERALL RESULTS")
    print("=" * 60)
    print(f"Total cases WITH sign analysis: {total_with}")
    print(f"Total cases WITHOUT sign analysis: {total_without}")
    
    if total_without > 0:
        overall_reduction = ((total_without - total_with) / total_without) * 100
        print(f"Overall case reduction: {overall_reduction:.1f}%")
        print(f"Cases eliminated: {total_without - total_with}")

if __name__ == "__main__":
    test_maximum_case_reduction()
