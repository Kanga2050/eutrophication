import sys
import os
# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#!/usr/bin/env python3
"""
Debug test 7 to check if the result should be positive or indeterminate.
"""
from sympy import symbols, parse_expr
from sign_analyzer import create_default_analyzer

def debug_test_7():
    """Debug the analysis of test 7 expression."""
    analyzer = create_default_analyzer()
    
    print("=== DEBUGGING TEST 7 ===")
    expr_str = "((((a*b) + (c*d)) * ((e*f) + (g*h))) + (x**2 + y**2))"
    print(f"Expression: {expr_str}")
    print()
    
    # Break it down step by step
    print("Step-by-step analysis:")
    print("1. Innermost terms:")
    
    sub_expressions = [
        "a*b",      # positive * positive = positive
        "c*d",      # positive * positive = positive  
        "e*f",      # positive * positive = positive
        "g*h",      # positive * positive = positive
        "x**2",     # non-negative (positive unless x=0)
        "y**2",     # non-negative (positive unless y=0)
    ]
    
    for sub_expr in sub_expressions:
        expr = parse_expr(sub_expr)
        sign = analyzer.analyze_sign(expr)
        print(f"   {sub_expr:8} -> {sign}")
    
    print("\n2. Next level combinations:")
    
    level2_expressions = [
        "(a*b) + (c*d)",        # positive + positive = positive
        "(e*f) + (g*h)",        # positive + positive = positive  
        "x**2 + y**2",          # non-negative + non-negative = positive (unless both x=y=0)
    ]
    
    for sub_expr in level2_expressions:
        expr = parse_expr(sub_expr)
        sign = analyzer.analyze_sign(expr)
        print(f"   {sub_expr:20} -> {sign}")
    
    print("\n3. Next level:")
    
    level3_expressions = [
        "((a*b) + (c*d)) * ((e*f) + (g*h))",  # positive * positive = positive
    ]
    
    for sub_expr in level3_expressions:
        expr = parse_expr(sub_expr)
        sign = analyzer.analyze_sign(expr)
        print(f"   {sub_expr:40} -> {sign}")
    
    print("\n4. Final combination:")
    final_expr = parse_expr(expr_str)
    sign = analyzer.analyze_sign(final_expr)
    print(f"   {expr_str} -> {sign}")
    
    print("\n=== EXPECTED ANALYSIS ===")
    print("Since we assume all constants (a,b,c,d,e,f,g,h) are positive:")
    print("- a*b = positive")
    print("- c*d = positive") 
    print("- (a*b) + (c*d) = positive + positive = positive")
    print("- e*f = positive")
    print("- g*h = positive")
    print("- (e*f) + (g*h) = positive + positive = positive")
    print("- ((a*b) + (c*d)) * ((e*f) + (g*h)) = positive * positive = positive")
    print("- x**2 + y**2 = non-negative (positive unless x=y=0)")
    print("- Final: positive + positive = positive")
    print()
    print("CONCLUSION: This should be 'positive', not 'indeterminate'!")

if __name__ == "__main__":
    debug_test_7()
