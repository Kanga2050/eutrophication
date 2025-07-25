"""
Optimized input processor with better error handling and performance.
"""
import re
from typing import List, Tuple, Union, Any
from sympy import sympify

from ..utils.validation import validate_operator, validate_expression, ValidationError


class InputProcessor:
    """Enhanced input processor with robust parsing and validation."""
    
    def __init__(self, strict_validation: bool = True):
        """
        Initialize input processor.
        
        Args:
            strict_validation: Whether to use strict validation
        """
        self.strict_validation = strict_validation
        self._operator_patterns = self._compile_operator_patterns()
    
    def _compile_operator_patterns(self) -> dict:
        """Compile regex patterns for operators for better performance."""
        # Order matters - longer operators first to avoid partial matches
        operators = ['<=', '>=', '==', '!=', '<', '>']
        patterns = {}
        
        for op in operators:
            # Escape special regex characters
            escaped_op = re.escape(op)
            patterns[op] = re.compile(rf'\s*{escaped_op}\s*')
        
        return patterns
    
    def process_inequalities(self, inequalities: List[Union[Tuple, str]]) -> List[Tuple]:
        """
        Process inequalities into standardized format with optimized parsing.
        
        Args:
            inequalities: List of inequalities in various formats
            
        Returns:
            List of (lhs, operator, rhs) tuples
            
        Raises:
            ValidationError: If processing fails
        """
        processed = []
        
        for i, item in enumerate(inequalities):
            try:
                result = self._process_single_inequality(item)
                processed.append(result)
            except Exception as e:
                error_msg = f"Error processing inequality {i+1} '{item}': {str(e)}"
                if self.strict_validation:
                    raise ValidationError(error_msg)
                else:
                    print(f"Warning: {error_msg}")
                    continue
        
        if not processed:
            raise ValidationError("No valid inequalities could be processed")
        
        return processed
    
    def _process_single_inequality(self, item: Union[Tuple, str]) -> Tuple:
        """
        Process a single inequality item.
        
        Args:
            item: Single inequality in any supported format
            
        Returns:
            (lhs, operator, rhs) tuple
        """
        if isinstance(item, tuple):
            return self._process_tuple_format(item)
        elif isinstance(item, str):
            return self._process_string_format(item)
        else:
            raise ValidationError(f"Unsupported inequality format: {type(item)}")
    
    def _process_tuple_format(self, item: Tuple) -> Tuple:
        """Process tuple format inequalities."""
        if len(item) == 2:
            # (expression, operator) format - assume RHS = 0
            expr, op = item
            if isinstance(expr, str):
                # Handle "lhs op rhs" string with separate operator
                lhs, rhs = self._parse_string_with_operator(expr, op)
            else:
                lhs, rhs = expr, 0
            return self._validate_and_convert(lhs, op, rhs)
            
        elif len(item) == 3:
            # (lhs, operator, rhs) format
            lhs, op, rhs = item
            return self._validate_and_convert(lhs, op, rhs)
        else:
            raise ValidationError(f"Tuple must have 2 or 3 elements, got {len(item)}")
    
    def _process_string_format(self, item: str) -> Tuple:
        """Process string format inequalities with optimized parsing."""
        # Find operator using pre-compiled patterns
        found_operators = []
        
        for op, pattern in self._operator_patterns.items():
            match = pattern.search(item)
            if match:
                found_operators.append((op, match.start(), match.end()))
        
        if not found_operators:
            raise ValidationError(f"No operator found in string: '{item}'")
        
        # Use the longest operator found (handles <= vs < correctly)
        found_operators.sort(key=lambda x: x[2] - x[1], reverse=True)
        op, start, end = found_operators[0]
        
        # Split string at operator
        lhs = item[:start].strip()
        rhs = item[end:].strip()
        
        if not lhs or not rhs:
            raise ValidationError(f"Incomplete inequality: '{item}'")
        
        return self._validate_and_convert(lhs, op, rhs)
    
    def _parse_string_with_operator(self, expr_str: str, expected_op: str) -> Tuple[str, str]:
        """Parse string expression with expected operator."""
        # Look for the expected operator in the string
        pattern = self._operator_patterns.get(expected_op)
        if not pattern:
            raise ValidationError(f"Unknown operator: {expected_op}")
        
        match = pattern.search(expr_str)
        if not match:
            raise ValidationError(f"Operator '{expected_op}' not found in: '{expr_str}'")
        
        lhs = expr_str[:match.start()].strip()
        rhs = expr_str[match.end():].strip()
        
        return lhs, rhs
    
    def _validate_and_convert(self, lhs: Any, op: str, rhs: Any) -> Tuple:
        """Validate and convert components to proper types."""
        # Validate operator
        validated_op = validate_operator(op)
        
        # Convert to SymPy expressions
        try:
            lhs_expr = validate_expression(lhs)
            rhs_expr = validate_expression(rhs)
        except Exception as e:
            raise ValidationError(f"Expression validation failed: {e}")
        
        return (lhs_expr, validated_op, rhs_expr)
    
    def validate_processed_inequalities(self, processed_ineqs: List[Tuple]) -> bool:
        """
        Validate processed inequalities.
        
        Args:
            processed_ineqs: List of (lhs, op, rhs) tuples
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If validation fails
        """
        if not processed_ineqs:
            raise ValidationError("No inequalities to validate")
        
        for i, (lhs, op, rhs) in enumerate(processed_ineqs):
            # Check operator
            if op not in ['<=', '>=', '<', '>', '==', '!=']:
                raise ValidationError(f"Invalid operator '{op}' in inequality {i+1}")
            
            # Check expressions
            if not hasattr(lhs, 'free_symbols'):
                raise ValidationError(f"LHS is not a SymPy expression in inequality {i+1}")
            
            if not hasattr(rhs, 'free_symbols'):
                raise ValidationError(f"RHS is not a SymPy expression in inequality {i+1}")
        
        return True
