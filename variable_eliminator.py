"""
Enhanced Variable Elimination Solver for Rational Inequalities.

This module implements a recursive variable elimination approach where variables
x1, x2, ..., xn are isolated and eliminated one by one, creating min/max expressions
that are then expanded into multiple inequality cases.
"""
from sympy import symbols, simplify, latex, Min, Max
from sympy.printing.latex import latex
from itertools import product
import os
from datetime import datetime

from solver import solve_rational_ineq_full
from case_processor import isolate_cases_from_solver
from input_processor import process_inequalities


class VariableEliminationSolver:
    """
    Enhanced solver that eliminates variables sequentially using min/max decomposition.
    """
    
    def __init__(self, use_sign_analysis=True):
        """
        Initialize the variable elimination solver.
        
        Args:
            use_sign_analysis: Whether to use sign analysis for optimization
        """
        self.use_sign_analysis = use_sign_analysis
        self.steps = []  # Store all steps for LaTeX output
        
    def solve_with_variable_elimination(self, inequalities, variables_to_eliminate):
        """
        Solve system by eliminating variables sequentially.
        
        Args:
            inequalities: List of inequality strings or tuples
            variables_to_eliminate: List of variable names ['x1', 'x2', ..., 'xn']
            
        Returns:
            dict: Complete solution with all steps
        """
        self.steps = []
        current_inequalities = process_inequalities(inequalities)
        
        # Step 0: Initial system
        step_0 = {
            'step_number': 0,
            'description': 'Initial Inequality System',
            'variable_eliminated': None,
            'input_inequalities': current_inequalities,
            'min_max_expressions': [],
            'eliminated_expressions': [],
            'output_inequalities': []
        }
        self.steps.append(step_0)
        
        # Eliminate each variable in sequence
        for i, var_name in enumerate(variables_to_eliminate):
            var_symbol = symbols(var_name)
            
            print(f"Eliminating variable: {var_name}")
            
            # Step 1: Isolate variable and create min/max expressions
            min_max_result = self._isolate_variable(current_inequalities, var_symbol)
            
            # Step 2: Remove variable from min/max expressions
            eliminated_result = self._eliminate_variable_from_minmax(min_max_result, var_symbol)
            
            # Step 3: Expand min/max combinations into new inequalities
            new_inequalities = self._expand_minmax_combinations(eliminated_result)
            
            # Record this elimination step
            step = {
                'step_number': i + 1,
                'description': f'Eliminate Variable {var_name}',
                'variable_eliminated': var_name,
                'input_inequalities': current_inequalities,
                'min_max_expressions': min_max_result,
                'eliminated_expressions': eliminated_result,
                'output_inequalities': new_inequalities
            }
            self.steps.append(step)
            
            # Update for next iteration
            current_inequalities = new_inequalities
            
            print(f"After eliminating {var_name}: {len(current_inequalities)} inequalities")
        
        return {
            'steps': self.steps,
            'final_inequalities': current_inequalities,
            'total_steps': len(variables_to_eliminate)
        }
    
    def _isolate_variable(self, inequalities, variable):
        """
        Isolate a variable from the inequality system, creating min/max expressions.
        
        Args:
            inequalities: List of (lhs, op, rhs) tuples
            variable: Variable symbol to isolate
            
        Returns:
            dict: Min/max expressions and constraints
        """
        constraints_without_var = []
        variable_bounds = []
        
        for lhs, op, rhs in inequalities:
            expr = simplify(lhs - rhs)
            
            if variable not in expr.free_symbols:
                # Constraint doesn't involve the variable
                constraints_without_var.append((lhs, op, rhs))
            else:
                # Solve for the variable bounds
                try:
                    # Use the existing solver to get bounds
                    case_outputs = solve_rational_ineq_full(expr, variable, op, self.use_sign_analysis)
                    parsed_cases = isolate_cases_from_solver(case_outputs)
                    
                    for label, bounds in parsed_cases:
                        for bound_expr, direction in bounds:
                            variable_bounds.append({
                                'expression': bound_expr,
                                'direction': direction,  # '>' for lower bound, '<' for upper bound
                                'case_label': label,
                                'original_inequality': (lhs, op, rhs)
                            })
                            
                except Exception as e:
                    print(f"Warning: Could not process inequality {expr} {op} 0: {e}")
                    # Fallback: treat as constraint
                    constraints_without_var.append((lhs, op, rhs))
        
        # Separate lower and upper bounds
        lower_bounds = [b for b in variable_bounds if b['direction'] == '>']
        upper_bounds = [b for b in variable_bounds if b['direction'] == '<']
        
        return {
            'constraints_without_var': constraints_without_var,
            'lower_bounds': lower_bounds,
            'upper_bounds': upper_bounds,
            'variable': variable
        }
    
    def _eliminate_variable_from_minmax(self, min_max_result, variable):
        """
        Create min/max expressions without the variable.
        
        Args:
            min_max_result: Result from _isolate_variable
            variable: Variable being eliminated
            
        Returns:
            dict: Min/max expressions without the variable
        """
        lower_bounds = min_max_result['lower_bounds']
        upper_bounds = min_max_result['upper_bounds']
        constraints = min_max_result['constraints_without_var']
        
        # Extract bound expressions (remove variable from consideration)
        lower_exprs = [bound['expression'] for bound in lower_bounds]
        upper_exprs = [bound['expression'] for bound in upper_bounds]
        
        # Create min/max expressions
        min_expr = None
        max_expr = None
        
        if upper_exprs:
            min_expr = Min(*upper_exprs) if len(upper_exprs) > 1 else upper_exprs[0]
            
        if lower_exprs:
            max_expr = Max(*lower_exprs) if len(lower_exprs) > 1 else lower_exprs[0]
        
        return {
            'constraints_without_var': constraints,
            'min_expression': min_expr,
            'max_expression': max_expr,
            'lower_bound_details': lower_bounds,
            'upper_bound_details': upper_bounds,
            'variable_eliminated': variable
        }
    
    def _expand_minmax_combinations(self, eliminated_result):
        """
        Expand min/max combinations into new inequality cases.
        
        Args:
            eliminated_result: Result from _eliminate_variable_from_minmax
            
        Returns:
            List of new inequality tuples
        """
        constraints = eliminated_result['constraints_without_var']
        min_expr = eliminated_result['min_expression']
        max_expr = eliminated_result['max_expression']
        lower_details = eliminated_result['lower_bound_details']
        upper_details = eliminated_result['upper_bound_details']
        
        new_inequalities = list(constraints)  # Start with constraints
        
        # For each combination of a term from max with a term from min,
        # create a new inequality: max_term <= min_term
        if max_expr is not None and min_expr is not None:
            # Get individual terms from Min/Max expressions
            max_terms = max_expr.args if hasattr(max_expr, 'args') and len(max_expr.args) > 1 else [max_expr]
            min_terms = min_expr.args if hasattr(min_expr, 'args') and len(min_expr.args) > 1 else [min_expr]
            
            # Create all combinations
            for max_term in max_terms:
                for min_term in min_terms:
                    # Create inequality: max_term <= min_term
                    new_inequalities.append((max_term, '<=', min_term))
        
        return new_inequalities
    
    def generate_latex_report(self):
        """
        Generate a comprehensive LaTeX report of all elimination steps.
        
        Returns:
            str: Complete LaTeX document
        """
        latex_content = self._generate_latex_header()
        
        for step in self.steps:
            latex_content += self._generate_step_latex(step)
        
        latex_content += self._generate_latex_footer()
        
        return latex_content
    
    def _generate_latex_header(self):
        """Generate LaTeX document header."""
        return r"""
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{geometry}
\usepackage{enumitem}
\geometry{margin=1in}

\title{Sequential Variable Elimination for Rational Inequalities}
\author{Enhanced Rational Inequality Solver}
\date{\today}

\begin{document}
\maketitle

\section{Introduction}

This document shows the step-by-step elimination of variables from a system of rational inequalities. 
For each variable elimination, we show four sub-steps:
\begin{enumerate}
\item Original inequalities involving the variable
\item Min/Max expressions after isolation
\item Min/Max expressions after variable elimination
\item Final expanded inequalities
\end{enumerate}

"""

    def _generate_step_latex(self, step):
        """Generate LaTeX for a single elimination step."""
        if step['step_number'] == 0:
            return self._generate_initial_system_latex(step)
        else:
            return self._generate_elimination_step_latex(step)
    
    def _generate_initial_system_latex(self, step):
        """Generate LaTeX for the initial system."""
        latex_content = r"\section{Initial System}" + "\n\n"
        latex_content += r"Starting with the following system of inequalities:" + "\n\n"
        latex_content += r"\begin{align}" + "\n"
        
        for i, (lhs, op, rhs) in enumerate(step['input_inequalities']):
            latex_content += f"& {latex(lhs)} {op} {latex(rhs)}"
            if i < len(step['input_inequalities']) - 1:
                latex_content += r" \\" + "\n"
            else:
                latex_content += "\n"
        
        latex_content += r"\end{align}" + "\n\n"
        return latex_content
    
    def _generate_elimination_step_latex(self, step):
        """Generate LaTeX for a variable elimination step."""
        var_name = step['variable_eliminated']
        step_num = step['step_number']
        
        latex_content = f"\\section{{Step {step_num}: Eliminate Variable ${var_name}$}}\n\n"
        
        # Sub-step 1: Input inequalities (ALL inequalities from this step)
        latex_content += f"\\subsection{{Step {step_num}.1: Input Inequalities}}\n\n"
        
        # Separate inequalities involving the variable vs those that don't
        var_related = []
        var_unrelated = []
        
        for ineq in step['input_inequalities']:
            lhs, op, rhs = ineq
            # Check if variable appears in this inequality
            var_appears = (str(var_name) in str(lhs)) or (str(var_name) in str(rhs))
            if var_appears:
                var_related.append(ineq)
            else:
                var_unrelated.append(ineq)
        
        # Show inequalities involving the variable first
        if var_related:
            latex_content += f"Inequalities involving ${var_name}$:\n"
            latex_content += r"\begin{align}" + "\n"
            for i, (lhs, op, rhs) in enumerate(var_related):
                latex_content += f"& {latex(lhs)} {op} {latex(rhs)}"
                if i < len(var_related) - 1:
                    latex_content += r" \\" + "\n"
                else:
                    latex_content += "\n"
            latex_content += r"\end{align}" + "\n\n"
        
        # Show unrelated inequalities at the bottom
        if var_unrelated:
            latex_content += f"Inequalities not involving ${var_name}$ (preserved):\n"
            latex_content += r"\begin{align}" + "\n"
            for i, (lhs, op, rhs) in enumerate(var_unrelated):
                latex_content += f"& {latex(lhs)} {op} {latex(rhs)}"
                if i < len(var_unrelated) - 1:
                    latex_content += r" \\" + "\n"
                else:
                    latex_content += "\n"
            latex_content += r"\end{align}" + "\n\n"
        
        # Sub-step 2: Min/Max expressions with proper format
        latex_content += f"\\subsection{{Step {step_num}.2: Min/Max Bounds for ${var_name}$}}\n\n"
        min_max = step['min_max_expressions']
        
        # Format: max(expressions) <= x <= min(expressions) or max(expressions) < x < min(expressions)
        lower_exprs = [bound['expression'] for bound in min_max['lower_bounds']] if min_max['lower_bounds'] else []
        upper_exprs = [bound['expression'] for bound in min_max['upper_bounds']] if min_max['upper_bounds'] else []
        
        if lower_exprs and upper_exprs:
            # Both bounds exist - show complete constraint
            max_expr = f"\\max\\left({', '.join([latex(expr) for expr in lower_exprs])}\\right)" if len(lower_exprs) > 1 else latex(lower_exprs[0])
            min_expr = f"\\min\\left({', '.join([latex(expr) for expr in upper_exprs])}\\right)" if len(upper_exprs) > 1 else latex(upper_exprs[0])
            
            latex_content += r"\begin{align}" + "\n"
            latex_content += f"& {max_expr} \\leq {var_name} \\leq {min_expr}\n"
            latex_content += r"\end{align}" + "\n\n"
            
        elif lower_exprs:
            # Only lower bounds
            max_expr = f"\\max\\left({', '.join([latex(expr) for expr in lower_exprs])}\\right)" if len(lower_exprs) > 1 else latex(lower_exprs[0])
            latex_content += r"\begin{align}" + "\n"
            latex_content += f"& {var_name} \\geq {max_expr}\n"
            latex_content += r"\end{align}" + "\n\n"
            
        elif upper_exprs:
            # Only upper bounds
            min_expr = f"\\min\\left({', '.join([latex(expr) for expr in upper_exprs])}\\right)" if len(upper_exprs) > 1 else latex(upper_exprs[0])
            latex_content += r"\begin{align}" + "\n"
            latex_content += f"& {var_name} \\leq {min_expr}\n"
            latex_content += r"\end{align}" + "\n\n"
        else:
            latex_content += "No bounds found for this variable.\n\n"
        
        # Sub-step 3: After elimination - show constraint between bounds
        latex_content += f"\\subsection{{Step {step_num}.3: Constraint After Eliminating ${var_name}$}}\n\n"
        eliminated = step['eliminated_expressions']
        
        if eliminated['max_expression'] is not None and eliminated['min_expression'] is not None:
            latex_content += "For the system to be feasible:\n"
            latex_content += r"\begin{align}" + "\n"
            latex_content += f"& {latex(eliminated['max_expression'])} \\leq {latex(eliminated['min_expression'])}\n"
            latex_content += r"\end{align}" + "\n\n"
        elif eliminated['max_expression'] is not None:
            latex_content += "Lower bound constraint:\n"
            latex_content += r"\begin{align}" + "\n"
            latex_content += f"& \\text{{Any value}} \\geq {latex(eliminated['max_expression'])}\n"
            latex_content += r"\end{align}" + "\n\n"
        elif eliminated['min_expression'] is not None:
            latex_content += "Upper bound constraint:\n"
            latex_content += r"\begin{align}" + "\n"
            latex_content += f"& \\text{{Any value}} \\leq {latex(eliminated['min_expression'])}\n"
            latex_content += r"\end{align}" + "\n\n"
        else:
            latex_content += "No constraints generated from elimination.\n\n"
        
        # Sub-step 4: All resulting inequalities (including unrelated ones)
        latex_content += f"\\subsection{{Step {step_num}.4: All Resulting Inequalities}}\n\n"
        latex_content += r"\begin{align}" + "\n"
        for i, (lhs, op, rhs) in enumerate(step['output_inequalities']):
            latex_content += f"& {latex(lhs)} {op} {latex(rhs)}"
            if i < len(step['output_inequalities']) - 1:
                latex_content += r" \\" + "\n"
            else:
                latex_content += "\n"
        latex_content += r"\end{align}" + "\n\n"
        
        return latex_content
    
    def _generate_latex_footer(self):
        """Generate LaTeX document footer."""
        return r"""
\section{Summary}

The sequential variable elimination process transforms the original system of inequalities 
into a new system where the specified variables have been eliminated. Each elimination 
step potentially increases the number of inequalities due to the expansion of min/max 
combinations, but removes one variable from consideration.

This approach is particularly useful for:
\begin{itemize}
\item Eliminating intermediate variables in optimization problems
\item Reducing dimensionality of constraint systems
\item Analyzing parameter dependencies in rational inequalities
\end{itemize}

\end{document}
"""


