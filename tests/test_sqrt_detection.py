#!/usr/bin/env python3
"""
Test square root detection in SymPy expressions.
"""

from sympy import symbols, sqrt, simplify

def test_sqrt_detection():
    x2 = symbols('x2')
    expr = 1.0 - 1.0*sqrt(4 - x2)
    
    print(f"Expression: {expr}")
    print(f"Type: {type(expr)}")
    print(f"Has sqrt: {expr.has(sqrt)}")
    
    # Try different ways to find square roots
    print(f"Find sqrt: {list(expr.find(sqrt))}")
    
    # Another approach
    from sympy import Pow
    print(f"Find Pow: {list(expr.find(Pow))}")
    
    # Check if any powers have rational exponents
    for pow_expr in expr.find(Pow):
        print(f"Power: {pow_expr}, exponent: {pow_expr.args[1]}")
        if pow_expr.args[1] == 0.5:
            print(f"  This is a square root of: {pow_expr.args[0]}")

if __name__ == "__main__":
    test_sqrt_detection()
