import sys
import os
# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys
import os
# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sympy.printing.latex import latex
from solver import solve_rational_ineq_full

from sympy import symbols, simplify, sympify
from itertools import product

def isolate_cases_from_solver(solver_output):
    """
    Extracts (label, bound_exprs) pairs from the full casework output.
    Each bound_exprs is a list of (bound_expr, direction), where direction is '>' or '<'.
    """
    cases = []
    for output in solver_output:
        lines = output.splitlines()
        label = lines[0].strip()
        bounds = []
        for line in lines:
            if "x <" in line or "x >" in line or "x <=" in line or "x >=" in line:
                parts = line.strip().split("x")
                if len(parts) == 2:
                    op_expr = parts[1].strip()
                    if op_expr.startswith('<') or op_expr.startswith('<='):
                        op = '<=' if '<=' in op_expr else '<'
                        expr = simplify(op_expr.replace('<=', '').replace('<', '').strip())
                        bounds.append((expr, '<'))
                    elif op_expr.startswith('>') or op_expr.startswith('>='):
                        op = '>=' if '>=' in op_expr else '>'
                        expr = simplify(op_expr.replace('>=', '').replace('>', '').strip())
                        bounds.append((expr, '>'))
        cases.append((label, bounds))
    return cases

def generate_case_labeled_bounds(ineq_list, x, solver_func):
    no_x = []
    x_ineq_cases = []

    for lhs, op, rhs in ineq_list:
        expr = simplify(lhs - rhs)
        free_syms = expr.free_symbols
        if x not in free_syms:
            no_x.append(f"{lhs} {op} {rhs}")
        else:
            case_outputs = solver_func(expr, x, op)
            parsed_cases = isolate_cases_from_solver(case_outputs)
            x_ineq_cases.append(parsed_cases)

    all_combos = list(product(*x_ineq_cases))
    outputs = []

    for combo in all_combos:
        labels = []
        lower_bounds = []
        upper_bounds = []

        for label, bounds in combo:
            labels.append(label)
            for expr, direction in bounds:
                if direction == '>':
                    lower_bounds.append(expr)
                elif direction == '<':
                    upper_bounds.append(expr)

        unchanged = r" \wedge ".join([f"{str(i)}" for i in no_x]) if no_x else r"\text{(no unchanged)}"
        max_lower = r"\max\left(" + ", ".join([latex(e) for e in lower_bounds]) + r"\right)" if lower_bounds else "-\infty"
        min_upper = r"\min\left(" + ", ".join([latex(e) for e in upper_bounds]) + r"\right)" if upper_bounds else "\infty"

        latex_output = (
            r"\textbf{" + r" \\ ".join(labels) + r"}\\[1em]" +
            r"\left\{" + unchanged + r" \wedge " +
            f"{max_lower} < x < {min_upper}" + r"\right\}\\[1em]" +
            r"\left\{" + unchanged + r" \wedge " +
            f"{max_lower} \le x \le {min_upper}" + r"\right\}"
        )

        outputs.append(latex_output)

    return outputs


x, a, b, c, d, e, f, g = symbols('x a b c d e f g')

ineqs = [
    ((a*x - c + b - 1)/(a*b*d) - b/a + 1/a + (b*d*c)/a - (x - e*f*c + (b - 1 - b*d*c)*(e*f + g*x)) / (g*c + 1 - c*f*a - g*x), "<="),
    ((x + 1)*(x - 2)/(x + 3), ">="),
    (a + b, "<= c"),  # doesn't involve x
]

# Prepare (lhs, op, rhs) form
processed_ineqs = []
for expr, op in ineqs:
    if isinstance(expr, str):
        lhs, rhs = expr.split(op)
        processed_ineqs.append((sympify(lhs), op, sympify(rhs)))
    elif isinstance(expr, tuple):
        lhs, rhs = expr
        processed_ineqs.append((lhs, op, rhs))
    else:
        processed_ineqs.append((expr, op, 0))

results = generate_case_labeled_bounds(processed_ineqs, x, solve_rational_ineq_full)

# Print LaTeX
for i, latex_out in enumerate(results):
    print(f"--- Case {i+1} ---")
    print(latex_out)
    print("\n")
