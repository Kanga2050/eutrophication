import sys
import os
# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#!/usr/bin/env python3
"""
Test script to verify if assuming all symbols are positive by default works.
"""
from sympy import sympify
from sign_analyzer import SignAnalyzer, SignCombiner

def test_positive_default_assumption():
    """Test analyzer with positive default assumption for all symbols."""
    
    # Create analyzer that assumes all symbols are positive by default
    analyzer = SignAnalyzer()
    
    # Test expressions that should be positive if all symbols are positive
    test_cases = [
        ('a', 'positive'),
        ('b', 'positive'), 
        ('c', 'positive'),
        ('x', 'positive'),
        ('y', 'positive'),
        ('e', 'positive'),  # This was our bug before
        ('f', 'positive'),
        ('a*b', 'positive'),  # pos * pos = pos
        ('a + b', 'positive'),  # pos + pos = pos  
        ('a*b + c*d', 'positive'),  # pos + pos = pos
        ('e*f', 'positive'),  # This was returning indeterminate before
        ('x**2', 'positive'),  # always positive (non-zero)
        ('x**2 + 1', 'positive'),  # pos + pos = pos
        ('a*x**2 + b*y**2', 'positive'),  # pos*pos + pos*pos = pos
    ]
    
    print("Testing with modified _analyze_atomic that assumes symbols are positive...")
    print("=" * 70)
    
    # Temporarily modify the _analyze_atomic method
    original_method = analyzer._analyze_atomic
    
    def modified_analyze_atomic(self, expr):
        """Modified version that assumes all symbols are positive."""
        # Numbers
        if isinstance(expr, Number):
            if expr > 0:
                return 'positive'
            elif expr < 0:
                return 'negative'
            else:
                return 'zero'
        
        # Symbols - ASSUME ALL POSITIVE BY DEFAULT
        if isinstance(expr, Symbol):
            if expr in self.assumptions:
                return self.assumptions[expr]
            # Special constants
            if expr == pi or expr == E:
                return 'positive'
            # DEFAULT: assume positive for all symbols
            return 'positive'
        
        # Simple functions (unchanged)
        if isinstance(expr, Function):
            func_name = expr.func.__name__
            if func_name == 'exp':
                return 'positive'  # e^x always positive
            elif func_name == 'Abs':
                arg_sign = self.analyze_sign(expr.args[0])
                return 'positive' if arg_sign != 'zero' else 'zero'
            elif func_name == 'sqrt':
                arg = expr.args[0]
                # Special case: sqrt(x^2) = |x|
                if isinstance(arg, Pow) and arg.args[1] == 2:
                    return 'positive'  # |x| ≥ 0, positive unless x=0
                arg_sign = self.analyze_sign(arg)
                return 'positive' if arg_sign == 'positive' else 'indeterminate'
        
        return 'indeterminate'
    
    # Monkey patch the method
    import types
    from sympy import Symbol, Function, Number, Pow, pi, E
    analyzer._analyze_atomic = types.MethodType(modified_analyze_atomic, analyzer)
    
    # Run tests
    all_passed = True
    for expr_str, expected in test_cases:
        expr = sympify(expr_str)
        result = analyzer.analyze_sign(expr)
        status = "✓" if result == expected else "✗"
        print(f"{expr_str:20} -> {result:12} (expected: {expected:12}) {status}")
        if result != expected:
            all_passed = False
    
    print("=" * 70)
    print(f"All tests passed: {all_passed}")
    return all_passed

if __name__ == "__main__":
    test_positive_default_assumption()
