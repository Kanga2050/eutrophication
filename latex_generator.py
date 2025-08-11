"""
LaTeX Document Generator for Hierarchical Case Elimination

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
        
        # Clean up common formatting issues - remove problematic patterns
        latex_expr = latex_expr.replace('\\left(', '(')
        latex_expr = latex_expr.replace('\\right)', ')')
        
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
        
        # Replace common Greek letters
        var_str = var_str.replace('Gamma', '\\Gamma')
        var_str = var_str.replace('Delta', '\\Delta')
        var_str = var_str.replace('gamma', '\\gamma')
        var_str = var_str.replace('delta', '\\delta')
        
        # Fix underscores to proper subscript notation
        var_str = re.sub(r'([a-zA-Z]+)_([a-zA-Z0-9]+)', r'\1_{\2}', var_str)
        
        return var_str
    
    def _format_step_details_comprehensive(self, step_details):
        """Format step details showing ALL inequalities at each step with proper case structure"""
        content = []
        
        for step_type, step_data in step_details.items():
            if step_type == "isolate":
                content.append(f"\\textbf{{Step 1: Isolate variable}}")
                
                # Show isolated inequalities (the new ones for this variable)
                if 'isolated_inequalities' in step_data and step_data['isolated_inequalities']:
                    content.append("\\textit{Inequalities involving the variable (after isolation):}")
                    content.append("\\begin{align}")
                    for ineq in step_data['isolated_inequalities']:
                        formatted_ineq = self.format_expr(ineq)
                        if formatted_ineq.strip():
                            content.append(f"& {formatted_ineq} \\\\")
                    content.append("\\end{align}")
                
                # Show non-involving inequalities (unchanged)
                if 'non_involving_inequalities' in step_data and step_data['non_involving_inequalities']:
                    content.append("\\textit{Inequalities not involving the variable (unchanged):}")
                    content.append("\\begin{align}")
                    for ineq in step_data['non_involving_inequalities']:
                        formatted_ineq = self.format_expr(ineq)
                        if formatted_ineq.strip():
                            content.append(f"& {formatted_ineq} \\\\")
                    content.append("\\end{align}")
                
                # Show complete system after Step 1
                if 'all_inequalities' in step_data and step_data['all_inequalities']:
                    content.append("\\textit{Complete system after Step 1:}")
                    content.append("\\begin{align}")
                    for ineq in step_data['all_inequalities']:
                        formatted_ineq = self.format_expr(ineq)
                        if formatted_ineq.strip():
                            content.append(f"& {formatted_ineq} \\\\")
                    content.append("\\end{align}")
                
            elif step_type == "combine":
                content.append(f"\\textbf{{Step 2: Combine bounds}}")
                content.append("\\textit{Combined constraint for the variable:}")
                content.append("\\begin{align}")
                if 'combined_constraint' in step_data:
                    formatted_constraint = self.format_expr(step_data['combined_constraint'])
                    if formatted_constraint.strip():
                        content.append(f"& {formatted_constraint} \\\\")
                content.append("\\end{align}")
                
                # Show all constraints after combining
                if 'all_constraints_after_combine' in step_data and step_data['all_constraints_after_combine']:
                    content.append("\\textit{Complete system after Step 2:}")
                    content.append("\\begin{align}")
                    for ineq in step_data['all_constraints_after_combine']:
                        if isinstance(ineq, tuple) and len(ineq) == 3:
                            formatted_ineq = self.format_expr(f"{ineq[0]} {ineq[1]} {ineq[2]}")
                        else:
                            formatted_ineq = self.format_expr(ineq)
                        if formatted_ineq.strip():
                            content.append(f"& {formatted_ineq} \\\\")
                    content.append("\\end{align}")
                
            elif step_type == "remove":
                content.append(f"\\textbf{{Step 3: Remove variable}}")
                
                # Show elimination constraints
                if 'elimination_constraints' in step_data and step_data['elimination_constraints']:
                    content.append("\\textit{Elimination constraints:}")
                    content.append("\\begin{align}")
                    for ineq in step_data['elimination_constraints']:
                        formatted_ineq = self.format_expr(ineq)
                        if formatted_ineq.strip():
                            content.append(f"& {formatted_ineq} \\\\")
                    content.append("\\end{align}")
                
                # Show complete system after removal
                if 'all_constraints_after_remove' in step_data and step_data['all_constraints_after_remove']:
                    content.append("\\textit{Complete system after removing variable:}")
                    content.append("\\begin{align}")
                    for ineq in step_data['all_constraints_after_remove']:
                        if isinstance(ineq, tuple) and len(ineq) == 3:
                            formatted_ineq = self.format_expr(f"{ineq[0]} {ineq[1]} {ineq[2]}")
                        else:
                            formatted_ineq = self.format_expr(ineq)
                        if formatted_ineq.strip():
                            content.append(f"& {formatted_ineq} \\\\")
                    content.append("\\end{align}")
                elif 'elimination_constraints' not in step_data or not step_data['elimination_constraints']:
                    content.append("\\textit{No elimination constraints generated (variable has no bounds).}")
                
            elif step_type == "expand":
                content.append(f"\\textbf{{Step 4: Expand cases}}")
                
                # Show each generated subcase with its complete constraint set
                if 'subcases' in step_data and step_data['subcases']:
                    for i, subcase in enumerate(step_data['subcases'], 1):
                        content.append(f"\\textit{{Case {i}: {subcase.get('case_name', f'Case {i}')}}}")
                        if 'inequalities' in subcase and subcase['inequalities']:
                            content.append("\\begin{align}")
                            for ineq in subcase['inequalities']:
                                if isinstance(ineq, tuple) and len(ineq) == 3:
                                    formatted_ineq = self.format_expr(f"{ineq[0]} {ineq[1]} {ineq[2]}")
                                else:
                                    formatted_ineq = self.format_expr(ineq)
                                if formatted_ineq.strip():
                                    content.append(f"& {formatted_ineq} \\\\")
                            content.append("\\end{align}")
                        else:
                            content.append("\\textit{No constraints (always satisfied)}")
                            content.append("\\begin{align}")
                            content.append("& \\text{Always satisfied} \\\\")
                            content.append("\\end{align}")
                else:
                    content.append("\\textit{No cases generated}")
                    content.append("\\begin{align}")
                    content.append("& \\text{No cases generated} \\\\")
                    content.append("\\end{align}")
        
        return "\n".join(content)

    def generate_elimination_latex(self, elimination_results, title="Variable Elimination Process"):
        """Generate complete LaTeX document for elimination results"""
        content = []
        
        # Document header
        content.append("\\documentclass{article}")
        content.append("\\usepackage{amsmath}")
        content.append("\\usepackage{amssymb}")
        content.append("\\usepackage{amsfonts}")
        content.append("\\usepackage{geometry}")
        content.append("\\geometry{margin=1in}")
        content.append("")
        content.append("\\begin{document}")
        content.append("")
        content.append(f"\\title{{{title}}}")
        content.append("\\author{Hierarchical Case Elimination System}")
        content.append("\\date{\\today}")
        content.append("\\maketitle")
        content.append("")
        
        # Add main content for each variable elimination
        for var, var_data in elimination_results.items():
            content.append(f"\\section{{Elimination of Variable ${self.format_variable(str(var))}$}}")
            content.append("")
            
            # Add step details
            if 'step_details' in var_data:
                step_content = self._format_step_details_comprehensive(var_data['step_details'])
                content.append(step_content)
                content.append("")
            
            content.append("\\newpage")
        
        # Document footer
        content.append("\\end{document}")
        
        return "\n".join(content)
