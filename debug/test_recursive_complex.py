import sys
import os
# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#!/usr/bin/env python3
"""
Test the recursive binary decomposition with very complex nested expressions.
"""
from sympy import symbols, parse_expr
from sign_analyzer import create_default_analyzer

def test_complex_recursive_expressions():
    """Test deeply nested expressions that benefit from recursive decomposition."""
    analyzer = create_default_analyzer()
    
    print("=== COMPLEX RECURSIVE EXPRESSION TEST ===")
    print("Testing deeply nested expressions using binary decomposition")
    print()
    
    # Very complex expressions that would be hard to analyze with traditional approach
    complex_expressions = [
        # Nested operations
        "((a*x**2 + b) * (c*y**2 + d)) + (e*z**2 + f)",
        
        # Multiple levels of nesting  
        "(x**2 + 1) * (y**2 + 2) * (z**2 + 3)",
        
        # Mixed operations
        "((a + b)**2 + (c + d)**2) * (x**2 + y**2)",
        
        # Recursive squares
        "(((x + 1)**2 + (y + 2)**2)**2 + (z + 3)**2)",
        
        # Complex sums with products
        "a*x**2*y**2 + b*z**2*w**2 + c*u**2*v**2",
        
        # Nested absolute values and exponentials
        "abs(x*y) * exp(z**2) + sqrt(a**2 + b**2)",
        
        # Very deep nesting
        "((((a*b) + (c*d)) * ((e*f) + (g*h))) + (x**2 + y**2))",
    ]
    
    print("Expression Analysis:")
    print("-" * 60)
    
    for i, expr_str in enumerate(complex_expressions, 1):
        try:
            expr = parse_expr(expr_str)
            sign = analyzer.analyze_sign(expr)
            
            print(f"Test {i}:")
            print(f"  Expression: {expr_str}")
            print(f"  Result: {sign}")
            print(f"  Explanation: {get_explanation(expr_str, sign)}")
            print()
            
        except Exception as e:
            print(f"Test {i}: Error analyzing {expr_str}")
            print(f"  Error: {e}")
            print()

def get_explanation(expr_str, sign):
    """Provide explanation for why the expression has the given sign."""
    if sign == 'positive':
        if 'x**2' in expr_str or 'y**2' in expr_str or 'z**2' in expr_str:
            if '+' in expr_str and '*' in expr_str:
                return "Product/sum of positive terms (squares + positive constants)"
            elif '*' in expr_str:
                return "Product of positive terms" 
            else:
                return "Sum includes squares and positive terms"
        elif 'abs(' in expr_str or 'exp(' in expr_str:
            return "Includes always-positive functions"
        else:
            return "Combination of positive constants and operations"
    elif sign == 'indeterminate':
        return "Contains terms that could be positive or negative"
    elif sign == 'negative':
        return "Dominated by negative terms"
    else:
        return f"Expression evaluates to {sign}"

def show_recursive_breakdown():
    """Show how the recursive algorithm breaks down a complex expression."""
    analyzer = create_default_analyzer()
    
    print("=== RECURSIVE BREAKDOWN EXAMPLE ===")
    print("Showing how (a*x**2 + b*y**2) * (c + d) is analyzed:")
    print()
    
    # Step by step breakdown
    expr_str = "(a*x**2 + b*y**2) * (c + d)"
    expr = parse_expr(expr_str)
    
    print(f"Main expression: {expr_str}")
    print("Recursive breakdown:")
    print("  1. Split into: (a*x**2 + b*y**2) * (c + d)")
    print("  2. Analyze left side: (a*x**2 + b*y**2)")
    print("     - Split into: (a*x**2) + (b*y**2)")
    print("     - a*x**2: positive * non-negative = positive")
    print("     - b*y**2: positive * non-negative = positive") 
    print("     - Combine: positive + positive = positive")
    print("  3. Analyze right side: (c + d)")
    print("     - c: positive (assumption)")
    print("     - d: positive (assumption)")
    print("     - Combine: positive + positive = positive")
    print("  4. Final combination: positive * positive = positive")
    print()
    
    result = analyzer.analyze_sign(expr)
    print(f"Final result: {result}")

if __name__ == "__main__":
    test_complex_recursive_expressions()
    print()
    show_recursive_breakdown()
