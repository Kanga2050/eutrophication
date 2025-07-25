"""
Enhanced case processor with better performance and organization.
"""
import re
from typing import List, Tuple, Dict, Any, Optional, Callable
from itertools import product
from sympy import simplify, Symbol
from sympy.printing.latex import latex

from ..utils.validation import safe_simplify, ProcessingError
from ..core.inequality_system import InequalitySystem, InequalityTerm


class CaseBound:
    """Represents a single bound from case analysis."""
    
    def __init__(self, expression, direction: str, source_case: str = ""):
        """
        Initialize a case bound.
        
        Args:
            expression: SymPy expression for the bound
            direction: '>' for lower bound, '<' for upper bound
            source_case: Description of the case that generated this bound
        """
        self.expression = expression
        self.direction = direction  # '>' or '<'
        self.source_case = source_case
        
        # Validate direction
        if direction not in ['>', '<']:
            raise ProcessingError(f"Invalid bound direction: {direction}")
    
    def is_lower_bound(self) -> bool:
        """Check if this is a lower bound (x > expression)."""
        return self.direction == '>'
    
    def is_upper_bound(self) -> bool:
        """Check if this is an upper bound (x < expression)."""
        return self.direction == '<'
    
    def __str__(self) -> str:
        return f"x {self.direction} {self.expression}"
    
    def __repr__(self) -> str:
        return f"CaseBound({self.expression}, '{self.direction}')"


class CaseResult:
    """Represents the result of analyzing a single case combination."""
    
    def __init__(self, labels: List[str], bounds: List[CaseBound], constraints: List[str]):
        """
        Initialize case result.
        
        Args:
            labels: List of case labels
            bounds: List of bounds for the variable
            constraints: List of constraint strings
        """
        self.labels = labels
        self.bounds = bounds
        self.constraints = constraints
        
        # Separate bounds by type
        self.lower_bounds = [b for b in bounds if b.is_lower_bound()]
        self.upper_bounds = [b for b in bounds if b.is_upper_bound()]
    
    def get_max_lower_bound(self):
        """Get the maximum lower bound expression."""
        if not self.lower_bounds:
            return None
        
        if len(self.lower_bounds) == 1:
            return self.lower_bounds[0].expression
        
        return f"max({', '.join([str(b.expression) for b in self.lower_bounds])})"
    
    def get_min_upper_bound(self):
        """Get the minimum upper bound expression."""
        if not self.upper_bounds:
            return None
        
        if len(self.upper_bounds) == 1:
            return self.upper_bounds[0].expression
        
        return f"min({', '.join([str(b.expression) for b in self.upper_bounds])})"
    
    def is_valid(self) -> bool:
        """Check if this case result represents a valid solution."""
        # A case is valid if we have at least one bound or constraint
        return len(self.bounds) > 0 or len(self.constraints) > 0


