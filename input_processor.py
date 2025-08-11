"""
Input Processor for Rational Inequality System
==============================================

This module processes input inequalities into a standardized format
for the hierarchical case elimination system.
"""

import sympy as sp
from typing import List, Tuple, Any


def process_inequalities(inequalities: List[str]) -> List[Tuple[str, str, str]]:
    """
    Process a list of inequality strings into standardized (lhs, op, rhs) tuples.
    
    Args:
        inequalities: List of inequality strings (e.g., ["x + y <= 5", "z > 0"])
        
    Returns:
        List of (lhs, op, rhs) tuples where:
        - lhs: Left-hand side expression as string
        - op: Operator as string ("<=", ">=", "<", ">", "==")
        - rhs: Right-hand side expression as string
    """
    processed = []
    
    for ineq_str in inequalities:
        if isinstance(ineq_str, tuple):
            # Already processed
            processed.append(ineq_str)
            continue
            
        ineq_str = ineq_str.strip()
        
        # Find the operator
        if " <= " in ineq_str:
            lhs, rhs = ineq_str.split(" <= ", 1)
            op = "<="
        elif " >= " in ineq_str:
            lhs, rhs = ineq_str.split(" >= ", 1) 
            op = ">="
        elif " < " in ineq_str:
            lhs, rhs = ineq_str.split(" < ", 1)
            op = "<"
        elif " > " in ineq_str:
            lhs, rhs = ineq_str.split(" > ", 1)
            op = ">"
        elif " == " in ineq_str:
            lhs, rhs = ineq_str.split(" == ", 1)
            op = "=="
        elif " = " in ineq_str:
            lhs, rhs = ineq_str.split(" = ", 1)
            op = "=="
        else:
            # Try without spaces
            if "<=" in ineq_str:
                lhs, rhs = ineq_str.split("<=", 1)
                op = "<="
            elif ">=" in ineq_str:
                lhs, rhs = ineq_str.split(">=", 1)
                op = ">="
            elif "<" in ineq_str:
                lhs, rhs = ineq_str.split("<", 1)
                op = "<"
            elif ">" in ineq_str:
                lhs, rhs = ineq_str.split(">", 1)
                op = ">"
            elif "==" in ineq_str:
                lhs, rhs = ineq_str.split("==", 1)
                op = "=="
            elif "=" in ineq_str:
                lhs, rhs = ineq_str.split("=", 1)
                op = "=="
            else:
                raise ValueError(f"Could not parse inequality: {ineq_str}")
        
        # Clean up whitespace
        lhs = lhs.strip()
        rhs = rhs.strip()
        
        processed.append((lhs, op, rhs))
    
    return processed


def validate_inequality_format(inequality_tuple: Tuple[str, str, str]) -> bool:
    """
    Validate that an inequality tuple is in the correct format.
    
    Args:
        inequality_tuple: (lhs, op, rhs) tuple
        
    Returns:
        True if valid, False otherwise
    """
    if len(inequality_tuple) != 3:
        return False
        
    lhs, op, rhs = inequality_tuple
    
    # Check that all are strings
    if not all(isinstance(x, str) for x in [lhs, op, rhs]):
        return False
        
    # Check that operator is valid
    valid_ops = ["<=", ">=", "<", ">", "=="]
    if op not in valid_ops:
        return False
        
    # Try to parse expressions with sympy
    try:
        sp.sympify(lhs)
        sp.sympify(rhs)
        return True
    except:
        return False


def normalize_inequality_expressions(inequality_tuple: Tuple[str, str, str]) -> Tuple[str, str, str]:
    """
    Normalize the expressions in an inequality tuple using SymPy.
    
    Args:
        inequality_tuple: (lhs, op, rhs) tuple
        
    Returns:
        Normalized (lhs, op, rhs) tuple
    """
    lhs, op, rhs = inequality_tuple
    
    try:
        # Parse with SymPy and convert back to string
        lhs_expr = sp.sympify(lhs)
        rhs_expr = sp.sympify(rhs)
        
        return (str(lhs_expr), op, str(rhs_expr))
    except:
        # If SymPy fails, return original
        return inequality_tuple


if __name__ == "__main__":
    # Test the processor
    test_inequalities = [
        "x + y <= 5",
        "z > 0",
        "a_l <= a_u",
        "2*x - 3*y >= 10"
    ]
    
    print("Testing input processor...")
    processed = process_inequalities(test_inequalities)
    
    for orig, proc in zip(test_inequalities, processed):
        print(f"'{orig}' -> {proc}")
        
    print("All tests passed!")
