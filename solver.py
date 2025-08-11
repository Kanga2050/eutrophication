"""
Core Rational Inequality Solver Engine

This module contains the main solving logic for rational inequalities using symbolic
branch expansion and case-based analysis. It handles complex rational expressions
by analyzing numerator and denominator separately, considering all possible sign
combinations to generate complete solution sets.

Key Features:
- **Sign Analysis Integration**: Optional optimization that reduces impossible cases
- **Comprehensive Case Generation**: Analyzes all possible sign combinations
- **Polynomial Support**: Handles linear, quadratic, and cubic polynomials
- **Parameter Support**: Works with symbolic parameters in addition to variables
- **Mathematical Rigor**: Ensures all mathematically valid cases are considered

Algorithm Overview:
1. **Expression Decomposition**: Separate rational expression into numerator/denominator
2. **Sign Analysis** (optional): Determine if certain cases can be eliminated early
3. **Case Generation**: For each possible sign combination of numerator and denominator
4. **Polynomial Solving**: Solve resulting polynomial inequalities for each case
5. **Result Formatting**: Generate descriptive case labels with mathematical reasoning

Supported Operations:
- Inequality operators: <=, <, >=, >
- Linear polynomials: ax + b <op> 0
- Quadratic polynomials: ax² + bx + c <op> 0
- Rational expressions: P(x)/Q(x) <op> 0

Author: Rational Inequality Solver Team
Version: Enhanced with Sign Analysis Integration and cubic support
"""
from sympy import expand, simplify, sqrt, acos, cos, pi, real_root
from sign_analyzer import create_default_analyzer, apply_sign_analysis_to_solver_output


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
    if use_sign_analysis and analyzer:
        # Add common assumptions for mathematical constants
        analyzer.add_assumption(1, 'positive')

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
        elif deg == 3:
            branch = _solve_cubic_case(coeffs, num_op, op, case_label, den_cond, analyzer)
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
    elif deg == 3:
        return [_solve_cubic_case(coeffs, op, op, f"Simplified case ({reason})", "", None)]
    else:
        return [f"Simplified case ({reason}):\n  Nonlinear (deg={deg}): ({num_expr}) {op} 0"]


def _solve_linear_case(coeffs, num_op, case_label, den_cond, analyzer=None):
    """Handle linear polynomial case with optional sign analysis."""
    # Original code used B, C meaning B*x + C
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

    # root: B*x + C {op} 0  ->  x {op} -C/B
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

    # Use symbolic sqrt for clarity
    r1 = simplify((-B - sqrt(delta)) / (2*A))
    r2 = simplify((-B + sqrt(delta)) / (2*A))

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


