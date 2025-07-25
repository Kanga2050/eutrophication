"""
Sign analysis module for determining the sign of mathematical expressions.
This module uses a recursive binary decomposition approach similar to merge sort.
"""
from sympy import (
    symbols, sympify, simplify, expand, factor, 
    Abs, sqrt, log, exp, sin, cos, tan, 
    I, pi, E, oo, zoo, nan,
    Add, Mul, Pow, Integer, Rational, Float,
    Symbol, Function, Expr
)
from sympy.core.numbers import Number
import re


class SignCombiner:
    """
    Handles the combination rules for binary operations on signs.
    This is like the 'merge' step in merge sort.
    """
    
    @staticmethod
    def combine_addition(sign1, sign2):
        """Combine two signs with addition operation."""
        combinations = {
            ('positive', 'positive'): 'positive',
            ('negative', 'negative'): 'negative',
            ('positive', 'zero'): 'positive',
            ('negative', 'zero'): 'negative',
            ('zero', 'positive'): 'positive',
            ('zero', 'negative'): 'negative',
            ('zero', 'zero'): 'zero',
            # Mixed signs are indeterminate
            ('positive', 'negative'): 'indeterminate',
            ('negative', 'positive'): 'indeterminate',
        }
        return combinations.get((sign1, sign2), 'indeterminate')
    
    @staticmethod
    def combine_multiplication(sign1, sign2):
        """Combine two signs with multiplication operation."""
        combinations = {
            ('positive', 'positive'): 'positive',
            ('negative', 'negative'): 'positive',
            ('positive', 'negative'): 'negative',
            ('negative', 'positive'): 'negative',
            ('positive', 'zero'): 'zero',
            ('negative', 'zero'): 'zero',
            ('zero', 'positive'): 'zero',
            ('zero', 'negative'): 'zero',
            ('zero', 'zero'): 'zero',
        }
        return combinations.get((sign1, sign2), 'indeterminate')
    
    @staticmethod
    def combine_power(base_sign, exp_sign, exponent_value=None):
        """Combine base and exponent signs for power operation."""
        # Handle zero base
        if base_sign == 'zero':
            if exp_sign == 'positive':
                return 'zero'
            elif exp_sign == 'zero':
                return 'indeterminate'  # 0^0
            else:
                return 'indeterminate'
        
        # Positive base always gives positive result
        if base_sign == 'positive':
            return 'positive'
        
        # Negative base depends on exponent
        if base_sign == 'negative':
            if exponent_value is not None:
                if isinstance(exponent_value, Number):
                    if exponent_value > 0 and exponent_value % 2 == 0:
                        return 'positive'  # (-a)^(even) = positive
                    elif exponent_value > 0 and exponent_value % 2 == 1:
                        return 'negative'  # (-a)^(odd) = negative
            return 'indeterminate'
        
        return 'indeterminate'


