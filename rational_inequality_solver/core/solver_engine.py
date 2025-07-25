"""
Optimized solver engine with improved sign analysis and caching.
"""
from typing import List, Optional, Dict, Any, Callable
from functools import lru_cache
import time

from sympy import symbols, expand, simplify, Symbol
from sympy.core.expr import Expr

from ..core.inequality_system import InequalitySystem
from ..processors.case_processor import CaseProcessor
from ..utils.validation import SolverError, safe_simplify
from .sign_analyzer import SignAnalyzer, create_optimized_analyzer


class SolverEngine:
    """
    Enhanced solver engine with performance optimizations and caching.
    """
    
    def __init__(self, 
                 use_sign_analysis: bool = True,
                 enable_caching: bool = True,
                 max_recursion_depth: int = 10,
                 timeout_seconds: Optional[float] = None):
        """
        Initialize solver engine.
        
        Args:
            use_sign_analysis: Enable sign analysis optimization
            enable_caching: Enable result caching
            max_recursion_depth: Maximum recursion depth for complex cases
            timeout_seconds: Maximum time allowed for solving
        """
        self.use_sign_analysis = use_sign_analysis
        self.enable_caching = enable_caching
        self.max_recursion_depth = max_recursion_depth
        self.timeout_seconds = timeout_seconds
        
        # Initialize components
        self.case_processor = CaseProcessor()
        self.sign_analyzer = create_optimized_analyzer() if use_sign_analysis else None
        
        # Performance tracking
        self._solve_count = 0
        self._cache_hits = 0
        
        # Clear cache if caching is disabled
        if not enable_caching:
            self._solve_rational_inequality.cache_clear()
    
    def solve(self, system: InequalitySystem) -> List[str]:
        """
        Solve inequality system.
        
        Args:
            system: InequalitySystem to solve
            
        Returns:
            List of LaTeX formatted solution cases
            
        Raises:
            SolverError: If solving fails
        """
        start_time = time.time()
        
        try:
            # Validate system
            system.validate()
            
            # Process with timeout if specified
            if self.timeout_seconds:
                def timeout_solver_func(expr, var, op):
                    return self._solve_with_timeout(expr, var, op, start_time)
                solver_func = timeout_solver_func
            else:
                solver_func = self._solve_rational_inequality
            
            # Process system
            results = self.case_processor.process_system(system, solver_func)
            
            self._solve_count += 1
            return results
            
        except Exception as e:
            raise SolverError(f"Failed to solve inequality system: {e}")
    
    def _solve_with_timeout(self, expr: Expr, var: Symbol, op: str, start_time: float) -> List[str]:
        """Solve with timeout checking."""
        if time.time() - start_time > self.timeout_seconds:
            raise SolverError(f"Solver timeout after {self.timeout_seconds} seconds")
        
        return self._solve_rational_inequality(expr, var, op)
    
    @lru_cache(maxsize=128)
    def _solve_rational_inequality(self, expr: Expr, var: Symbol, op: str) -> List[str]:
        """
        Solve rational inequality with caching.
        
        Args:
            expr: Expression to solve
            var: Variable symbol
            op: Operator string
            
        Returns:
            List of case descriptions
        """
        # Check cache hit
        if self.enable_caching:
            cache_info = self._solve_rational_inequality.cache_info()
            if cache_info.hits > self._cache_hits:
                self._cache_hits = cache_info.hits
        
        try:
            N, D = expr.as_numer_denom()
            N = expand(N)
            D = expand(D)
            
            # Apply sign analysis optimizations
            if self.use_sign_analysis and self.sign_analyzer:
                simplified_result = self._try_sign_analysis_simplification(N, D, var, op)
                if simplified_result:
                    return simplified_result
            
            # Standard case analysis
            return self._standard_case_analysis(N, D, var, op)
            
        except Exception as e:
            raise SolverError(f"Error solving {expr} {op} 0: {e}")
    
    def _try_sign_analysis_simplification(self, N: Expr, D: Expr, var: Symbol, op: str) -> Optional[List[str]]:
        """
        Try to simplify using sign analysis.
        
        Args:
            N: Numerator expression
            D: Denominator expression  
            var: Variable symbol
            op: Operator string
            
        Returns:
            Simplified result if possible, None otherwise
        """
        try:
            # Analyze signs
            num_sign = self.sign_analyzer.analyze_sign(N)
            den_sign = self.sign_analyzer.analyze_sign(D)
            
            # Handle definite denominator signs
            if den_sign == 'positive':
                return self._solve_simplified_case(N, var, op, "denominator always positive")
            elif den_sign == 'negative':
                inverted_op = self._invert_operator(op)
                return self._solve_simplified_case(N, var, inverted_op, "denominator always negative")
            elif den_sign == 'zero':
                return [f"Expression undefined: denominator {D} = 0"]
            
            # Handle definite numerator signs
            if num_sign == 'zero':
                if op in ['<=', '>=']:
                    return [f"Expression always satisfies {op} 0: numerator {N} = 0"]
                else:
                    return [f"Expression never satisfies {op} 0: numerator {N} = 0"]
            
            return None  # No simplification possible
            
        except Exception:
            return None  # Fall back to standard analysis
    
    def _solve_simplified_case(self, num_expr: Expr, var: Symbol, op: str, reason: str) -> List[str]:
        """
        Solve simplified case where denominator sign is known.
        
        Args:
            num_expr: Numerator expression
            var: Variable symbol
            op: Operator string
            reason: Explanation for simplification
            
        Returns:
            List of case descriptions
        """
        num_poly = num_expr.as_poly(var)
        if num_poly is None:
            return [f"Simplified case ({reason}):\\n  Condition: ({num_expr}) {op} 0"]
        
        deg = num_poly.degree()
        coeffs = num_poly.all_coeffs()
        
        if deg == 1:
            return [self._solve_linear_case(coeffs, op, f"Simplified case ({reason})", "")]
        elif deg == 2:
            return [self._solve_quadratic_case(coeffs, op, op, f"Simplified case ({reason})", "")]
        else:
            return [f"Simplified case ({reason}):\\n  Nonlinear (deg={deg}): ({num_expr}) {op} 0"]
    
    def _standard_case_analysis(self, N: Expr, D: Expr, var: Symbol, op: str) -> List[str]:
        """
        Perform standard case analysis.
        
        Args:
            N: Numerator expression
            D: Denominator expression
            var: Variable symbol
            op: Operator string
            
        Returns:
            List of case descriptions
        """
        branches = []
        inverted_op = self._invert_operator(op)
        
        cases = [(op, '>'), (inverted_op, '<')]
        case_labels = [
            f"Case 1: Entire expression {op} 0 because {N} {op} 0 and {D} > 0",
            f"Case 2: Entire expression {op} 0 because {N} {inverted_op} 0 and {D} < 0"
        ]
        
        for i, (num_op, den_op) in enumerate(cases):
            case_label = case_labels[i]
            den_cond = f"({D}) {den_op} 0"
            
            num_poly = N.as_poly(var)
            if num_poly is None:
                branches.append(f"{case_label}:\\n  Condition: ({N}) {num_op} 0\\n  and {den_cond}")
                continue
            
            deg = num_poly.degree()
            coeffs = num_poly.all_coeffs()
            
            if deg == 1:
                branch = self._solve_linear_case(coeffs, num_op, case_label, den_cond)
                branches.append(branch)
            elif deg == 2:
                branch = self._solve_quadratic_case(coeffs, num_op, op, case_label, den_cond)
                branches.append(branch)
            else:
                branches.append(f"{case_label}:\\n  Nonlinear (deg={deg}): ({N}) {num_op} 0\\n  and {den_cond}")
        
        return branches
    
    def _solve_linear_case(self, coeffs: List, num_op: str, case_label: str, den_cond: str) -> str:
        """Handle linear polynomial case."""
        B, C = coeffs
        
        # Apply sign analysis if available
        if self.use_sign_analysis and self.sign_analyzer:
            b_sign = self.sign_analyzer.analyze_sign(B)
            if b_sign == 'positive':
                case_label += f" (coefficient {B} > 0)"
            elif b_sign == 'negative':
                case_label += f" (coefficient {B} < 0)"
            elif b_sign == 'zero':
                return f"{case_label}:\\n  Linear coefficient is zero: {B} = 0\\n  Expression reduces to constant {C}"
        
        root = safe_simplify(-C / B)
        den_part = f"\\n  and {den_cond}" if den_cond else ""
        return (f"{case_label}:\\n"
                f"  Linear condition: x {num_op} {root}{den_part}\\n")
    
    def _solve_quadratic_case(self, coeffs: List, num_op: str, op: str, case_label: str, den_cond: str) -> str:
        """Handle quadratic polynomial case."""
        A, B, C = coeffs
        
        # Apply sign analysis if available
        if self.use_sign_analysis and self.sign_analyzer:
            a_sign = self.sign_analyzer.analyze_sign(A)
            if a_sign == 'positive':
                case_label += f" (leading coefficient {A} > 0)"
            elif a_sign == 'negative':
                case_label += f" (leading coefficient {A} < 0)"
            elif a_sign == 'zero':
                return f"{case_label}:\\n  Leading coefficient is zero: {A} = 0\\n  Expression is actually linear or constant"
        
        delta = safe_simplify(B**2 - 4*A*C)
        r1 = safe_simplify((-B - delta**0.5) / (2*A))
        r2 = safe_simplify((-B + delta**0.5) / (2*A))
        
        conds = [
            f"Discriminant = {delta}",
            f"Leading coefficient A = {A}",
            f"If {delta} < 0:"
        ]
        
        # Add discriminant < 0 cases
        if op in ('<', '<='):
            conds.extend([
                f"  If {A} > 0 → No solution",
                f"  If {A} < 0 → All real x"
            ])
        else:
            conds.extend([
                f"  If {A} > 0 → All real x",
                f"  If {A} < 0 → No solution"
            ])
        
        # Add discriminant >= 0 cases
        conds.extend([
            f"If {delta} >= 0:",
            "  Let r1 = " + str(r1),
            "  Let r2 = " + str(r2),
            "  Assume r1 < r2"
        ])
        
        if op in ('<', '<='):
            conds.extend([
                f"  If {A} > 0 → inequality holds between roots:",
                f"    {r1} < x < {r2}",
                f"  If {A} < 0 → inequality holds outside roots:",
                f"    x < {r1} or x > {r2}"
            ])
        else:
            conds.extend([
                f"  If {A} > 0 → inequality holds outside roots:",
                f"    x < {r1} or x > {r2}",
                f"  If {A} < 0 → inequality holds between roots:",
                f"    {r1} < x < {r2}"
            ])
        
        den_part = f"\\n  and {den_cond}" if den_cond else ""
        return f"{case_label}:\\n  " + "\\n  ".join(conds) + den_part
    
    def _invert_operator(self, op: str) -> str:
        """Invert inequality operator."""
        return {'<=': '>', '<': '>=', '>=': '<', '>': '<='}[op]
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        cache_info = self._solve_rational_inequality.cache_info() if self.enable_caching else None
        
        return {
            'solve_count': self._solve_count,
            'cache_enabled': self.enable_caching,
            'cache_hits': cache_info.hits if cache_info else 0,
            'cache_misses': cache_info.misses if cache_info else 0,
            'sign_analysis_enabled': self.use_sign_analysis,
        }
    
    def clear_cache(self):
        """Clear the solver cache."""
        if self.enable_caching:
            self._solve_rational_inequality.cache_clear()
            self._cache_hits = 0
