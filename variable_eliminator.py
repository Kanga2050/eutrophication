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
            
            # Step 1: Isolate variable and create case-based constraints
            case_result = self._isolate_variable(current_inequalities, var_symbol)
            
            # Step 2: Create elimination constraints from cases
            eliminated_result = self._eliminate_variable_from_minmax(case_result, var_symbol)
            
            # Step 3: Expand case combinations into new inequalities
            new_inequalities = self._expand_minmax_combinations(eliminated_result)
            
            # Record this elimination step
            step = {
                'step_number': i + 1,
                'description': f'Eliminate Variable {var_name}',
                'variable_eliminated': var_name,
                'input_inequalities': current_inequalities,
                'case_based_constraints': case_result,
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
        Isolate a variable from the inequality system, creating case-based bounds.
        
        Args:
            inequalities: List of (lhs, op, rhs) tuples
            variable: Variable symbol to isolate
            
        Returns:
            dict: Case-based bounds and constraints
        """
        constraints_without_var = []
        case_based_constraints = []
        
        for lhs, op, rhs in inequalities:
            expr = simplify(lhs - rhs)
            
            if variable not in expr.free_symbols:
                # Constraint doesn't involve the variable
                constraints_without_var.append((lhs, op, rhs))
            else:
                # Solve for the variable bounds
                try:
                    # Use the existing solver to get bounds with full case information
                    case_outputs = solve_rational_ineq_full(expr, variable, op, self.use_sign_analysis)
                    
                    # Parse cases and extract both bounds and conditions
                    for case_output in case_outputs:
                        case_info = self._parse_case_with_conditions(case_output, variable)
                        if case_info:
                            case_info['original_inequality'] = (lhs, op, rhs)
                            case_based_constraints.append(case_info)
                        
                except Exception as e:
                    print(f"Warning: Could not process inequality {expr} {op} 0: {e}")
                    print(f"  Skipping constraint {lhs} {op} {rhs} - contains {variable} but cannot be isolated")
        
        return {
            'constraints_without_var': constraints_without_var,
            'case_based_constraints': case_based_constraints,
            'variable': variable
        }
    
    def _parse_case_with_conditions(self, case_output, variable):
        """
        Parse a single case output to extract bounds and conditions.
        
        Args:
            case_output: Single case output string from solver
            variable: Variable being isolated
            
        Returns:
            dict: Case information with bounds and conditions
        """
        import re
        
        lines = case_output.strip().split('\n')
        if not lines:
            return None
            
        # Extract case description
        case_description = lines[0].strip()
        
        # Extract bounds on the target variable
        bounds = []
        conditions = []
        
        for line in lines[1:]:
            line = line.strip()
            
            # Look for "Linear condition: x >= expr" or "Linear condition: x < expr"
            if 'Linear condition:' in line:
                # Extract the condition part after "Linear condition:"
                condition_part = line.split('Linear condition:')[1].strip()
                
                # Look for patterns like "x >= 0", "x < 0", etc.
                var_match = re.search(r'x\s*([<>]=?)\s*(.+)', condition_part)
                if var_match:
                    op, expr_str = var_match.groups()
                    try:
                        expr = simplify(expr_str.strip())
                        direction = '<' if '<' in op else '>'
                        bounds.append((expr, direction))
                    except:
                        continue
            
            # Look for conditions like "and (expr) > 0"
            elif line.startswith('and'):
                # Extract condition after 'and'
                and_match = re.search(r'and\s*\(([^)]+)\)\s*([<>]=?)\s*(.+)', line)
                if and_match:
                    cond_expr, cond_op, cond_rhs = and_match.groups()
                    try:
                        cond_lhs = simplify(cond_expr.strip())
                        cond_rhs = simplify(cond_rhs.strip())
                        conditions.append((cond_lhs, cond_op, cond_rhs))
                    except:
                        continue
        
        if bounds:
            return {
                'case_description': case_description,
                'bounds': bounds,
                'conditions': conditions
            }
        
        return None
    
    def _eliminate_variable_from_minmax(self, case_result, variable):
        """
        Create elimination constraints from case-based bounds.
        
        Args:
            case_result: Result from _isolate_variable with case-based constraints
            variable: Variable being eliminated
            
        Returns:
            dict: Elimination constraints with their conditions
        """
        constraints_without_var = case_result['constraints_without_var']
        case_constraints = case_result['case_based_constraints']
        
        # Separate cases by bounds type
        lower_bound_cases = []
        upper_bound_cases = []
        
        for case in case_constraints:
            for bound_expr, direction in case['bounds']:
                case_info = {
                    'expression': bound_expr,
                    'direction': direction,
                    'conditions': case['conditions'],
                    'case_description': case['case_description'],
                    'original_inequality': case['original_inequality']
                }
                
                if direction == '>':
                    lower_bound_cases.append(case_info)
                else:  # direction == '<'
                    upper_bound_cases.append(case_info)
        
        return {
            'constraints_without_var': constraints_without_var,
            'lower_bound_cases': lower_bound_cases,
            'upper_bound_cases': upper_bound_cases,
            'variable_eliminated': variable
        }
    
    def _expand_minmax_combinations(self, eliminated_result):
        """
        Create elimination constraints from case combinations.
        
        Args:
            eliminated_result: Result from _eliminate_variable_from_minmax
            
        Returns:
            List of new inequality tuples with case information
        """
        constraints_without_var = eliminated_result['constraints_without_var']
        lower_bound_cases = eliminated_result['lower_bound_cases']
        upper_bound_cases = eliminated_result['upper_bound_cases']
        
        new_inequalities = list(constraints_without_var)  # Start with constraints without the variable
        
        print(f"Found {len(lower_bound_cases)} lower bound cases and {len(upper_bound_cases)} upper bound cases")
        
        # For each valid combination of lower and upper bounds, create elimination constraints
        if lower_bound_cases and upper_bound_cases:
            for lower_case in lower_bound_cases:
                for upper_case in upper_bound_cases:
                    # Filter conditions first
                    lower_valid_conditions = self._filter_trivial_conditions(lower_case['conditions'])
                    upper_valid_conditions = self._filter_trivial_conditions(upper_case['conditions'])
                    
                    # Skip impossible cases
                    if lower_valid_conditions is None or upper_valid_conditions is None:
                        print(f"  Skipping impossible case combination")
                        continue
                    
                    # Check if the remaining conditions are compatible
                    if self._are_conditions_compatible(lower_valid_conditions, upper_valid_conditions):
                        # Create elimination constraint: lower_bound <= upper_bound
                        elimination_constraint = (lower_case['expression'], '<=', upper_case['expression'])
                        
                        # Combine valid conditions
                        all_valid_conditions = lower_valid_conditions + upper_valid_conditions
                        
                        # Add the elimination constraint
                        new_inequalities.append(elimination_constraint)
                        
                        # Add only non-trivial conditions as separate constraints
                        for cond_lhs, cond_op, cond_rhs in all_valid_conditions:
                            new_inequalities.append((cond_lhs, cond_op, cond_rhs))
                        
                        print(f"Created elimination constraint: {lower_case['expression']} <= {upper_case['expression']}")
                        if all_valid_conditions:
                            print(f"  With conditions: {[f'{lhs} {op} {rhs}' for lhs, op, rhs in all_valid_conditions]}")
                        else:
                            print(f"  No additional conditions needed")
        
        # If only lower bounds exist, add them with their conditions
        elif lower_bound_cases and not upper_bound_cases:
            for lower_case in lower_bound_cases:
                valid_conditions = self._filter_trivial_conditions(lower_case['conditions'])
                if valid_conditions is not None:  # Only if case is possible
                    # Add the conditions as constraints  
                    for cond_lhs, cond_op, cond_rhs in valid_conditions:
                        new_inequalities.append((cond_lhs, cond_op, cond_rhs))
                    print(f"Added conditions for lower bound case: {lower_case['expression']}")
        
        # If only upper bounds exist, add them with their conditions
        elif upper_bound_cases and not lower_bound_cases:
            for upper_case in upper_bound_cases:
                valid_conditions = self._filter_trivial_conditions(upper_case['conditions'])
                if valid_conditions is not None:  # Only if case is possible
                    # Add the conditions as constraints
                    for cond_lhs, cond_op, cond_rhs in valid_conditions:
                        new_inequalities.append((cond_lhs, cond_op, cond_rhs))
                    print(f"Added conditions for upper bound case: {upper_case['expression']}")
        
        return new_inequalities
    
    def _filter_trivial_conditions(self, conditions):
        """Filter out trivial conditions like 1 > 0 (always true) or 1 < 0 (always false)."""
        valid_conditions = []
        
        for cond_lhs, cond_op, cond_rhs in conditions:
            try:
                from sympy import sympify
                lhs_val = sympify(cond_lhs)
                rhs_val = sympify(cond_rhs)
                
                # If both sides are constants, evaluate
                if lhs_val.is_number and rhs_val.is_number:
                    # Convert to float for comparison
                    lhs_float = float(lhs_val)
                    rhs_float = float(rhs_val)
                    
                    if cond_op == '>':
                        is_true = lhs_float > rhs_float
                    elif cond_op == '<':
                        is_true = lhs_float < rhs_float
                    elif cond_op == '>=':
                        is_true = lhs_float >= rhs_float
                    elif cond_op == '<=':
                        is_true = lhs_float <= rhs_float
                    elif cond_op == '==':
                        is_true = abs(lhs_float - rhs_float) < 1e-10
                    else:
                        is_true = None
                    
                    if is_true is True:
                        # Always true condition - skip it
                        print(f"    Skipping always-true condition: {cond_lhs} {cond_op} {cond_rhs}")
                        continue
                    elif is_true is False:
                        # Always false condition - this case is impossible
                        print(f"    Found impossible condition {cond_lhs} {cond_op} {cond_rhs} - case is invalid")
                        return None  # Return None to indicate impossible case
                
                # Keep non-trivial conditions
                valid_conditions.append((cond_lhs, cond_op, cond_rhs))
                
            except:
                # If we can't evaluate, keep the condition
                valid_conditions.append((cond_lhs, cond_op, cond_rhs))
        
        return valid_conditions
    
    def _are_conditions_compatible(self, conditions1, conditions2):
        """
        Check if two sets of conditions are compatible (don't contradict each other).
        
        Also filters out trivial conditions like 1 > 0 (always true) or 1 < 0 (always false).
        """
        # Combine all conditions
        all_conditions = conditions1 + conditions2
        
        # Filter and check conditions
        valid_conditions = []
        
        for cond_lhs, cond_op, cond_rhs in all_conditions:
            # Check for trivial conditions
            try:
                from sympy import sympify
                lhs_val = sympify(cond_lhs)
                rhs_val = sympify(cond_rhs)
                
                # If both sides are constants, evaluate
                if lhs_val.is_number and rhs_val.is_number:
                    if cond_op == '>':
                        is_true = lhs_val > rhs_val
                    elif cond_op == '<':
                        is_true = lhs_val < rhs_val
                    elif cond_op == '>=':
                        is_true = lhs_val >= rhs_val
                    elif cond_op == '<=':
                        is_true = lhs_val <= rhs_val
                    elif cond_op == '==':
                        is_true = lhs_val == rhs_val
                    else:
                        is_true = None
                    
                    if is_true is False:
                        # This condition is always false, so the combination is impossible
                        return False
                    elif is_true is True:
                        # This condition is always true, so we can ignore it
                        continue
                
                # Keep non-trivial conditions
                valid_conditions.append((cond_lhs, cond_op, cond_rhs))
                
            except:
                # If we can't evaluate, keep the condition
                valid_conditions.append((cond_lhs, cond_op, cond_rhs))
        
        # For now, assume remaining conditions are compatible
        # A more sophisticated check would look for contradictions like x > 0 and x < 0
        return True
    
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

\title{Sequential Variable Elimination for Rational Inequalities with Case Analysis}
\author{Enhanced Rational Inequality Solver}
\date{\today}

\begin{document}
\maketitle

\section{Introduction}

This document shows the step-by-step elimination of variables from a system of rational inequalities 
using comprehensive case analysis. Each inequality is solved by isolating the target variable 
and analyzing all possible cases that arise from sign conditions and domain constraints.

For each variable elimination, we show four sub-steps:
\begin{enumerate}
\item Original inequalities involving the variable
\item Min/Max expressions after isolation (with detailed case-by-case analysis)
\item Min/Max expressions after variable elimination  
\item Final expanded inequalities
\end{enumerate}

The case analysis shows how each original inequality is decomposed into multiple cases based on:
\begin{itemize}
\item Sign analysis of expressions in denominators
\item Domain constraints from square roots and other functions
\item Conditional bounds that depend on parameter values
\end{itemize}

"""

    def _generate_step_latex(self, step):
        """Generate LaTeX for a single elimination step."""
        if step['step_number'] == 0:
            return self._generate_initial_system_latex(step)
        else:
            return self._generate_elimination_step_latex(step)
    
    def _generate_initial_system_latex(self, step):
        """Generate LaTeX for the initial system with large brackets and ∧ symbols."""
        latex_content = r"\section{Initial System}" + "\n\n"
        latex_content += r"Starting with the following system of inequalities:" + "\n\n"
        
        latex_content += r"\left\{" + "\n"
        latex_content += r"\begin{aligned}" + "\n"
        
        for i, (lhs, op, rhs) in enumerate(step['input_inequalities']):
            latex_content += f"& {latex(lhs)} {op} {latex(rhs)}"
            if i < len(step['input_inequalities']) - 1:
                latex_content += r" \\" + "\n"
                latex_content += r"& \wedge \\" + "\n"  # ∧ symbol for "and"
            else:
                latex_content += "\n"
        
        latex_content += r"\end{aligned}" + "\n"
        latex_content += r"\right\}" + "\n\n"
        
        return latex_content
    
    def _generate_elimination_step_latex(self, step):
        """Generate LaTeX for a variable elimination step with large brackets and iff arrows."""
        var_name = step['variable_eliminated']
        step_num = step['step_number']
        
        latex_content = f"\\section{{Step {step_num}: Eliminate Variable ${var_name}$}}\n\n"
        
        # Sub-step 1: Input inequalities with large brackets and ∧ symbols
        latex_content += f"\\subsection{{Step {step_num}.1: Input Inequalities}}\n\n"
        
        # All inequalities in large brackets with ∧ separators
        all_ineqs = step['input_inequalities']
        
        latex_content += r"\left\{" + "\n"
        latex_content += r"\begin{aligned}" + "\n"
        
        for i, (lhs, op, rhs) in enumerate(all_ineqs):
            latex_content += f"& {latex(lhs)} {op} {latex(rhs)}"
            if i < len(all_ineqs) - 1:
                latex_content += r" \\" + "\n"
                latex_content += r"& \wedge \\" + "\n"  # ∧ symbol for "and"
            else:
                latex_content += "\n"
        
        latex_content += r"\end{aligned}" + "\n"
        latex_content += r"\right\}" + "\n\n"
        
        # Sub-step 2: Case-based bounds analysis
        latex_content += f"\\subsection{{Step {step_num}.2: Case-Based Bounds for ${var_name}$}}\n\n"
        case_result = step['case_based_constraints']
        
        if case_result['case_based_constraints']:
            latex_content += "\\textbf{Case Analysis:}\n\n"
            
            # Group cases by type
            lower_cases = []
            upper_cases = []
            
            for case in case_result['case_based_constraints']:
                for bound_expr, direction in case['bounds']:
                    case_info = {
                        'expression': bound_expr,
                        'direction': direction,
                        'conditions': case['conditions'],
                        'case_description': case['case_description'],
                        'original_inequality': case['original_inequality']
                    }
                    
                    if direction == '>':
                        lower_cases.append(case_info)
                    else:
                        upper_cases.append(case_info)
            
            # Show lower bounds with their cases and conditions
            if lower_cases:
                latex_content += "\\textbf{Lower Bounds:}\n"
                for i, case in enumerate(lower_cases):
                    latex_content += f"\\begin{{itemize}}\n"
                    latex_content += f"\\item Case {i+1}: {case['case_description']}\n"
                    latex_content += f"      Original inequality: ${latex(case['original_inequality'][0])} {case['original_inequality'][1]} {latex(case['original_inequality'][2])}$\n"
                    latex_content += f"      Result: ${var_name} {case['direction']} {latex(case['expression'])}$\n"
                    
                    # Add conditions if any
                    if case['conditions']:
                        latex_content += "      Conditions:\n"
                        for cond_lhs, cond_op, cond_rhs in case['conditions']:
                            latex_content += f"      \\quad ${latex(cond_lhs)} {cond_op} {latex(cond_rhs)}$\n"
                    
                    latex_content += f"\\end{{itemize}}\n"
                latex_content += "\n"
            
            # Show upper bounds with their cases and conditions
            if upper_cases:
                latex_content += "\\textbf{Upper Bounds:}\n"
                for i, case in enumerate(upper_cases):
                    latex_content += f"\\begin{{itemize}}\n"
                    latex_content += f"\\item Case {i+1}: {case['case_description']}\n"
                    latex_content += f"      Original inequality: ${latex(case['original_inequality'][0])} {case['original_inequality'][1]} {latex(case['original_inequality'][2])}$\n"
                    latex_content += f"      Result: ${var_name} {case['direction']} {latex(case['expression'])}$\n"
                    
                    # Add conditions if any
                    if case['conditions']:
                        latex_content += "      Conditions:\n"
                        for cond_lhs, cond_op, cond_rhs in case['conditions']:
                            latex_content += f"      \\quad ${latex(cond_lhs)} {cond_op} {latex(cond_rhs)}$\n"
                    
                    latex_content += f"\\end{{itemize}}\n"
                latex_content += "\n"
        else:
            latex_content += "No case-based bounds found for this variable.\n\n"
        
        # Sub-step 3: Constraint after elimination
        latex_content += f"\\subsection{{Step {step_num}.3: Elimination Constraints}}\n\n"
        eliminated = step['eliminated_expressions']
        
        # Show how cases combine to create elimination constraints
        if eliminated['lower_bound_cases'] and eliminated['upper_bound_cases']:
            latex_content += "\\textbf{Case Combinations for Elimination:}\n\n"
            latex_content += "For the variable to be eliminable, each lower bound case must be compatible with each upper bound case.\n\n"
            
            for i, lower_case in enumerate(eliminated['lower_bound_cases']):
                for j, upper_case in enumerate(eliminated['upper_bound_cases']):
                    latex_content += f"\\textbf{{Combination {i+1},{j+1}:}}\n"
                    latex_content += f"Lower bound: ${latex(lower_case['expression'])}$ (from {lower_case['case_description']})\n"
                    latex_content += f"Upper bound: ${latex(upper_case['expression'])}$ (from {upper_case['case_description']})\n"
                    latex_content += f"Elimination constraint: ${latex(lower_case['expression'])} \\leq {latex(upper_case['expression'])}$\n"
                    
                    # Show conditions
                    all_conditions = lower_case['conditions'] + upper_case['conditions']
                    if all_conditions:
                        latex_content += "Required conditions:\n"
                        for cond_lhs, cond_op, cond_rhs in all_conditions:
                            latex_content += f"\\quad ${latex(cond_lhs)} {cond_op} {latex(cond_rhs)}$\n"
                    latex_content += "\n"
                    
        elif eliminated['lower_bound_cases']:
            latex_content += "\\textbf{Only Lower Bounds:}\n"
            latex_content += "Variable has only lower bounds, so elimination adds the required conditions.\n\n"
            
        elif eliminated['upper_bound_cases']:
            latex_content += "\\textbf{Only Upper Bounds:}\n"
            latex_content += "Variable has only upper bounds, so elimination adds the required conditions.\n\n"
        else:
            latex_content += "No elimination constraints generated.\n\n"
        
        # Sub-step 4: Final system with large brackets
        latex_content += f"\\subsection{{Step {step_num}.4: All Resulting Inequalities}}\n\n"
        
        latex_content += r"\left\{" + "\n"
        latex_content += r"\begin{aligned}" + "\n"
        
        for i, (lhs, op, rhs) in enumerate(step['output_inequalities']):
            latex_content += f"& {latex(lhs)} {op} {latex(rhs)}"
            if i < len(step['output_inequalities']) - 1:
                latex_content += r" \\" + "\n"
                latex_content += r"& \wedge \\" + "\n"
            else:
                latex_content += "\n"
        
        latex_content += r"\end{aligned}" + "\n"
        latex_content += r"\right\}" + "\n\n"
        
        return latex_content
    
    def _generate_latex_footer(self):
        """Generate LaTeX document footer."""
        return r"""
\section{Summary}

The sequential variable elimination process with comprehensive case analysis transforms the original 
system of inequalities into a new system where the specified variables have been eliminated. 
Each elimination step shows the detailed case-by-case breakdown of how inequalities are solved, 
including all sign analysis conditions and domain constraints.

Key features of this approach:
\begin{itemize}
\item \textbf{Case Analysis}: Each inequality is solved by considering all possible cases
\item \textbf{Sign Analysis}: Denominators and critical expressions are analyzed for sign changes
\item \textbf{Domain Constraints}: Square roots and other functions impose additional constraints
\item \textbf{Min/Max Expansion}: Bounds are combined and expanded into multiple constraints
\end{itemize}

This approach is particularly useful for:
\begin{itemize}
\item Eliminating intermediate variables in optimization problems
\item Reducing dimensionality of constraint systems  
\item Analyzing parameter dependencies in rational inequalities
\item Understanding the complete solution structure through case analysis
\end{itemize}

The resulting system may have more inequalities than the original due to case expansion, 
but contains fewer variables and makes the constraint structure more explicit.

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
            
            case_result = step['case_based_constraints']
            if 'case_based_constraints' in case_result:
                # Count lower and upper bound cases
                lower_cases = sum(1 for case in case_result['case_based_constraints'] 
                                for bound_expr, direction in case['bounds'] if direction == '>')
                upper_cases = sum(1 for case in case_result['case_based_constraints'] 
                                for bound_expr, direction in case['bounds'] if direction == '<')
                print(f"  Lower bound cases found: {lower_cases}")
                print(f"  Upper bound cases found: {upper_cases}")
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
            
            case_result = step['case_based_constraints']
            if 'case_based_constraints' in case_result:
                summary.append("Case-based bounds:")
                for case in case_result['case_based_constraints']:
                    summary.append(f"  Case: {case['case_description']}")
                    for bound_expr, direction in case['bounds']:
                        summary.append(f"    {step['variable_eliminated']} {direction} {bound_expr}")
                    for cond_lhs, cond_op, cond_rhs in case['conditions']:
                        summary.append(f"    Condition: {cond_lhs} {cond_op} {cond_rhs}")
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