class SignAnalyzer:
    """
    Recursive sign analyzer using binary decomposition approach.
    """
    
    def __init__(self):
        """Initialize the sign analyzer with default assumptions."""
        self.assumptions = {}
        self.combiner = SignCombiner()
    
    def add_assumption(self, symbol, sign):
        """Add an assumption about a symbol's sign."""
        if isinstance(symbol, str):
            symbol = sympify(symbol)
        self.assumptions[symbol] = sign
    
    def analyze_sign(self, expr):
        """
        Recursively analyze the sign of an expression using binary decomposition.
        This is the main entry point - like the top-level mergesort call.
        """
        if isinstance(expr, str):
            expr = sympify(expr)
        
        expr = simplify(expr)
        
        # Base cases (like the base case in merge sort)
        if self._is_atomic(expr):
            return self._analyze_atomic(expr)
        
        # Recursive decomposition (like the divide step in merge sort)
        return self._decompose_and_analyze(expr)
    
    def _is_atomic(self, expr):
        """Check if expression is atomic (base case for recursion)."""
        return (isinstance(expr, Number) or 
                isinstance(expr, Symbol) or
                (isinstance(expr, Function) and self._is_simple_function(expr)))
    
    def _is_simple_function(self, expr):
        """Check if function is simple enough to be treated as atomic."""
        func_name = expr.func.__name__
        return func_name in ['Abs', 'exp', 'sqrt'] and len(expr.args) == 1
    
    def _analyze_atomic(self, expr):
        """Analyze atomic expressions (base case)."""
        # Numbers
        if isinstance(expr, Number):
            if expr > 0:
                return 'positive'
            elif expr < 0:
                return 'negative'
            else:
                return 'zero'
        
        # Symbols
        if isinstance(expr, Symbol):
            if expr in self.assumptions:
                return self.assumptions[expr]
            # Special constants
            if expr == pi or expr == E:
                return 'positive'
            # DEFAULT: assume all symbols are positive unless explicitly stated otherwise
            # This aligns with typical mathematical analysis where variables represent positive quantities
            return 'positive'
        
        # Simple functions
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
    
    def _decompose_and_analyze(self, expr):
        """
        Decompose expression into binary operations and recursively analyze.
        This is like the divide-and-conquer step in merge sort.
        """
        # Handle addition (sum of terms)
        if isinstance(expr, Add):
            return self._analyze_addition(expr)
        
        # Handle multiplication (product of factors)
        elif isinstance(expr, Mul):
            return self._analyze_multiplication(expr)
        
        # Handle powers
        elif isinstance(expr, Pow):
            return self._analyze_power(expr)
        
        # Handle complex functions
        elif isinstance(expr, Function):
            return self._analyze_complex_function(expr)
        
        return 'indeterminate'
    
    def _analyze_addition(self, expr):
        """
        Analyze addition by recursively combining pairs of terms.
        Like merge sort: divide terms into pairs, analyze each, then combine.
        """
        terms = list(expr.args)
        
        # Base case: single term
        if len(terms) == 1:
            return self.analyze_sign(terms[0])
        
        # Special optimization: check for guaranteed positive sums
        if self._is_guaranteed_positive_sum(terms):
            return 'positive'
        
        # Recursive binary combination
        return self._binary_combine_terms(terms, self.combiner.combine_addition)
    
    def _analyze_multiplication(self, expr):
        """
        Analyze multiplication by recursively combining pairs of factors.
        """
        factors = list(expr.args)
        
        # Base case: single factor
        if len(factors) == 1:
            return self.analyze_sign(factors[0])
        
        # Recursive binary combination
        return self._binary_combine_terms(factors, self.combiner.combine_multiplication)
    
    def _analyze_power(self, expr):
        """Analyze power expressions."""
        base, exponent = expr.args
        
        # Special case: even powers are always non-negative
        if isinstance(exponent, Number) and exponent > 0 and exponent % 2 == 0:
            base_sign = self.analyze_sign(base)
            return 'positive' if base_sign != 'zero' else 'zero'
        
        # Special case: x^2 pattern
        if exponent == 2:
            base_sign = self.analyze_sign(base)
            return 'positive' if base_sign != 'zero' else 'zero'
        
        # General case
        base_sign = self.analyze_sign(base)
        exp_sign = self.analyze_sign(exponent)
        return self.combiner.combine_power(base_sign, exp_sign, exponent)
    
    def _analyze_complex_function(self, expr):
        """Analyze complex functions that aren't atomic."""
        func_name = expr.func.__name__
        
        if func_name in ['sin', 'cos', 'tan', 'log']:
            return 'indeterminate'
        
        return 'indeterminate'
    
    def _binary_combine_terms(self, terms, combine_func):
        """
        Recursively combine terms/factors using binary operations.
        This is the core recursive algorithm similar to merge sort.
        """
        # Base case: empty list
        if not terms:
            return 'zero'
        
        # Base case: single term
        if len(terms) == 1:
            return self.analyze_sign(terms[0])
        
        # Base case: two terms - direct combination
        if len(terms) == 2:
            sign1 = self.analyze_sign(terms[0])
            sign2 = self.analyze_sign(terms[1])
            return combine_func(sign1, sign2)
        
        # Recursive case: divide and conquer
        mid = len(terms) // 2
        left_terms = terms[:mid]
        right_terms = terms[mid:]
        
        # Recursively analyze each half
        left_sign = self._binary_combine_terms(left_terms, combine_func)
        right_sign = self._binary_combine_terms(right_terms, combine_func)
        
        # Combine the results
        return combine_func(left_sign, right_sign)
    
    def _is_guaranteed_positive_sum(self, terms):
        """
        Check if a sum is guaranteed to be positive.
        Optimization for common patterns like x^2 + 1, a^2 + b^2, etc.
        """
        has_positive_constant = False
        all_non_negative = True
        
        for term in terms:
            term_sign = self.analyze_sign(term)
            
            if term_sign == 'positive':
                has_positive_constant = True
            elif term_sign == 'zero':
                continue  # Zero terms don't affect positivity
            elif self._is_guaranteed_non_negative_term(term):
                continue  # Non-negative terms are okay
            else:
                all_non_negative = False
                break
        
        return all_non_negative and has_positive_constant
    
    def _is_guaranteed_non_negative_term(self, term):
        """Check if a single term is guaranteed to be non-negative."""
        # Squares: x^2, (anything)^2
        if isinstance(term, Pow) and term.args[1] == 2:
            return True
        
        # Even powers: x^4, x^6, etc.
        if isinstance(term, Pow) and isinstance(term.args[1], Number):
            exp = term.args[1]
            if exp > 0 and exp % 2 == 0:
                return True
        
        # Absolute values
        if isinstance(term, Function) and term.func.__name__ == 'Abs':
            return True
        
        # Products with guaranteed non-negative factors
        if isinstance(term, Mul):
            factors = term.args
            return all(self._is_guaranteed_non_negative_factor(f) for f in factors)
        
        return False
    
    def _is_guaranteed_non_negative_factor(self, factor):
        """Check if a factor in a product is guaranteed to be non-negative."""
        # Positive constants/assumptions
        if factor in self.assumptions and self.assumptions[factor] == 'positive':
            return True
        
        # Positive numbers
        if isinstance(factor, Number) and factor > 0:
            return True
        
        # Squares and even powers
        if isinstance(factor, Pow):
            exp = factor.args[1]
            if isinstance(exp, Number) and exp > 0 and exp % 2 == 0:
                return True
            if exp == 2:
                return True
        
        # Absolute values
        if isinstance(factor, Function) and factor.func.__name__ == 'Abs':
            return True
        
        return False
    
    # Convenience methods
    def is_always_positive(self, expr):
        """Check if expression is always positive."""
        return self.analyze_sign(expr) == 'positive'
    
    def is_always_negative(self, expr):
        """Check if expression is always negative."""
        return self.analyze_sign(expr) == 'negative'
    
    def is_always_zero(self, expr):
        """Check if expression is always zero."""
        return self.analyze_sign(expr) == 'zero'
    
    def is_never_zero(self, expr):
        """Check if expression is never zero."""
        sign = self.analyze_sign(expr)
        return sign in ['positive', 'negative', 'nonzero']
    
    def can_determine_sign(self, expr):
        """Check if the sign can be determined."""
        sign = self.analyze_sign(expr)
        return sign != 'indeterminate'


