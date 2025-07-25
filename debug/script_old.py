import sys
import os
# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
Legacy script.py - now refactored into separate modules.
This file imports from the new modular structure.
"""
from solver import solve_rational_ineq_full

            conds.append(f"Discriminant = {delta}")
            conds.append(f"Leading coefficient A = {A}")

            # Only define inequality intervals if discriminant >= 0
            conds.append(f"If {delta} < 0:")
            if op in ('<', '<='):
                conds.append(f"  If {A} > 0 → No solution")
                conds.append(f"  If {A} < 0 → All real x")
            else:
                conds.append(f"  If {A} > 0 → All real x")
                conds.append(f"  If {A} < 0 → No solution")

            conds.append(f"If {delta} >= 0:")
            conds.append("  Let r1 = " + str(r1))
            conds.append("  Let r2 = " + str(r2))
            conds.append("  Assume r1 < r2")

            if op in ('<', '<='):
                conds.append(f"  If {A} > 0 → inequality holds between roots:")
                conds.append(f"    {r1} < x < {r2}")
                conds.append(f"  If {A} < 0 → inequality holds outside roots:")
                conds.append(f"    x < {r1} or x > {r2}")
            else:
                conds.append(f"  If {A} > 0 → inequality holds outside roots:")
                conds.append(f"    x < {r1} or x > {r2}")
                conds.append(f"  If {A} < 0 → inequality holds between roots:")
                conds.append(f"    {r1} < x < {r2}")

            branches.append(f"{case_label}:\n  " + "\n  ".join(conds) + f"\n  and {den_cond}")

        else:
            branches.append(f"{case_label}:\n  Nonlinear (deg={deg}): ({N}) {num_op} 0\n  and {den_cond}")

    return branches



# Prepare the symbolic expression
a, b, c, d, e, f, g, x = symbols("a b c d e f g x")
expr_str = """
    x/((c-a)*(b-g))-1
"""
expr = simplify(sympify(expr_str, evaluate=False))
solution_branches = solve_rational_ineq_full(expr, x, ">=")

for i in solution_branches:
    print(i)# return first two branches as sample (output trimmed for space)