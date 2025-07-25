"""
Core inequality system representation and validation.
"""
from typing import List, Tuple, Union, Optional
from sympy import symbols, Symbol, sympify, simplify
from sympy.core.expr import Expr

from ..utils.validation import validate_operator, validate_expression
from ..processors.input_processor import InputProcessor


class InequalityTerm:
    """Represents a single inequality term with validation."""
    
    def __init__(self, lhs: Union[str, Expr], operator: str, rhs: Union[str, Expr, int, float] = 0):
        """
        Initialize an inequality term.
        
        Args:
            lhs: Left-hand side expression
            operator: Inequality operator (<=, <, >=, >, ==, !=)
            rhs: Right-hand side expression (default: 0)
        """
        self.lhs = self._ensure_expr(lhs)
        self.rhs = self._ensure_expr(rhs)
        self.operator = validate_operator(operator)
        
        # Computed properties
        self._expression = None
        self._variables = None
        
    def _ensure_expr(self, value: Union[str, Expr, int, float]) -> Expr:
        """Convert value to SymPy expression."""
        if isinstance(value, (int, float)):
            return sympify(value)
        elif isinstance(value, str):
            return sympify(value)
        elif hasattr(value, 'free_symbols'):  # SymPy expression
            return value
        else:
            raise TypeError(f"Cannot convert {type(value)} to SymPy expression")
    
    @property
    def expression(self) -> Expr:
        """Get the normalized expression (lhs - rhs)."""
        if self._expression is None:
            self._expression = simplify(self.lhs - self.rhs)
        return self._expression
    
    @property
    def variables(self) -> set:
        """Get all variables in the inequality."""
        if self._variables is None:
            self._variables = self.expression.free_symbols
        return self._variables
    
    def contains_variable(self, var: Symbol) -> bool:
        """Check if inequality contains the given variable."""
        return var in self.variables
    
    def __str__(self) -> str:
        return f"{self.lhs} {self.operator} {self.rhs}"
    
    def __repr__(self) -> str:
        return f"InequalityTerm({self.lhs}, '{self.operator}', {self.rhs})"


class InequalitySystem:
    """Represents a system of rational inequalities with validation and preprocessing."""
    
    def __init__(self, inequalities: List[Union[Tuple, str]], variable: Union[str, Symbol] = 'x'):
        """
        Initialize inequality system.
        
        Args:
            inequalities: List of inequalities in various formats
            variable: Primary variable to solve for
        """
        self.primary_variable = symbols(variable) if isinstance(variable, str) else variable
        self.terms: List[InequalityTerm] = []
        self.constraints: List[InequalityTerm] = []  # Terms not involving primary variable
        
        # Process input inequalities
        processor = InputProcessor()
        processed = processor.process_inequalities(inequalities)
        
        # Convert to InequalityTerm objects and classify
        for lhs, op, rhs in processed:
            term = InequalityTerm(lhs, op, rhs)
            
            if term.contains_variable(self.primary_variable):
                self.terms.append(term)
            else:
                self.constraints.append(term)
    
    @property
    def variable_terms(self) -> List[InequalityTerm]:
        """Get terms that involve the primary variable."""
        return self.terms
    
    @property
    def constraint_terms(self) -> List[InequalityTerm]:
        """Get constraint terms that don't involve the primary variable."""
        return self.constraints
    
    @property
    def all_variables(self) -> set:
        """Get all variables in the system."""
        variables = set()
        for term in self.terms + self.constraints:
            variables.update(term.variables)
        return variables
    
    @property
    def parameters(self) -> set:
        """Get all parameters (variables other than primary variable)."""
        return self.all_variables - {self.primary_variable}
    
    def validate(self) -> bool:
        """
        Validate the inequality system.
        
        Returns:
            True if system is valid
            
        Raises:
            ValueError: If system is invalid
        """
        if not self.terms:
            raise ValueError("No inequalities involve the primary variable")
        
        # Check for undefined expressions
        for term in self.terms + self.constraints:
            try:
                # Try to evaluate with dummy values to catch undefined expressions
                test_subs = {var: 1 for var in term.variables}
                term.expression.subs(test_subs)
            except Exception as e:
                raise ValueError(f"Invalid expression in term {term}: {e}")
        
        return True
    
    def get_rational_terms(self) -> List[InequalityTerm]:
        """Get terms with rational expressions (containing fractions)."""
        rational_terms = []
        for term in self.terms:
            numer, denom = term.expression.as_numer_denom()
            if denom != 1:  # Has denominator other than 1
                rational_terms.append(term)
        return rational_terms
    
    def get_polynomial_terms(self) -> List[InequalityTerm]:
        """Get terms with polynomial expressions only."""
        polynomial_terms = []
        for term in self.terms:
            numer, denom = term.expression.as_numer_denom()
            if denom == 1:  # No denominator
                polynomial_terms.append(term)
        return polynomial_terms
    
    def __len__(self) -> int:
        return len(self.terms) + len(self.constraints)
    
    def __str__(self) -> str:
        parts = []
        if self.terms:
            parts.append(f"Variable terms: {[str(t) for t in self.terms]}")
        if self.constraints:
            parts.append(f"Constraints: {[str(t) for t in self.constraints]}")
        return f"InequalitySystem({', '.join(parts)})"