def create_default_analyzer():
    """Create a sign analyzer with default mathematical assumptions."""
    analyzer = SignAnalyzer()
    
    # No need to explicitly add positive assumptions for common symbols
    # since the analyzer now assumes all symbols are positive by default
    # unless explicitly overridden with add_assumption()
    
    return analyzer


def analyze_rational_inequality_signs(numerator, denominator, analyzer=None):
    """
    Analyze signs for a rational inequality of the form numerator/denominator.
    
    Args:
        numerator: SymPy expression for numerator
        denominator: SymPy expression for denominator
        analyzer: SignAnalyzer instance (optional)
        
    Returns:
        Dictionary with sign analysis results
    """
    if analyzer is None:
        analyzer = create_default_analyzer()
    
    num_sign = analyzer.analyze_sign(numerator)
    den_sign = analyzer.analyze_sign(denominator)
    
    # Determine if we can simplify cases
    simplified_cases = []
    
    if num_sign == 'positive' and den_sign == 'positive':
        simplified_cases.append('expression_always_positive')
    elif num_sign == 'negative' and den_sign == 'positive':
        simplified_cases.append('expression_always_negative')
    elif num_sign == 'positive' and den_sign == 'negative':
        simplified_cases.append('expression_always_negative')
    elif num_sign == 'negative' and den_sign == 'negative':
        simplified_cases.append('expression_always_positive')
    elif num_sign == 'zero':
        simplified_cases.append('expression_always_zero')
    elif den_sign == 'zero':
        simplified_cases.append('expression_undefined')
    
    return {
        'numerator_sign': num_sign,
        'denominator_sign': den_sign,
        'simplified_cases': simplified_cases,
        'can_reduce_cases': len(simplified_cases) > 0
    }


