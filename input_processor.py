"""
Input Processing Module for Rational Inequality Solver

This module handles the processing and validation of inequality inputs in various formats,
converting them into a standardized internal representation that the solver can work with.
It provides flexible input parsing while ensuring mathematical correctness and consistency.

Key Features:
- **Multiple Input Formats**: Support for tuples, strings, and mixed formats
- **Automatic Conversion**: Convert strings to SymPy expressions with validation
- **Operator Validation**: Ensure inequality operators are mathematically valid
- **Error Handling**: Comprehensive error reporting for malformed inputs
- **Standardization**: Convert all inputs to consistent (lhs, op, rhs) format

Supported Input Formats:
1. **(expression, operator)** tuples: (x**2 - 1, ">=")
2. **(lhs, operator, rhs)** tuples: (x**2, ">=", 1)
3. **Full string format**: "x**2 - 1 >= 0"
4. **Mixed formats**: Combinations of the above in a single list

Functions:
- process_inequalities(): Main processing function for inequality lists
- validate_processed_inequalities(): Validation function for processed results
- _parse_string_inequality(): String parsing helper function
- _parse_full_string_inequality(): Complete string inequality parser

Processing Steps:
1. **Format Detection**: Identify input format for each inequality
2. **Parsing**: Extract left-hand side, operator, and right-hand side
3. **Conversion**: Convert string expressions to SymPy symbolic expressions
4. **Validation**: Check operator validity and expression structure
5. **Standardization**: Return consistent (lhs, op, rhs) format

Author: Rational Inequality Solver Team
Version: Enhanced Input Validation and Format Support
"""
from sympy import sympify


def process_inequalities(ineqs):
    """
    Process a list of inequalities into standardized (lhs, op, rhs) format.
    
    Args:
        ineqs: List of inequalities in various formats:
               - (expression, operator) tuples
               - (lhs, operator, rhs) tuples  
               - "lhs operator rhs" strings
               
    Returns:
        List of (lhs, op, rhs) tuples where lhs and rhs are SymPy expressions
        
    Raises:
        ValueError: If inequality format is not recognized
    """
    processed_ineqs = []
    
    for item in ineqs:
        try:
            if isinstance(item, tuple) and len(item) == 2:
                expr, op = item
                if isinstance(expr, str):
                    # Handle string format "lhs op rhs"
                    lhs, rhs = _parse_string_inequality(expr, op)
                else:
                    # Handle (expression, operator) format
                    lhs, rhs = expr, 0
                    
            elif isinstance(item, tuple) and len(item) == 3:
                # Handle (lhs, op, rhs) format
                lhs, op, rhs = item
                
            elif isinstance(item, str):
                # Handle pure string format
                lhs, op, rhs = _parse_full_string_inequality(item)
                
            else:
                raise ValueError(f"Unrecognized inequality format: {item}")
                
            # Convert to SymPy expressions
            lhs_expr = sympify(lhs) if not hasattr(lhs, 'free_symbols') else lhs
            rhs_expr = sympify(rhs) if not hasattr(rhs, 'free_symbols') else rhs
            
            processed_ineqs.append((lhs_expr, op.strip(), rhs_expr))
            
        except Exception as e:
            raise ValueError(f"Error processing inequality {item}: {str(e)}")
    
    return processed_ineqs


def _parse_string_inequality(expr_str, expected_op):
    """
    Parse a string inequality of the form "lhs op rhs".
    
    Args:
        expr_str: String containing the inequality
        expected_op: Expected operator (for validation)
        
    Returns:
        Tuple of (lhs, rhs) as strings
    """
    # Find the operator in the string
    operators = ['<=', '>=', '<', '>', '==', '!=']
    found_op = None
    
    for op in operators:
        if op in expr_str:
            if found_op is None or len(op) > len(found_op):
                found_op = op
    
    if found_op is None:
        raise ValueError(f"No operator found in: {expr_str}")
    
    # Split by the operator
    parts = expr_str.split(found_op, 1)
    if len(parts) != 2:
        raise ValueError(f"Could not parse inequality: {expr_str}")
    
    lhs, rhs = parts[0].strip(), parts[1].strip()
    
    # Validate operator matches expected
    if found_op != expected_op.strip():
        print(f"Warning: Found operator '{found_op}' but expected '{expected_op}'")
    
    return lhs, rhs


def _parse_full_string_inequality(ineq_str):
    """
    Parse a complete string inequality to extract lhs, operator, and rhs.
    
    Args:
        ineq_str: Complete inequality string like "x + 1 <= 2*y"
        
    Returns:
        Tuple of (lhs, op, rhs)
    """
    # Find the operator
    operators = ['<=', '>=', '<', '>', '==', '!=']
    found_op = None
    
    for op in operators:
        if op in ineq_str:
            if found_op is None or len(op) > len(found_op):
                found_op = op
    
    if found_op is None:
        raise ValueError(f"No operator found in: {ineq_str}")
    
    # Split by the operator
    parts = ineq_str.split(found_op, 1)
    if len(parts) != 2:
        raise ValueError(f"Could not parse inequality: {ineq_str}")
    
    lhs, rhs = parts[0].strip(), parts[1].strip()
    
    return lhs, found_op, rhs


def validate_processed_inequalities(processed_ineqs):
    """
    Validate that processed inequalities are properly formatted.
    
    Args:
        processed_ineqs: List of (lhs, op, rhs) tuples
        
    Returns:
        bool: True if all inequalities are valid
        
    Raises:
        ValueError: If validation fails
    """
    valid_operators = ['<=', '>=', '<', '>', '==', '!=']
    
    for i, (lhs, op, rhs) in enumerate(processed_ineqs):
        if op not in valid_operators:
            raise ValueError(f"Invalid operator '{op}' in inequality {i+1}")
        
        if not hasattr(lhs, 'free_symbols'):
            raise ValueError(f"LHS is not a SymPy expression in inequality {i+1}")
            
        if not hasattr(rhs, 'free_symbols'):
            raise ValueError(f"RHS is not a SymPy expression in inequality {i+1}")
    
    return True
