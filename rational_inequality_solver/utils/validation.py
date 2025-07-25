"""
Utility functions for validation and error handling.
"""
from typing import Union, Any
from sympy import sympify
from sympy.core.expr import Expr


VALID_OPERATORS = ['<=', '>=', '<', '>', '==', '!=']


def validate_operator(operator: str) -> str:
    """
    Validate inequality operator.
    
    Args:
        operator: String operator to validate
        
    Returns:
        Validated operator string
        
    Raises:
        ValueError: If operator is invalid
    """
    operator = operator.strip()
    if operator not in VALID_OPERATORS:
        raise ValueError(f"Invalid operator '{operator}'. Valid operators: {VALID_OPERATORS}")
    return operator


def validate_expression(expr: Union[str, Expr, int, float]) -> Expr:
    """
    Validate and convert to SymPy expression.
    
    Args:
        expr: Expression to validate
        
    Returns:
        SymPy expression
        
    Raises:
        ValueError: If expression is invalid
    """
    try:
        if isinstance(expr, (int, float)):
            return sympify(expr)
        elif isinstance(expr, str):
            return sympify(expr)
        elif hasattr(expr, 'free_symbols'):  # SymPy expression
            return expr
        else:
            raise TypeError(f"Cannot convert {type(expr)} to SymPy expression")
    except Exception as e:
        raise ValueError(f"Invalid expression '{expr}': {e}")


def safe_simplify(expr: Expr, max_attempts: int = 3) -> Expr:
    """
    Safely simplify expression with fallback.
    
    Args:
        expr: Expression to simplify
        max_attempts: Maximum simplification attempts
        
    Returns:
        Simplified expression or original if simplification fails
    """
    from sympy import simplify, expand, factor
    
    # Try different simplification strategies
    strategies = [simplify, expand, factor]
    
    for i, strategy in enumerate(strategies):
        if i >= max_attempts:
            break
        try:
            result = strategy(expr)
            if result != expr:  # Simplification changed something
                return result
        except Exception:
            continue
    
    return expr  # Return original if all strategies fail


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class ProcessingError(Exception):
    """Custom exception for processing errors."""
    pass


class SolverError(Exception):
    """Custom exception for solver errors.""" 
    pass