def apply_sign_analysis_to_solver_output(solver_output, analyzer=None):
    """
    Apply sign analysis to solver output to reduce unnecessary cases.
    
    Args:
        solver_output: List of case strings from the solver
        analyzer: SignAnalyzer instance (optional)
        
    Returns:
        Filtered list of cases with redundant cases removed
    """
    if analyzer is None:
        analyzer = create_default_analyzer()
    
    filtered_cases = []
    
    for case in solver_output:
        # Extract expressions from case description
        if "because" in case and ">= 0" in case:
            # Try to extract the expression
            match = re.search(r'because (.+?) [<>=]+ 0', case)
            if match:
                expr_str = match.group(1).strip()
                try:
                    expr = sympify(expr_str)
                    sign = analyzer.analyze_sign(expr)
                    
                    # Skip cases that are always false
                    if ">= 0" in case and sign == 'negative':
                        continue
                    elif "<= 0" in case and sign == 'positive':
                        continue
                    elif "> 0" in case and sign in ['negative', 'zero']:
                        continue
                    elif "< 0" in case and sign in ['positive', 'zero']:
                        continue
                        
                except:
                    pass  # If we can't parse, keep the case
        
        filtered_cases.append(case)
    
    return filtered_cases


def get_sign_based_assumptions(expressions, analyzer=None):
    """
    Generate assumptions based on sign analysis of expressions.
    
    Args:
        expressions: List of SymPy expressions
        analyzer: SignAnalyzer instance (optional)
        
    Returns:
        Dictionary of assumptions
    """
    if analyzer is None:
        analyzer = create_default_analyzer()
    
    assumptions = {}
    
    for expr in expressions:
        sign = analyzer.analyze_sign(expr)
        if sign != 'indeterminate':
            assumptions[expr] = sign
    
    return assumptions


# Example usage and testing functions
def demo_sign_analysis():
    """Demonstrate the recursive binary decomposition sign analysis."""
    analyzer = create_default_analyzer()
    
    test_expressions = [
        # Simple cases
        "x**2",
        "x**2 + 1", 
        "x**2 - 1",
        "abs(x)",
        "exp(x)",
        
        # Binary operations - addition
        "a + b",  # positive + positive
        "x**2 + y**2",  # non-negative + non-negative
        "x**2 + 3",  # non-negative + positive
        
        # Binary operations - multiplication  
        "a*b",  # positive * positive
        "a*x**2",  # positive * non-negative
        "(-2)*x**2",  # negative * non-negative
        
        # Complex recursive cases
        "a*x**2 + b*y**2",  # (positive * non-negative) + (positive * non-negative)
        "(x + y)**2",  # (indeterminate)^2
        "a**2 + b**2 + c**2",  # non-negative + non-negative + non-negative
        
        # Nested operations
        "(x**2 + 1) * (y**2 + 2)",  # positive * positive
        "(a + b) * (c + d)",  # positive * positive
        
        # Functions
        "sqrt(x**2 + 1)",
        "abs(x - 1)",
        "exp(x**2)",
    ]
    
    print("Recursive Binary Decomposition Sign Analysis Demo")
    print("=" * 60)
    print("Each expression is recursively broken down into binary operations")
    print("then combined using sign combination rules.\n")
    
    for expr_str in test_expressions:
        try:
            expr = sympify(expr_str)
            sign = analyzer.analyze_sign(expr)
            print(f"{expr_str:25} -> {sign}")
        except Exception as e:
            print(f"{expr_str:25} -> Error: {e}")
    
    print("\n" + "=" * 60)
    print("Testing binary combination rules directly...")
    
    # Test the binary combination rules
    combiner = SignCombiner()
    
    print("\nAddition rules:")
    addition_tests = [
        ('positive', 'positive'), ('negative', 'negative'),
        ('positive', 'zero'), ('negative', 'zero'),
        ('positive', 'negative'), ('zero', 'zero')
    ]
    
    for sign1, sign2 in addition_tests:
        result = combiner.combine_addition(sign1, sign2)
        print(f"  {sign1} + {sign2} = {result}")
    
    print("\nMultiplication rules:")
    mult_tests = [
        ('positive', 'positive'), ('negative', 'negative'),
        ('positive', 'negative'), ('negative', 'positive'),
        ('positive', 'zero'), ('zero', 'zero')
    ]
    
    for sign1, sign2 in mult_tests:
        result = combiner.combine_multiplication(sign1, sign2)
        print(f"  {sign1} * {sign2} = {result}")


if __name__ == "__main__":
    demo_sign_analysis()
