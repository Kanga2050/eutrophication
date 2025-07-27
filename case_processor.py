"""
Case Processing Module for Rational Inequality Solver

This module handles the processing of solver output and generates properly formatted
LaTeX bounds expressions. It serves as the bridge between the core solver engine
and the output formatting system, combining multiple inequality cases using
Cartesian products to generate comprehensive solution sets.

Key Features:
- **Case Extraction**: Parse solver output into structured case data
- **Bound Generation**: Extract upper and lower bounds from case analysis
- **Cartesian Product Combination**: Generate all valid case combinations
- **LaTeX Formatting**: Create professional mathematical output
- **Sign Analysis Integration**: Support for optimized case filtering

Functions:
- isolate_cases_from_solver(): Extract structured data from raw solver output
- generate_case_labeled_bounds(): Main interface for generating LaTeX bounds
- _format_latex_output(): Format final results as LaTeX expressions

Algorithm:
1. **Parse Solver Output**: Extract case labels and bound expressions
2. **Separate Cases**: Distinguish between variable-dependent and independent cases
3. **Generate Combinations**: Use Cartesian product for all valid case combinations  
4. **Extract Bounds**: Identify upper and lower bounds for the target variable
5. **Format Output**: Generate LaTeX with proper mathematical notation

Author: Rational Inequality Solver Team
Version: Enhanced with Sign Analysis Support
"""
import re
from sympy import simplify
from sympy.printing.latex import latex
from itertools import product


def isolate_cases_from_solver(solver_output):
    """
    Extracts (label, bound_exprs) pairs from the full casework output.
    Each bound_exprs is a list of (bound_expr, direction), where direction is '>' or '<'.
    
    Args:
        solver_output: List of solver output strings
        
    Returns:
        List of (label, bounds) tuples
    """
    cases = []
    for output in solver_output:
        lines = output.splitlines()
        if not lines:
            continue
            
        label = lines[0].strip()
        bounds = []
        
        # Use regex for more robust parsing
        for line in lines:
            # Match patterns like "x < expr", "x > expr", "x <= expr", "x >= expr"
            match = re.search(r'x\s*([<>]=?)\s*(.+)', line.strip())
            if match:
                op, expr_str = match.groups()
                try:
                    expr = simplify(expr_str.strip())
                    direction = '<' if '<' in op else '>'
                    bounds.append((expr, direction))
                except Exception:
                    # Skip malformed expressions
                    continue
                    
        cases.append((label, bounds))
    return cases


def generate_case_labeled_bounds(ineq_list, x, solver_func, use_sign_analysis=True):
    """
    Generate LaTeX formatted bounds for all case combinations.
    
    Args:
        ineq_list: List of (lhs, op, rhs) tuples
        x: Variable symbol
        solver_func: Function to solve individual inequalities
        use_sign_analysis: Whether to use sign analysis optimization
        
    Returns:
        List of LaTeX formatted strings
    """
    no_x_constraints = []
    x_ineq_cases = []

    # Process each inequality
    for lhs, op, rhs in ineq_list:
        expr = simplify(lhs - rhs)
        
        if x not in expr.free_symbols:
            # Constraint doesn't involve x
            no_x_constraints.append(f"{lhs} {op} {rhs}")
        else:
            # Solve inequality involving x
            case_outputs = solver_func(expr, x, op, use_sign_analysis)
            parsed_cases = isolate_cases_from_solver(case_outputs)
            if parsed_cases:  # Only add non-empty cases
                x_ineq_cases.append(parsed_cases)

    if not x_ineq_cases:
        # No x-dependent inequalities
        return [_format_latex_output([], [], [], no_x_constraints)]

    # Generate all combinations of cases
    all_combos = list(product(*x_ineq_cases))
    outputs = []

    for combo in all_combos:
        labels = []
        lower_bounds = []
        upper_bounds = []

        # Extract bounds from each case in the combination
        for label, bounds in combo:
            labels.append(label)
            for expr, direction in bounds:
                if direction == '>':
                    lower_bounds.append(expr)
                elif direction == '<':
                    upper_bounds.append(expr)

        latex_output = _format_latex_output(labels, lower_bounds, upper_bounds, no_x_constraints)
        outputs.append(latex_output)

    return outputs


def _format_latex_output(labels, lower_bounds, upper_bounds, no_x_constraints):
    """
    Format the output as LaTeX.
    
    Args:
        labels: List of case labels
        lower_bounds: List of lower bound expressions
        upper_bounds: List of upper bound expressions
        no_x_constraints: List of constraints not involving x
        
    Returns:
        Formatted LaTeX string
    """
    # Format unchanged constraints
    if no_x_constraints:
        unchanged = r" \wedge ".join([str(constraint) for constraint in no_x_constraints])
    else:
        unchanged = r"\text{(no additional constraints)}"

    # Format bounds
    if lower_bounds:
        max_lower = r"\max\left(" + ", ".join([latex(e) for e in lower_bounds]) + r"\right)"
    else:
        max_lower = r"-\infty"

    if upper_bounds:
        min_upper = r"\min\left(" + ", ".join([latex(e) for e in upper_bounds]) + r"\right)"
    else:
        min_upper = r"+\infty"

    # Format case labels
    case_header = r"\textbf{" + r" \\ ".join(labels) + r"}" if labels else r"\textbf{Base Case}"

    # Generate LaTeX output
    latex_output = (
        case_header + r"\\[1em]" +
        r"\left\{" + unchanged + r" \wedge " +
        f"{max_lower} < x < {min_upper}" + r"\right\}\\[1em]" +
        r"\left\{" + unchanged + r" \wedge " +
        f"{max_lower} \\le x \\le {min_upper}" + r"\right\}"
    )

    return latex_output
