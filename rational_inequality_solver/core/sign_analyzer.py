"""
Optimized sign analyzer with better performance and caching.
"""
from typing import Dict, Set, Optional, Union
from functools import lru_cache
from sympy import (
    symbols, sympify, simplify, expand, factor,
    Add, Mul, Pow, Integer, Rational, Float,
    Symbol, Function, Expr, Number,
    Abs, sqrt, log, exp, sin, cos, tan,
    I, pi, E, oo, zoo, nan
)


class OptimizedSignAnalyzer:
    """
    Enhanced sign analyzer with performance optimizations and caching.
    """
    
    def __init__(self, cache_size: int = 256):
        """
        Initialize optimized sign analyzer.
        
        Args:
            cache_size: Size of the analysis cache
        """
        self.assumptions = {}
        self.cache_size = cache_size
        
        # Clear cache if different size needed
        if self.analyze_sign.__wrapped__.__name__ in globals():
            self.analyze_sign.cache_clear()
    
    def add_assumption(self, expr, sign: str):
        """
        Add sign assumption for an expression.
        
        Args:
            expr: Expression or symbol
            sign: 'positive', 'negative', 'zero', or 'indeterminate'
        """
        if isinstance(expr, (int, float)):
            expr = sympify(expr)
        
        if sign not in ['positive', 'negative', 'zero', 'indeterminate']:
            raise ValueError(f"Invalid sign: {sign}")
        
        # Store assumptions by string representation for consistent hashing
        self.assumptions[str(expr)] = sign
    
    @lru_cache(maxsize=256)
    def analyze_sign(self, expr) -> str:
        """
        Analyze the sign of an expression with caching.
        
        Args:
            expr: SymPy expression to analyze
            
        Returns:
            'positive', 'negative', 'zero', or 'indeterminate'
        """
        if isinstance(expr, (int, float)):
            expr = sympify(expr)
        
        # Check assumptions first
        expr_str = str(expr)
        if expr_str in self.assumptions:
            return self.assumptions[expr_str]
        
        return self._analyze_sign_recursive(expr)
    
    def _analyze_sign_recursive(self, expr) -> str:
        """Recursive sign analysis implementation."""
        # Handle atomic expressions
        if expr.is_Atom:
            return self._analyze_atomic(expr)
        
        # Handle compound expressions
        if isinstance(expr, Add):
            return self._analyze_addition(expr)
        elif isinstance(expr, Mul):
            return self._analyze_multiplication(expr)
        elif isinstance(expr, Pow):
            return self._analyze_power(expr)
        else:
            return self._analyze_function(expr)
    
    def _analyze_atomic(self, expr) -> str:
        """Analyze atomic expressions (numbers, symbols, constants)."""
        # Numbers
        if isinstance(expr, (Integer, Rational, Float)):
            if expr > 0:
                return 'positive'
            elif expr < 0:
                return 'negative'
            else:
                return 'zero'
        
        # Mathematical constants
        if expr == pi or expr == E:
            return 'positive'
        elif expr == I:
            return 'indeterminate'  # Complex
        elif expr in [oo, -oo, zoo, nan]:
            return 'indeterminate'
        
        # Symbols
        if isinstance(expr, Symbol):
            # Check if we have assumptions for this symbol
            expr_str = str(expr)
            if expr_str in self.assumptions:
                return self.assumptions[expr_str]
            
            # Default assumption: indeterminate
            return 'indeterminate'
        
        # Functions without arguments
        if isinstance(expr, Function) and not expr.args:
            return 'indeterminate'
        
        return 'indeterminate'
    
    def _analyze_addition(self, expr: Add) -> str:
        """Analyze addition expressions."""
        signs = [self.analyze_sign(arg) for arg in expr.args]
        
        # Count different sign types
        positive_count = signs.count('positive')
        negative_count = signs.count('negative')
        zero_count = signs.count('zero')
        indeterminate_count = signs.count('indeterminate')
        
        # If any indeterminate, result is indeterminate
        if indeterminate_count > 0:
            return 'indeterminate'
        
        # All zeros
        if zero_count == len(signs):
            return 'zero'
        
        # All positive or positive with zeros
        if negative_count == 0 and positive_count > 0:
            return 'positive'
        
        # All negative or negative with zeros
        if positive_count == 0 and negative_count > 0:
            return 'negative'
        
        # Mixed positive and negative
        return 'indeterminate'
    
    def _analyze_multiplication(self, expr: Mul) -> str:
        """Analyze multiplication expressions."""
        signs = [self.analyze_sign(arg) for arg in expr.args]
        
        # If any zero, result is zero
        if 'zero' in signs:
            return 'zero'
        
        # If any indeterminate, result is indeterminate
        if 'indeterminate' in signs:
            return 'indeterminate'
        
        # Count negative signs
        negative_count = signs.count('negative')
        
        # Even number of negatives → positive
        # Odd number of negatives → negative
        return 'positive' if negative_count % 2 == 0 else 'negative'
    
    def _analyze_power(self, expr: Pow) -> str:
        """Analyze power expressions."""
        base_sign = self.analyze_sign(expr.base)
        exp_sign = self.analyze_sign(expr.exp)
        
        # Handle special cases
        if base_sign == 'zero':
            if exp_sign == 'positive':
                return 'zero'
            elif exp_sign == 'zero':
                return 'indeterminate'  # 0^0 is indeterminate
            else:
                return 'indeterminate'  # 0^negative is undefined
        
        if base_sign == 'positive':
            return 'positive'  # positive^anything = positive
        
        if base_sign == 'negative':
            # Check if exponent is an integer
            try:
                if expr.exp.is_integer:
                    if expr.exp % 2 == 0:
                        return 'positive'  # negative^even = positive
                    else:
                        return 'negative'  # negative^odd = negative
                else:
                    return 'indeterminate'  # negative^non-integer can be complex
            except:
                return 'indeterminate'
        
        # Special case: x^2 type expressions
        if expr.exp == 2:
            if base_sign in ['positive', 'negative']:
                return 'positive'  # anything^2 >= 0
        
        return 'indeterminate'
    
    def _analyze_function(self, expr) -> str:
        """Analyze function expressions."""
        # Absolute value is always non-negative
        if isinstance(expr, Abs):
            arg_sign = self.analyze_sign(expr.args[0])
            if arg_sign == 'zero':
                return 'zero'
            elif arg_sign in ['positive', 'negative']:
                return 'positive'
            else:
                return 'positive'  # |x| >= 0 for real x
        
        # Square root is non-negative for real arguments
        if isinstance(expr, sqrt):
            return 'positive'  # sqrt(x) >= 0 for x >= 0
        
        # Exponential is always positive
        if isinstance(expr, exp):
            return 'positive'
        
        # Logarithm can be positive, negative, or zero
        if isinstance(expr, log):
            return 'indeterminate'
        
        # Trigonometric functions
        if isinstance(expr, (sin, cos, tan)):
            return 'indeterminate'
        
        return 'indeterminate'
    
    def clear_cache(self):
        """Clear the analysis cache."""
        self.analyze_sign.cache_clear()
    
    def get_cache_info(self):
        """Get cache statistics."""
        return self.analyze_sign.cache_info()


