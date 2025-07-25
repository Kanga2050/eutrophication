import sys
import os
# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#!/usr/bin/env python3
"""
Debug the assumptions to see why e*f is not recognized as positive.
"""
from sympy import symbols, parse_expr, sympify
from sign_analyzer import create_default_analyzer

def debug_assumptions():
    """Debug why assumptions aren't working correctly."""
    analyzer = create_default_analyzer()
    
    print("=== DEBUGGING ASSUMPTIONS ===")
    print("Checking what assumptions are loaded:")
    print(f"Assumptions: {analyzer.assumptions}")
    print()
    
    print("Testing individual symbols:")
    test_symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    for symbol_str in test_symbols:
        symbol = sympify(symbol_str)
        sign = analyzer.analyze_sign(symbol)
        in_assumptions = symbol in analyzer.assumptions
        print(f"Symbol {symbol_str}: sign={sign}, in_assumptions={in_assumptions}")
        if in_assumptions:
            print(f"  Assumption value: {analyzer.assumptions[symbol]}")
    
    print("\nTesting products:")
    products = ['a*b', 'c*d', 'e*f', 'g*h']
    
    for product_str in products:
        expr = parse_expr(product_str)
        sign = analyzer.analyze_sign(expr)
        print(f"Product {product_str}: {sign}")

if __name__ == "__main__":
    debug_assumptions()