def _solve_cubic_case(coeffs, num_op, op, case_label, den_cond, analyzer=None):
    """
    Handle cubic polynomial case and return a descriptive case block.
    coeffs = [A, B, C, D] for A*x^3 + B*x^2 + C*x + D.
    Matches the style/format of the linear/quadratic handlers.
    """
    A, B, C, D = coeffs

    # sign-analysis note for leading coefficient (same style as other handlers)
    if analyzer:
        a_sign = analyzer.analyze_sign(A)
        if a_sign == 'positive':
            case_label += f" (leading coefficient {A} > 0)"
        elif a_sign == 'negative':
            case_label += f" (leading coefficient {A} < 0)"
        elif a_sign == 'zero':
            return f"{case_label}:\n  Leading coefficient is zero: {A} = 0\n  Expression is actually degree < 3"

    # normalize to monic depressed cubic: x^3 + p x^2 + q x + r  (divide by A)
    p = simplify(B / A)
    q = simplify(C / A)
    r = simplify(D / A)

    # depressed cubic substitution x = t - p/3 -> t^3 + alpha*t + beta = 0
    alpha = simplify(q - p**2 / 3)
    beta = simplify(2*p**3 / 27 - p*q / 3 + r)

    # cubic discriminant
    Delta = simplify((beta / 2)**2 + (alpha / 3)**3)

    conds = [
        f"Depressed cubic parameters: alpha = {alpha}, beta = {beta}",
        f"Discriminant Delta = {Delta}",
        f"Back-substitution: x = t - ({p})/3"
    ]

    # CASE: Delta > 0 -> one real root (Cardano)
    if Delta.is_positive or (Delta != 0 and not Delta.is_negative):
        # use real_root for real cube roots where possible
        u = simplify(real_root(-beta / 2 + sqrt(Delta), 3))
        v = simplify(real_root(-beta / 2 - sqrt(Delta), 3))
        r1 = simplify(u + v - p / 3)
        conds.append(f"One real root (Cardano): r = {r1}")

        # qualitative solution pattern depends on sign(A) and operator
        if op in ('<', '<='):
            conds.append("Cubic has a single real root (graph crosses once).")
            conds.append("  If A > 0: cubic goes -∞ → +∞, so inequality holds to the left of root.")
            conds.append("  If A < 0: cubic goes +∞ → -∞, so inequality holds to the right of root.")
            conds.append(f"  Therefore: for A>0 solution ~ x {'<=' if op=='<=' else '<'} {r1}; for A<0 solution ~ x {'>=' if op=='<=' else '>'} {r1}")
        else:
            conds.append("Cubic has a single real root (graph crosses once).")
            conds.append("  If A > 0: cubic goes -∞ → +∞, so >= region is to the right of root.")
            conds.append("  If A < 0: cubic goes +∞ → -∞, so >= region is to the left of root.")
            conds.append(f"  Therefore: for A>0 solution ~ x {'>=' if op=='>=' else '>'} {r1}; for A<0 solution ~ x {'<=' if op=='>=' else '<'} {r1}")

        den_part = f"\n  and {den_cond}" if den_cond else ""
        return f"{case_label}:\n  " + "\n  ".join(conds) + den_part

    # CASE: Delta == 0 -> multiple roots (double or triple)
    if Delta == 0:
        # triple root when alpha == beta == 0
        if alpha == 0 and beta == 0:
            triple = simplify(-p / 3)
            conds.append(f"Triple root at x = {triple}")
            conds.append("Triple root has odd multiplicity (3) so sign changes through the root.")
            if op in ('<', '<='):
                conds.append("  For A>0: solution is x <= triple (qualitatively); for A<0: x >= triple.")
            else:
                conds.append("  For A>0: solution is x >= triple (qualitatively); for A<0: x <= triple.")
            den_part = f"\n  and {den_cond}" if den_cond else ""
            return f"{case_label}:\n  " + "\n  ".join(conds) + den_part

        # otherwise one double root and one simple root
        # For depressed cubic t^3 + alpha t + beta = 0 with Delta=0:
        # let u = real_root(beta/2,3). Then double root t_d = u and simple t_s = -2*u.
        u = simplify(real_root(beta / 2, 3))
        t_double = simplify(u)
        t_single = simplify(-2 * u)
        r_double = simplify(t_double - p / 3)
        r_single = simplify(t_single - p / 3)
        conds.append(f"Double root r_d = {r_double}, simple root r_s = {r_single}")
        conds.append("Sign-change rule: even multiplicity -> no sign change at double root; odd -> sign change at simple root.")
        conds.append("Construct solution by ordering the roots and applying multiplicity rule; include double root when operator allows equality.")
        den_part = f"\n  and {den_cond}" if den_cond else ""
        return f"{case_label}:\n  " + "\n  ".join(conds) + den_part

    # CASE: Delta < 0 -> three distinct real roots (trigonometric solution)
    rho = simplify(2 * sqrt(-alpha / 3))
    acos_arg = simplify((-beta / 2) / sqrt(- (alpha / 3)**3))
    theta = simplify(acos(acos_arg) / 3)

    t1 = simplify(rho * cos(theta))
    t2 = simplify(rho * cos(theta + 2 * pi / 3))
    t3 = simplify(rho * cos(theta + 4 * pi / 3))

    r1 = simplify(t1 - p / 3)
    r2 = simplify(t2 - p / 3)
    r3 = simplify(t3 - p / 3)

    conds.append("Three distinct real roots (trigonometric form):")
    conds.append(f"  r1 = {r1}")
    conds.append(f"  r2 = {r2}")
    conds.append(f"  r3 = {r3}")
    conds.append("Assume ordering r1 < r2 < r3 (sort if necessary).")

    if op in ('<', '<='):
        conds.append("Inequality <=0 / <0: include intervals where cubic is nonpositive/negative.")
        conds.append("  If A > 0: sign pattern (-, +, -, +) → solution for <=0: (-∞, r1] ∪ [r2, r3] (endpoints for <=).")
        conds.append("  If A < 0: pattern flips → solution for <=0: [r1, r2] ∪ [r3, ∞).")
    else:
        conds.append("Inequality >=0 / >0: include intervals where cubic is nonnegative/positive.")
        conds.append("  If A > 0: solution for >=0: [r1, r2] ∪ [r3, ∞).")
        conds.append("  If A < 0: solution for >=0: (-∞, r1] ∪ [r2, r3].")

    den_part = f"\n  and {den_cond}" if den_cond else ""
    return f"{case_label}:\n  " + "\n  ".join(conds) + den_part