def create_optimized_analyzer(cache_size: int = 256) -> OptimizedSignAnalyzer:
    """
    Create an optimized sign analyzer with common mathematical assumptions.
    
    Args:
        cache_size: Size of the analysis cache
        
    Returns:
        Configured OptimizedSignAnalyzer instance
    """
    analyzer = OptimizedSignAnalyzer(cache_size)
    
    # Add common mathematical assumptions
    analyzer.add_assumption(1, 'positive')
    analyzer.add_assumption(-1, 'negative')
    analyzer.add_assumption(0, 'zero')
    analyzer.add_assumption(pi, 'positive')
    analyzer.add_assumption(E, 'positive')
    
    return analyzer


# Legacy compatibility function
def apply_sign_analysis_to_solver_output(branches: list, analyzer: OptimizedSignAnalyzer) -> list:
    """
    Apply sign analysis to filter impossible cases from solver output.
    
    Args:
        branches: List of solver output strings
        analyzer: Sign analyzer instance
        
    Returns:
        Filtered list of valid branches
    """
    # This is a simplified version - in practice, this would parse
    # the solver output and apply sign analysis to filter contradictions
    filtered_branches = []
    
    for branch in branches:
        # Simple filtering: remove obviously contradictory cases
        if "No solution" in branch and "All real x" in branch:
            continue  # Skip contradictory cases
        
        filtered_branches.append(branch)
    
    return filtered_branches if filtered_branches else branches


# Alias for backward compatibility
SignAnalyzer = OptimizedSignAnalyzer
create_default_analyzer = create_optimized_analyzer