class CaseProcessor:
    """Enhanced case processor with better organization and performance."""
    
    def __init__(self, max_case_combinations: int = 1000):
        """
        Initialize case processor.
        
        Args:
            max_case_combinations: Maximum number of case combinations to process
        """
        self.max_case_combinations = max_case_combinations
        self._bound_pattern = re.compile(r'x\s*([<>]=?)\s*(.+)')
    
    def process_system(self, system: InequalitySystem, solver_func: Callable) -> List[str]:
        """
        Process inequality system and generate LaTeX formatted results.
        
        Args:
            system: InequalitySystem to process
            solver_func: Function to solve individual inequalities
            
        Returns:
            List of LaTeX formatted case results
        """
        # Process constraints (terms not involving primary variable)
        constraint_strs = [str(term) for term in system.constraint_terms]
        
        # Process variable terms
        if not system.variable_terms:
            # No variable terms, just return constraints
            return [self._format_constraint_only_result(constraint_strs)]
        
        # Solve each variable term
        case_results = []
        for term in system.variable_terms:
            case_outputs = solver_func(
                term.expression, 
                system.primary_variable, 
                term.operator
            )
            parsed_cases = self._parse_solver_output(case_outputs)
            if parsed_cases:
                case_results.append(parsed_cases)
        
        if not case_results:
            return [self._format_constraint_only_result(constraint_strs)]
        
        # Generate combinations
        return self._generate_case_combinations(case_results, constraint_strs)
    
    def _parse_solver_output(self, solver_output: List[str]) -> List[Tuple[str, List[CaseBound]]]:
        """
        Parse solver output into structured case data.
        
        Args:
            solver_output: Raw solver output strings
            
        Returns:
            List of (label, bounds) tuples
        """
        cases = []
        
        for output in solver_output:
            if not output.strip():
                continue
            
            lines = output.splitlines()
            label = lines[0].strip() if lines else "Unknown Case"
            bounds = []
            
            # Extract bounds using compiled regex for better performance
            for line in lines[1:]:
                match = self._bound_pattern.search(line.strip())
                if match:
                    op, expr_str = match.groups()
                    try:
                        expr = safe_simplify(sympify(expr_str.strip()))
                        direction = '<' if '<' in op else '>'
                        bound = CaseBound(expr, direction, label)
                        bounds.append(bound)
                    except Exception:
                        # Skip malformed expressions
                        continue
            
            cases.append((label, bounds))
        
        return cases
    
    def _generate_case_combinations(self, case_results: List[List], constraints: List[str]) -> List[str]:
        """
        Generate all combinations of cases with safety limits.
        
        Args:
            case_results: List of case results from different terms
            constraints: List of constraint strings
            
        Returns:
            List of LaTeX formatted results
        """
        # Check combination limit
        total_combinations = 1
        for cases in case_results:
            total_combinations *= len(cases) if cases else 1
        
        if total_combinations > self.max_case_combinations:
            raise ProcessingError(
                f"Too many case combinations ({total_combinations}). "
                f"Limit is {self.max_case_combinations}."
            )
        
        # Generate combinations
        all_combos = list(product(*case_results))
        latex_results = []
        
        for combo in all_combos:
            case_result = self._combine_cases(combo, constraints)
            if case_result.is_valid():
                latex_output = self._format_latex_result(case_result)
                latex_results.append(latex_output)
        
        return latex_results
    
    def _combine_cases(self, case_combo: Tuple, constraints: List[str]) -> CaseResult:
        """
        Combine multiple cases into a single case result.
        
        Args:
            case_combo: Tuple of (label, bounds) from different terms
            constraints: List of constraint strings
            
        Returns:
            Combined CaseResult
        """
        labels = []
        all_bounds = []
        
        for label, bounds in case_combo:
            labels.append(label)
            all_bounds.extend(bounds)
        
        return CaseResult(labels, all_bounds, constraints)
    
    def _format_latex_result(self, case_result: CaseResult) -> str:
        """
        Format case result as LaTeX.
        
        Args:
            case_result: CaseResult to format
            
        Returns:
            LaTeX formatted string
        """
        # Format case header
        if case_result.labels:
            case_header = r"\\textbf{" + r" \\\\ ".join(case_result.labels) + r"}"
        else:
            case_header = r"\\textbf{Base Case}"
        
        # Format constraints
        if case_result.constraints:
            constraint_text = r" \\wedge ".join(case_result.constraints)
        else:
            constraint_text = r"\\text{(no additional constraints)}"
        
        # Format bounds
        max_lower = self._format_bound_expression(case_result.get_max_lower_bound(), r"-\\infty")
        min_upper = self._format_bound_expression(case_result.get_min_upper_bound(), r"+\\infty")
        
        # Generate complete LaTeX output
        latex_output = (
            case_header + r"\\\\[1em]" +
            r"\\left\\{" + constraint_text + r" \\wedge " +
            f"{max_lower} < x < {min_upper}" + r"\\right\\}\\\\[1em]" +
            r"\\left\\{" + constraint_text + r" \\wedge " +
            f"{max_lower} \\\\le x \\\\le {min_upper}" + r"\\right\\}"
        )
        
        return latex_output
    
    def _format_bound_expression(self, bound_expr, default: str) -> str:
        """Format a bound expression for LaTeX output."""
        if bound_expr is None:
            return default
        
        if isinstance(bound_expr, str) and bound_expr.startswith(('max(', 'min(')):
            # Already formatted
            return bound_expr
        
        try:
            return latex(bound_expr)
        except Exception:
            return str(bound_expr)
    
    def _format_constraint_only_result(self, constraints: List[str]) -> str:
        """Format result when there are only constraints, no variable terms."""
        if constraints:
            constraint_text = r" \\wedge ".join(constraints)
        else:
            constraint_text = r"\\text{(no constraints)}"
        
        return (
            r"\\textbf{Constraint-Only Case}\\\\[1em]" +
            r"\\left\\{" + constraint_text + r"\\right\\}"
        )
