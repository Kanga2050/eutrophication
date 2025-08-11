"""
LaTeX Document Generator for Hierarchical Case Elimination

Author: Simplified Rational Inequality Solver Team
Version: Pure Inequality System - No Constraint/Inequality Separation
"""
from sympy import latex, simplify
import re


class HierarchicalLatexGenerator:
        expr_str = re.sub(r'\begin\{equation\}', '', expr_str)
        expr_str = re.sub(r'\end\{equation\}', '', expr_str)Hierarchical Variable Elimination

This module provides comprehensive LaTeX document generation for the hierarchical
variable elimination system. It generates professional mathematical documentation
with step-by-step process explanation and hierarchical case structure.

Classes:
- HierarchicalLatexGenerator: Generates complete LaTeX documentation

Author: Simplified Rational Inequality Solver Team
Version: Pure Inequality System - No Constraint/Inequality Separation
"""
from sympy import latex, simplify
import re


class HierarchicalLatexGenerator:
    """Generates LaTeX documentation for hierarchical case structure"""
    
    def format_expr(self, expr):
        """Format mathematical expressions for LaTeX with proper cleanup"""
        if expr is None:
            return "\\text{None}"
        
        # Convert to string if it's a SymPy expression
        if hasattr(expr, 'latex'):
            latex_expr = latex(expr)
        else:
            latex_expr = str(expr)
        
        # Remove nested equation environments that cause LaTeX errors
        latex_expr = re.sub(r'\\begin\{equation\}', '', latex_expr)
        latex_expr = re.sub(r'\\end\{equation\}', '', latex_expr)
        
        # Clean up common formatting issues
        latex_expr = re.sub(r'\\left\\(', '(', latex_expr)
        latex_expr = re.sub(r'\\right\\)', ')', latex_expr)
        
        # Fix variable names with underscores (e.g., n_l -> n_{l})
        latex_expr = re.sub(r'([a-zA-Z]+)_([a-zA-Z0-9]+)', r'\1_{\2}', latex_expr)
        
        # Fix Greek letters - simple replacement for common ones
        latex_expr = latex_expr.replace('Gamma', '\\Gamma')
        latex_expr = latex_expr.replace('Delta', '\\Delta')
        latex_expr = latex_expr.replace('gamma', '\\gamma')
        latex_expr = latex_expr.replace('delta', '\\delta')
        
        # Clean up multiple spaces and formatting
        latex_expr = re.sub(r'\s+', ' ', latex_expr)
        latex_expr = latex_expr.strip()
        
        return latex_expr
    
    def format_inequality_operator(self, op):
        """Format inequality operators for LaTeX."""
        if op == '<=':
            return r'\leq'
        elif op == '>=':
            return r'\geq'
        elif op == '<':
            return '<'
        elif op == '>':
            return '>'
        else:
            return op
    
    def format_variable(self, var_str):
        """Format variable for LaTeX with proper subscripts and Greek letters."""
        import re
        
        # Handle special constants like Gamma, Delta, etc.
        var_str = str(var_str)
        
        # Greek letters
        if var_str == 'Gamma':
            return r'\Gamma'
        elif var_str == 'Delta':
            return r'\Delta'
        elif var_str == 'gamma':
            return r'\gamma'
        elif var_str == 'delta':
            return r'\delta'
        
        # Handle subscripted variables (n_l, a_u, etc.)
        if '_' in var_str:
            parts = var_str.split('_')
            if len(parts) == 2:
                base, subscript = parts
                return f"{base}_{{{subscript}}}"
        
        # Handle numbered variables (x1, x2, etc.)
        if re.match(r'^[a-zA-Z]\d+$', var_str):
            return re.sub(r'([a-zA-Z])(\d+)', r'\1_{\2}', var_str)
        
        return var_str
    
    def generate_hierarchical_latex(self, all_cases, variables_to_eliminate, original_inequalities):
        """Generate complete LaTeX with enhanced hierarchical case documentation"""
        latex_content = []
        
        # Enhanced document header
        latex_content.extend([
            "\\documentclass{article}",
            "\\usepackage{amsmath}",
            "\\usepackage{amssymb}",
            "\\usepackage{geometry}",
            "\\usepackage{enumitem}",
            "\\usepackage{array}",
            "\\usepackage{titlesec}",
            "\\usepackage{xcolor}",
            "\\geometry{margin=1in}",
            "",
            "% Custom section formatting for hierarchical cases",
            "\\titleformat{\\subsubsection}[runin]{\\normalfont\\bfseries}{\\thesubsubsection.}{1em}{}",
            "\\titleformat{\\paragraph}[runin]{\\normalfont\\bfseries}{\\theparagraph.}{1em}{}",
            "",
            "% Custom environments for mathematical steps",
            "\\newenvironment{stepdetail}",
            "  {\\begin{quote}\\small\\color{blue}}",
            "  {\\end{quote}}",
            "",
            "\\title{Complete 4-Step Variable Elimination Process: \\\\",
            "No Constraint/Inequality Separation - Pure Inequality System}",
            "\\author{Simplified Rational Inequality Solver}",
            "\\date{\\today}",
            "",
            "\\begin{document}",
            "\\maketitle",
            ""
        ])
        
        # Enhanced introduction
        latex_content.extend([
            "\\section{Overview}",
            "",
            "This document presents a complete 4-step variable elimination process where",
            "\\textbf{ALL results are treated as inequalities within cases}. There is",
            "\\textbf{no distinction between constraints and inequalities} - everything",
            "must be satisfied within each case.",
            "",
            "\\textbf{Key Principle:}",
            "\\begin{quote}",
            "\\textit{At the end, we can just say all the inequalities in one of the cases needs to be true.}",
            "\\end{quote}",
            "",
            "\\textbf{System Features:}",
            "\\begin{itemize}",
            "\\item No separation between constraints and inequalities",
            "\\item All results are inequalities within cases",
            "\\item Detailed 4-step process for each variable",
            "\\item Complete mathematical documentation",
            "\\item Hierarchical case structure",
            "\\end{itemize}",
            ""
        ])
        
        # Show enhanced original system
        latex_content.extend([
            "\\section{Initial System}",
            "",
            "Starting with the following system of inequalities involving:",
            "\\begin{itemize}",
            "\\item \\textbf{Variables}: $x_1, x_2, x_3, x_4, \\ldots$ (to be eliminated in order)",
            "\\item \\textbf{Constants}: $a, b, c, d, e, f, g, h, \\ldots$ (parameters)",
            "\\end{itemize}",
            "",
            "\\begin{align}"
        ])
        
        for i, ineq in enumerate(original_inequalities, 1):
            # Enhanced formatting for the original inequalities
            # Convert variable names (x1 -> x_1) and operators (<= -> \leq, >= -> \geq)
            formatted_ineq = ineq
            import re
            formatted_ineq = re.sub(r'x(\d+)', r'x_{\1}', formatted_ineq)
            formatted_ineq = formatted_ineq.replace('*', r' \cdot ')
            formatted_ineq = formatted_ineq.replace('>=', r'\geq')
            formatted_ineq = formatted_ineq.replace('<=', r'\leq')
            latex_content.append(f"& \\text{{({i})}} \\quad {formatted_ineq} \\\\")
        
        latex_content.extend([
            "\\end{align}",
            "",
            f"Variables to eliminate (in order): $\\{{{', '.join([self.format_variable(v) for v in variables_to_eliminate])}\\}}$",
            "",
            "\\textbf{Goal}: Eliminate all variables to obtain a system of inequalities",
            "involving only the constants $a, b, c, d, e, f, g, h, \\ldots$",
            ""
        ])
        
        # Document each case hierarchically with enhanced formatting
        root_cases = [case for case in all_cases if case.level == 0]
        
        for root_case in root_cases:
            latex_content.extend(self._generate_case_hierarchy_latex(root_case, variables_to_eliminate))
        
        # Enhanced final solution summary
        final_cases = [case for case in all_cases if not case.subcases]
        latex_content.extend([
            "\\section{Final Solution Summary}",
            "",
            f"After systematically eliminating all variables $\\{{{', '.join([self.format_variable(v) for v in variables_to_eliminate])}\\}}$",
            f"using the enhanced hierarchical 4-step process, we obtain the following",
            f"{len(final_cases)} final case(s), each representing a complete solution region:",
            ""
        ])
        
        for i, case in enumerate(final_cases, 1):
            latex_content.extend([
                f"\\subsection{{Final Case {i}: {case.name}}}",
                ""
            ])
            
            if not case.inequalities:
                latex_content.extend([
                    "This case has no inequalities and represents the region where the original",
                    "system is always satisfied (unconditionally feasible region).",
                    ""
                ])
            else:
                latex_content.extend([
                    "This case represents the solution region defined by:",
                    "\\begin{align}"
                ])
                
                for inequality in case.inequalities:
                    expr, op, rhs = inequality
                    formatted_expr = self.format_expr(expr)
                    formatted_rhs = self.format_expr(rhs)
                    formatted_op = self.format_inequality_operator(op)
                    latex_content.append(f"& {formatted_expr} {formatted_op} {formatted_rhs} \\\\")
                
                latex_content.extend([
                    "\\end{align}",
                    "",
                    "\\begin{stepdetail}",
                    f"\\textbf{{Interpretation}}: This final case represents all parameter values",
                    f"$(a, b, c, d, e, f, g, h, \\ldots)$ for which the original system has solutions.",
                    "\\end{stepdetail}",
                    ""
                ])
        
        # Enhanced conclusion
        latex_content.extend([
            "\\section{Conclusion}",
            "",
            "The complete 4-step variable elimination process with no constraint/inequality separation provides:",
            "\\begin{itemize}",
            "\\item \\textbf{Unified Treatment}: All results are inequalities within cases",
            "\\item \\textbf{Mathematical Clarity}: No artificial distinction between constraint types",
            "\\item \\textbf{Systematic Elimination}: Variables are eliminated in specified order",
            "\\item \\textbf{Hierarchical Organization}: Complex case structures are clearly organized",
            "\\item \\textbf{Simple Interpretation}: Final result requires all inequalities in one case to be true",
            "\\end{itemize}",
            "",
            f"This elimination process demonstrates that:",
            "\\begin{itemize}",
            "\\item All results are expressed as inequalities within cases",
            "\\item No distinction is made between constraints and inequalities",
            "\\item The final solution requires all inequalities in one of the cases to be true",
            "\\item The 4-step process systematically eliminates each variable",
            "\\end{itemize}",
            "",
            f"The final result characterizes the complete solution space through",
            f"{len(final_cases)} distinct case(s), where each case contains only inequalities",
            f"that must all be satisfied simultaneously.",
            ""
        ])
        
        latex_content.append("\\end{document}")
        return "\n".join(latex_content)
    
    def _generate_case_hierarchy_latex(self, case, variables_to_eliminate):
        """Generate LaTeX for a complete case hierarchy with detailed conditions"""
        latex_content = []
        
        # Generate case header with conditions
        case_header_with_conditions = self._generate_case_header_with_conditions(case)
        
        # Case header
        if case.level == 0:
            latex_content.extend([
                f"\\section{{{case_header_with_conditions}}}",
                ""
            ])
        elif case.level == 1:
            latex_content.extend([
                f"\\subsection{{{case_header_with_conditions}}}",
                ""
            ])
        elif case.level == 2:
            latex_content.extend([
                f"\\subsubsection{{{case_header_with_conditions}}}",
                ""
            ])
        else:
            latex_content.extend([
                f"\\paragraph{{{case_header_with_conditions}}}",
                ""
            ])
        
        # Show case inequalities only for top-level cases to avoid repetition
        if case.level == 0 and case.inequalities:
            latex_content.extend([
                f"Inequalities for {case.name}:",
                "\\begin{align}"
            ])
            
            for inequality in case.inequalities:
                expr, op, rhs = inequality
                formatted_expr = self.format_expr(expr)
                formatted_rhs = self.format_expr(rhs)
                formatted_op = self.format_inequality_operator(op)
                latex_content.append(f"& {formatted_expr} {formatted_op} {formatted_rhs} \\\\")
            
            latex_content.extend([
                "\\end{align}",
                ""
            ])
        
        # Show elimination steps for this case with clean process
        if case.elimination_steps:
            for i, step in enumerate(case.elimination_steps):
                variable = step['variable']
                formatted_variable = self.format_variable(variable)
                latex_content.extend([
                    f"\\textbf{{Elimination of variable ${formatted_variable}$ in {case.name}:}}",
                    ""
                ])
                
                # Add step-by-step process showing only key changes, not all inequalities
                latex_content.extend(self._format_step_details_concise(step, variable))
        
        # Document subcases recursively
        for subcase in case.subcases:
            latex_content.extend(self._generate_case_hierarchy_latex(subcase, variables_to_eliminate))
        
        return latex_content
    
    def _generate_case_header_with_conditions(self, case):
        """Generate case header that includes the specific conditions for that case"""
        header = case.name
        
        if case.inequalities:
            # Extract key conditions from the case inequalities
            conditions = []
            for expr, op, rhs in case.inequalities:
                if rhs == 0:
                    # Simplified condition format
                    simplified_expr = self.format_expr(expr)
                    formatted_op = self.format_inequality_operator(op)
                    conditions.append(f"${simplified_expr} {formatted_op} 0$")
                else:
                    simplified_expr = self.format_expr(expr)
                    simplified_rhs = self.format_expr(rhs)
                    formatted_op = self.format_inequality_operator(op)
                    conditions.append(f"${simplified_expr} {formatted_op} {simplified_rhs}$")
            
            if conditions and len(conditions) <= 3:  # Only show if not too many conditions
                conditions_str = ", ".join(conditions)
                header = f"{case.name}: {conditions_str}"
        
        return header
    
    def _format_step_details(self, step, variable):
        """Format step-by-step process showing inequalities after each step"""
        latex_content = []
        
        # Format variable for LaTeX
        formatted_variable = self.format_variable(variable)
        
        # Step 1: Show inequalities after isolating variable
        if 'step1' in step and step['step1'].get('step1_inequalities'):
            step1_inequalities = step['step1']['step1_inequalities']
            latex_content.extend([
                f"\\textbf{{Step 1}}: Inequalities after isolating ${formatted_variable}$:",
                "\\begin{align}"
            ])
            for i, ineq in enumerate(step1_inequalities, 1):
                if len(ineq) == 3:
                    lhs, op, rhs = ineq
                    formatted_lhs = self.format_expr(lhs)
                    formatted_rhs = self.format_expr(rhs)
                    formatted_op = self.format_inequality_operator(op)
                    latex_content.append(f"& {formatted_lhs} {formatted_op} {formatted_rhs} \\\\")
            latex_content.extend([
                "\\end{align}",
                ""
            ])
        
        # Step 2: Show inequalities after combining to min/max form
        if 'step2' in step:
            step2_data = step['step2']
            latex_content.extend([
                f"\\textbf{{Step 2}}: Inequalities after combining to min/max form:",
                "\\begin{align}"
            ])
            
            # Show non-involving variables first
            if step2_data.get('step2_inequalities'):
                step2_inequalities = step2_data['step2_inequalities']
                minmax_inequalities = step2_data.get('minmax_inequalities', [])
                
                # Separate min/max inequalities from regular ones
                regular_inequalities = []
                for ineq in step2_inequalities:
                    if ineq not in minmax_inequalities:
                        regular_inequalities.append(ineq)
                
                # Show regular inequalities first (those not involving the variable)
                for ineq in regular_inequalities:
                    if len(ineq) == 3:
                        lhs, op, rhs = ineq
                        formatted_lhs = self.format_expr(lhs)
                        formatted_rhs = self.format_expr(rhs)
                        formatted_op = self.format_inequality_operator(op)
                        latex_content.append(f"& {formatted_lhs} {formatted_op} {formatted_rhs} \\\\")
                
                # Show the min/max form if it exists
                if step2_data.get('minmax_form') and step2_data.get('lower_bounds') and step2_data.get('upper_bounds'):
                    # Get the actual bound expressions
                    lower_bounds = step2_data['lower_bounds']
                    upper_bounds = step2_data['upper_bounds']
                    
                    # Format the expressions properly
                    if len(lower_bounds) == 1 and len(upper_bounds) == 1:
                        lower_expr = self.format_expr(lower_bounds[0][0])
                        upper_expr = self.format_expr(upper_bounds[0][0])
                        latex_content.append(f"& \\max\\{{{lower_expr}\\}} \\leq {formatted_variable} \\leq \\min\\{{{upper_expr}\\}} \\\\")
                    elif len(lower_bounds) > 0 and len(upper_bounds) > 0:
                        lower_exprs = [self.format_expr(expr) for expr, op in lower_bounds]
                        upper_exprs = [self.format_expr(expr) for expr, op in upper_bounds]
                        lower_max = "\\max\\{" + ", ".join(lower_exprs) + "\\}"
                        upper_min = "\\min\\{" + ", ".join(upper_exprs) + "\\}"
                        latex_content.append(f"& {lower_max} \\leq {formatted_variable} \\leq {upper_min} \\\\")
                    elif len(lower_bounds) > 0:
                        # Only lower bounds
                        lower_exprs = [self.format_expr(expr) for expr, op in lower_bounds]
                        if len(lower_exprs) == 1:
                            latex_content.append(f"& {formatted_variable} \\geq {lower_exprs[0]} \\\\")
                        else:
                            lower_max = "\\max\\{" + ", ".join(lower_exprs) + "\\}"
                            latex_content.append(f"& {formatted_variable} \\geq {lower_max} \\\\")
                    elif len(upper_bounds) > 0:
                        # Only upper bounds
                        upper_exprs = [self.format_expr(expr) for expr, op in upper_bounds]
                        if len(upper_exprs) == 1:
                            latex_content.append(f"& {formatted_variable} \\leq {upper_exprs[0]} \\\\")
                        else:
                            upper_min = "\\min\\{" + ", ".join(upper_exprs) + "\\}"
                            latex_content.append(f"& {formatted_variable} \\leq {upper_min} \\\\")
            
            latex_content.extend([
                "\\end{align}",
                ""
            ])
        
        # Step 3: Show inequalities after removing variable
        if 'step3' in step and step['step3'].get('step3_inequalities'):
            step3_inequalities = step['step3']['step3_inequalities']
            latex_content.extend([
                f"\\textbf{{Step 3}}: Inequalities after removing ${formatted_variable}$:",
                "\\begin{align}"
            ])
            for i, ineq in enumerate(step3_inequalities, 1):
                if len(ineq) == 3:
                    lhs, op, rhs = ineq
                    formatted_lhs = self.format_expr(lhs)
                    formatted_rhs = self.format_expr(rhs)
                    formatted_op = self.format_inequality_operator(op)
                    latex_content.append(f"& {formatted_lhs} {formatted_op} {formatted_rhs} \\\\")
            latex_content.extend([
                "\\end{align}",
                ""
            ])
        
        # Step 4: Reference to subcases (inequalities shown in subcases)
        if 'step4' in step:
            latex_content.extend([
                f"\\textbf{{Step 4}}: Expanded into {step['step4'].get('subcases', 0)} subcase(s). Inequalities for each subcase are shown below.",
                ""
            ])
        
        return latex_content

    def _format_step_details_concise(self, step, variable):
        """Format 4-step process showing only resulting inequalities after each step"""
        latex_content = []
        
        # Format variable for LaTeX
        formatted_variable = self.format_variable(variable)
        
        # Step 1: Show isolated bounds
        if 'step1' in step:
            step1_data = step['step1']
            latex_content.extend([
                f"\\textbf{{Step 1}}: Isolated bounds for ${formatted_variable}$",
                "\\begin{align}"
            ])
            
            # Get isolated inequalities and not involving inequalities
            isolated_inequalities = step1_data.get('isolated_inequalities', [])
            not_involving = step1_data.get('not_involving_var', [])
            
            # Show isolated bounds for the variable
            for var_expr, op, bound_expr in isolated_inequalities:
                formatted_bound = self.format_expr(bound_expr)
                formatted_op = self.format_inequality_operator(op)
                latex_content.append(f"& {formatted_variable} {formatted_op} {formatted_bound} \\\\")
            
            # Show inequalities not involving the variable
            for lhs, op, rhs in not_involving:
                formatted_lhs = self.format_expr(lhs)
                formatted_rhs = self.format_expr(rhs)
                formatted_op = self.format_inequality_operator(op)
                latex_content.append(f"& {formatted_lhs} {formatted_op} {formatted_rhs} \\\\")
            
            latex_content.extend([
                "\\end{align}",
                ""
            ])
        
        # Step 2: Show min/max form with preserved inequalities
        if 'step2' in step:
            step2_data = step['step2']
            latex_content.extend([
                f"\\textbf{{Step 2}}: Combined bounds for ${formatted_variable}$",
                "\\begin{align}"
            ])
            
            lower_bounds = step2_data.get('lower_bounds', [])
            upper_bounds = step2_data.get('upper_bounds', [])
            not_involving = step2_data.get('not_involving_var', [])
            
            # Show combined constraint
            if lower_bounds and upper_bounds:
                if len(lower_bounds) == 1 and len(upper_bounds) == 1:
                    lower_expr = self.format_expr(lower_bounds[0][0])
                    upper_expr = self.format_expr(upper_bounds[0][0])
                    latex_content.append(f"& {lower_expr} \\leq {formatted_variable} \\leq {upper_expr} \\\\")
                else:
                    lower_exprs = [self.format_expr(expr) for expr, op in lower_bounds]
                    upper_exprs = [self.format_expr(expr) for expr, op in upper_bounds]
                    lower_max = "\\max\\{" + ", ".join(lower_exprs) + "\\}"
                    upper_min = "\\min\\{" + ", ".join(upper_exprs) + "\\}"
                    latex_content.append(f"& {lower_max} \\leq {formatted_variable} \\leq {upper_min} \\\\")
            elif lower_bounds:
                lower_exprs = [self.format_expr(expr) for expr, op in lower_bounds]
                if len(lower_exprs) == 1:
                    latex_content.append(f"& {formatted_variable} \\geq {lower_exprs[0]} \\\\")
                else:
                    lower_max = "\\max\\{" + ", ".join(lower_exprs) + "\\}"
                    latex_content.append(f"& {formatted_variable} \\geq {lower_max} \\\\")
            elif upper_bounds:
                upper_exprs = [self.format_expr(expr) for expr, op in upper_bounds]
                if len(upper_exprs) == 1:
                    latex_content.append(f"& {formatted_variable} \\leq {upper_exprs[0]} \\\\")
                else:
                    upper_min = "\\min\\{" + ", ".join(upper_exprs) + "\\}"
                    latex_content.append(f"& {formatted_variable} \\leq {upper_min} \\\\")
            
            # Show preserved inequalities not involving the variable
            for lhs, op, rhs in not_involving:
                formatted_lhs = self.format_expr(lhs)
                formatted_rhs = self.format_expr(rhs)
                formatted_op = self.format_inequality_operator(op)
                latex_content.append(f"& {formatted_lhs} {formatted_op} {formatted_rhs} \\\\")
            
            latex_content.extend([
                "\\end{align}",
                ""
            ])
        
        # Step 3: Show elimination constraints and remaining inequalities
        if 'step3' in step:
            step3_data = step['step3']
            latex_content.extend([
                f"\\textbf{{Step 3}}: After eliminating ${formatted_variable}$",
                "\\begin{align}"
            ])
            
            # Show all constraints after elimination
            all_constraints = step3_data.get('all_constraints', [])
            for lhs, op, rhs in all_constraints:
                formatted_lhs = self.format_expr(lhs)
                formatted_rhs = self.format_expr(rhs)
                formatted_op = self.format_inequality_operator(op)
                latex_content.append(f"& {formatted_lhs} {formatted_op} {formatted_rhs} \\\\")
            
            latex_content.extend([
                "\\end{align}",
                ""
            ])
        
        # Step 4: Note about case expansion
        if 'step4' in step:
            latex_content.extend([
                f"\\textbf{{Step 4}}: Generated subcases for next variable elimination",
                ""
            ])
        
        return latex_content