def solve_with_variable_elimination(inequalities, variables_to_eliminate, 
                                  use_sign_analysis=True, save_latex=True, 
                                  output_filename=None):
    """
    Solve a system of rational inequalities by eliminating variables sequentially.
    
    Args:
        inequalities: List of inequalities in supported formats
        variables_to_eliminate: List of variable names ['x1', 'x2', 'x3', ...]
        use_sign_analysis: Whether to use sign analysis optimization
        save_latex: Whether to save LaTeX output to file
        output_filename: Custom filename for output (optional)
        
    Returns:
        dict: Complete solution with steps and final inequalities
    """
    print("=" * 80)
    print("ENHANCED VARIABLE ELIMINATION SOLVER")
    print("=" * 80)
    print(f"Input: {len(inequalities)} inequalities")
    print(f"Variables to eliminate: {variables_to_eliminate}")
    print(f"Sign analysis: {'Enabled' if use_sign_analysis else 'Disabled'}")
    print()
    
    # Initialize solver
    solver = VariableEliminationSolver(use_sign_analysis=use_sign_analysis)
    
    # Solve the system
    result = solver.solve_with_variable_elimination(inequalities, variables_to_eliminate)
    
    # Generate LaTeX report
    if save_latex:
        latex_content = solver.generate_latex_report()
        
        # Generate filename if not provided
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"variable_elimination_{timestamp}"
        
        # Save to output_final folder for complete documentation
        output_final_dir = "output_final"
        os.makedirs(output_final_dir, exist_ok=True)
        
        final_latex_file = os.path.join(output_final_dir, f"{output_filename}_complete.tex")
        with open(final_latex_file, 'w') as f:
            f.write(latex_content)
        
        print(f"Complete LaTeX report saved to: {final_latex_file}")
        print()
        
        # Also save summary to standard output folder
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        text_file = os.path.join(output_dir, f"{output_filename}_summary.txt")
        with open(text_file, 'w') as f:
            f.write(_generate_text_summary(result))
        
        print(f"Text summary saved to: {text_file}")
        print()
    
    # Print summary
    _print_solution_summary(result)
    
    return result


