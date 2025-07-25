"""
Core solver module for rational inequalities.
Contains the main solving logic and case generation with sign analysis optimization.
"""
from sympy import symbols, expand, simplify
from sign_analyzer import SignAnalyzer, create_default_analyzer, apply_sign_analysis_to_solver_output


def solve_rational_ineq_full(expr, x, op, use_sign_analysis=True):
    """
    Solve a rational inequality expr <op> 0 by symbolic branch expansion.
    Each condition is printed fully in terms of constants and x.
    
    Args:
        expr: SymPy expression
        x: Variable symbol
        op: Operator string ('<=', '<', '>=', '>')
        use_sign_analysis: Whether to use sign analysis for optimization
        
    Returns:
        List of case descriptions
    """
    N, D = expr.as_numer_denom()
    N = expand(N)
    D = expand(D)

    def invert_op(o):
        """Invert inequality operator."""
        return {'<=': '>', '<': '>=', '>=': '<', '>': '<='}[o]

    # Initialize sign analyzer
    analyzer = create_default_analyzer() if use_sign_analysis else None
    
    # Perform sign analysis if enabled
    if use_sign_analysis:
        # Add common assumptions for mathematical constants
        analyzer.add_assumption(1, 'positive')
        # Add assumptions that squares are non-negative
        # Note: x**2 >= 0 for real x
        
        # Check if we can determine signs of numerator or denominator
        num_sign = analyzer.analyze_sign(N)
        den_sign = analyzer.analyze_sign(D)
        
        # If denominator is always positive/negative, we can simplify
        if den_sign == 'positive':
            return _solve_simplified_case(N, x, op, "denominator always positive")
        elif den_sign == 'negative':
            inverted_op = invert_op(op)
            return _solve_simplified_case(N, x, inverted_op, "denominator always negative")
        elif den_sign == 'zero':
            return [f"Expression undefined: denominator {D} = 0"]
        
        # If numerator has definite sign, we can simplify some cases
        if num_sign == 'zero':
            if op in ['<=', '>=']:
                return [f"Expression always satisfies {op} 0: numerator {N} = 0"]
            else:
                return [f"Expression never satisfies {op} 0: numerator {N} = 0"]

    branches = []
    cases = [(op, '>'), (invert_op(op), '<')]
    case_labels = [
        f"Case 1: Entire expression {op} 0 because {N} {op} 0 and {D} > 0",
        f"Case 2: Entire expression {op} 0 because {N} {invert_op(op)} 0 and {D} < 0"
    ]

    for i, (num_op, den_op) in enumerate(cases):
        case_label = case_labels[i]
        den_cond = f"({D}) {den_op} 0"

        num_poly = N.as_poly(x)
        if num_poly is None:
            branches.append(f"{case_label}:\n  Condition: ({N}) {num_op} 0\n  and {den_cond}")
            continue

        deg = num_poly.degree()
        coeffs = num_poly.all_coeffs()

        if deg == 1:
            branch = _solve_linear_case(coeffs, num_op, case_label, den_cond, analyzer)
            branches.append(branch)
        elif deg == 2:
            branch = _solve_quadratic_case(coeffs, num_op, op, case_label, den_cond, analyzer)
            branches.append(branch)
        else:
            branches.append(f"{case_label}:\n  Nonlinear (deg={deg}): ({N}) {num_op} 0\n  and {den_cond}")

    # Apply sign analysis to filter impossible cases
    if use_sign_analysis and analyzer:
        branches = apply_sign_analysis_to_solver_output(branches, analyzer)

    return branches

def _solve_simplified_case(num_expr, x, op, reason):
    """
    Solve simplified case where denominator sign is known.
    
    Args:
        num_expr: Numerator expression
        x: Variable symbol
        op: Operator string
        reason: Explanation for simplification
        
    Returns:
        List of case descriptions
    """
    num_poly = num_expr.as_poly(x)
    if num_poly is None:
        return [f"Simplified case ({reason}):\n  Condition: ({num_expr}) {op} 0"]
    
    deg = num_poly.degree()
    coeffs = num_poly.all_coeffs()
    
    if deg == 1:
        return [_solve_linear_case(coeffs, op, f"Simplified case ({reason})", "", None)]
    elif deg == 2:
        return [_solve_quadratic_case(coeffs, op, op, f"Simplified case ({reason})", "", None)]
    else:
        return [f"Simplified case ({reason}):\n  Nonlinear (deg={deg}): ({num_expr}) {op} 0"]


def _solve_linear_case(coeffs, num_op, case_label, den_cond, analyzer=None):
    """Handle linear polynomial case with optional sign analysis."""
    B, C = coeffs
    
    # Apply sign analysis to coefficients if available
    if analyzer:
        b_sign = analyzer.analyze_sign(B)
        c_sign = analyzer.analyze_sign(C)
        
        # If coefficient signs are known, we can provide more specific analysis
        if b_sign == 'positive':
            case_label += f" (coefficient {B} > 0)"
        elif b_sign == 'negative':
            case_label += f" (coefficient {B} < 0)"
        elif b_sign == 'zero':
            return f"{case_label}:\n  Linear coefficient is zero: {B} = 0\n  Expression reduces to constant {C}"
    
    root = simplify(-C / B)
    den_part = f"\n  and {den_cond}" if den_cond else ""
    return (f"{case_label}:\n"
            f"  Linear condition: x {num_op} {root}{den_part}\n")


def _solve_quadratic_case(coeffs, num_op, op, case_label, den_cond, analyzer=None):
    """Handle quadratic polynomial case with optional sign analysis."""
    A, B, C = coeffs
    
    # Apply sign analysis to leading coefficient if available
    if analyzer:
        a_sign = analyzer.analyze_sign(A)
        if a_sign == 'positive':
            case_label += f" (leading coefficient {A} > 0)"
        elif a_sign == 'negative':
            case_label += f" (leading coefficient {A} < 0)"
        elif a_sign == 'zero':
            # Degenerate case - not actually quadratic
            return f"{case_label}:\n  Leading coefficient is zero: {A} = 0\n  Expression is actually linear or constant"
    
    delta = simplify(B**2 - 4*A*C)

    r1 = simplify((-B - delta**0.5) / (2*A))
    r2 = simplify((-B + delta**0.5) / (2*A))

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

    den_part = f"\n  and {den_cond}" if den_cond else ""
    return f"{case_label}:\n  " + "\n  ".join(conds) + den_part