def _print_solution_summary(result):
    """Print a summary of the solution to console."""
    print("SOLUTION SUMMARY")
    print("-" * 40)
    print(f"Total elimination steps: {result['total_steps']}")
    print(f"Final number of inequalities: {len(result['final_inequalities'])}")
    print()
    
    for step in result['steps']:
        if step['step_number'] == 0:
            print(f"Step {step['step_number']}: {step['description']}")
            print(f"  Initial inequalities: {len(step['input_inequalities'])}")
        else:
            print(f"Step {step['step_number']}: {step['description']}")
            print(f"  Variable eliminated: {step['variable_eliminated']}")
            print(f"  Input inequalities: {len(step['input_inequalities'])}")
            print(f"  Output inequalities: {len(step['output_inequalities'])}")
            
            min_max = step['min_max_expressions']
            print(f"  Lower bounds found: {len(min_max['lower_bounds'])}")
            print(f"  Upper bounds found: {len(min_max['upper_bounds'])}")
        print()


def _generate_text_summary(result):
    """Generate a text summary of the solution."""
    summary = []
    summary.append("VARIABLE ELIMINATION SOLVER - SUMMARY REPORT")
    summary.append("=" * 60)
    summary.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append(f"Total steps: {result['total_steps']}")
    summary.append(f"Final inequalities: {len(result['final_inequalities'])}")
    summary.append("")
    
    for step in result['steps']:
        summary.append(f"STEP {step['step_number']}: {step['description']}")
        summary.append("-" * 40)
        
        if step['step_number'] == 0:
            summary.append("Initial system:")
            for lhs, op, rhs in step['input_inequalities']:
                summary.append(f"  {lhs} {op} {rhs}")
        else:
            summary.append(f"Variable eliminated: {step['variable_eliminated']}")
            summary.append("")
            
            summary.append("Input inequalities:")
            for lhs, op, rhs in step['input_inequalities']:
                summary.append(f"  {lhs} {op} {rhs}")
            summary.append("")
            
            min_max = step['min_max_expressions']
            if min_max['lower_bounds']:
                summary.append("Lower bounds:")
                for bound in min_max['lower_bounds']:
                    summary.append(f"  {step['variable_eliminated']} > {bound['expression']}")
                summary.append("")
            
            if min_max['upper_bounds']:
                summary.append("Upper bounds:")
                for bound in min_max['upper_bounds']:
                    summary.append(f"  {step['variable_eliminated']} < {bound['expression']}")
                summary.append("")
            
            summary.append("Output inequalities:")
            for lhs, op, rhs in step['output_inequalities']:
                summary.append(f"  {lhs} {op} {rhs}")
        
        summary.append("")
    
    summary.append("FINAL SYSTEM:")
    summary.append("-" * 40)
    for lhs, op, rhs in result['final_inequalities']:
        summary.append(f"  {lhs} {op} {rhs}")
    
    return "\n".join(summary)
