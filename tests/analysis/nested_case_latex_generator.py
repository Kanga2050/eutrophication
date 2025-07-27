#!/usr/bin/env python3

"""
CORRECTED Unified Main with Proper Nested Case Structure

This implements the correct LaTeX output where:
1. Case 1 is solved completely to the end
2. Then Case 2 is solved completely to the end  
3. Cases can be nested (Case 1.1, Case 1.2, etc.)
"""

import sys
sys.path.append('/workspaces/codespaces-blank')

from complete_tree_elimination_final import CompleteTreeBasedEliminator
from sympy import symbols, latex, simplify
from datetime import datetime
import os

class NestedCaseLatexGenerator:
    """
    Generates LaTeX with proper nested case structure.
    """
    
    def __init__(self):
        self.eliminator = CompleteTreeBasedEliminator()
        self.case_counter = 0
        
    def generate_nested_case_latex(self, inequalities, variables_to_eliminate):
        """
        Generate LaTeX with proper nested case structure.
        """
        
        # Start with single case containing all initial inequalities
        from input_processor import process_inequalities
        initial_system = process_inequalities(inequalities)
        
        # Generate the complete case tree
        case_tree = self._build_case_tree(initial_system, variables_to_eliminate)
        
        # Generate LaTeX document
        latex_content = self._generate_latex_document(inequalities, variables_to_eliminate, case_tree)
        
        return latex_content
    
    def _build_case_tree(self, initial_system, variables_to_eliminate):
        """
        Build the complete case tree structure.
        Returns nested structure showing all cases and subcases.
        """
        
        # Start with root case
        case_tree = {
            'case_id': 'Initial',
            'system': initial_system,
            'variable_eliminated': None,
            'subcases': []
        }
        
        # Process each variable elimination step
        current_level_cases = [case_tree]
        
        for step, variable in enumerate(variables_to_eliminate, 1):
            next_level_cases = []
            
            for case_node in current_level_cases:
                # Eliminate variable from this case's system
                subcases = self.eliminator.eliminate_variable_with_complete_cases(
                    case_node['system'], variable
                )
                
                # Create subcase nodes
                for subcase_idx, subcase_system in enumerate(subcases, 1):
                    subcase_node = {
                        'case_id': f"{case_node['case_id']}.{subcase_idx}",
                        'system': subcase_system,
                        'variable_eliminated': variable,
                        'subcases': []
                    }
                    case_node['subcases'].append(subcase_node)
                    next_level_cases.append(subcase_node)
            
            current_level_cases = next_level_cases
        
        return case_tree
    
    def _generate_latex_document(self, inequalities, variables_to_eliminate, case_tree):
        """
        Generate complete LaTeX document with nested case structure.
        """
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        latex_content = f"""\\documentclass{{article}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{geometry}}
\\usepackage{{enumitem}}
\\geometry{{margin=1in}}

\\title{{Variable Elimination with Nested Case Analysis}}
\\author{{Corrected Tree-Based Rational Inequality Solver}}
\\date{{\\today}}

\\begin{{document}}
\\maketitle

\\section{{Introduction}}

This document demonstrates the correct approach to variable elimination where each case
is solved completely to the end before proceeding to the next case. This creates a 
nested tree structure where subcases can have their own subcases.

\\section{{Initial System}}

Starting with the following system of inequalities:

\\left\\{{
\\begin{{aligned}}
"""
        
        # Add initial inequalities
        for i, ineq in enumerate(inequalities):
            if i > 0:
                latex_content += " \\\\\n& \\wedge \\\\\n"
            latex_content += f"& {ineq}"
        
        latex_content += """
\\end{aligned}
\\right\\}

"""
        
        # Generate nested case structure
        latex_content += self._generate_nested_cases_latex(case_tree, variables_to_eliminate, 1)
        
        latex_content += """
\\section{Summary}

The variable elimination process creates a nested tree structure where each case
is solved completely before moving to the next case. This ensures that:

\\begin{itemize}
\\item All possible parameter regions are covered
\\item No mathematical information is lost
\\item The complete solution structure is preserved
\\item Cases can have subcases that are also solved to completion
\\end{itemize}

The final result is a collection of case-specific constraint systems that together
represent the complete solution space after variable elimination.

\\end{document}
"""
        
        return latex_content
    
    def _generate_nested_cases_latex(self, case_node, variables_to_eliminate, depth):
        """
        Generate LaTeX for nested case structure recursively.
        """
        latex_content = ""
        
        # Skip the initial case, start with its subcases
        if case_node['case_id'] == 'Initial':
            if case_node['subcases']:
                variable = variables_to_eliminate[0]
                latex_content += f"\\section{{Eliminating Variable ${latex(symbols(variable))}$}}\n\n"
                
                for subcase in case_node['subcases']:
                    latex_content += self._generate_case_section_latex(subcase, variables_to_eliminate, 1, depth)
            
            return latex_content
        
        return latex_content
    
    def _generate_case_section_latex(self, case_node, variables_to_eliminate, step, depth):
        """
        Generate LaTeX for a specific case section.
        """
        latex_content = ""
        
        # Determine section level based on depth
        if depth == 1:
            section_cmd = "subsection"
        elif depth == 2:
            section_cmd = "subsubsection"
        else:
            section_cmd = "paragraph"
        
        # Case header
        case_number = case_node['case_id'].split('.')[-1]
        latex_content += f"\\{section_cmd}{{Case {case_number}}}\n\n"
        
        # Show current system
        latex_content += "\\textbf{Current System:}\n\n"
        latex_content += "\\left\\{\n\\begin{aligned}\n"
        
        for i, constraint in enumerate(case_node['system']):
            if i > 0:
                latex_content += " \\\\\n& \\wedge \\\\\n"
            
            expr, op, rhs = constraint
            if rhs == 0:
                latex_content += f"& {latex(expr)} {op} 0"
            else:
                latex_content += f"& {latex(expr)} {op} {latex(rhs)}"
        
        latex_content += "\n\\end{aligned}\n\\right\\}\n\n"
        
        # If this case has subcases, process next variable elimination
        if case_node['subcases']:
            # Find which variable is being eliminated next
            current_step = step
            if current_step < len(variables_to_eliminate):
                next_variable = variables_to_eliminate[current_step]
                
                latex_content += f"\\textbf{{Eliminating ${latex(symbols(next_variable))}$ from Case {case_number}:}}\n\n"
                
                # Show the analysis for this variable elimination
                latex_content += self._show_variable_elimination_analysis(
                    case_node['system'], next_variable, case_node['case_id']
                )
                
                # Process each subcase
                for subcase in case_node['subcases']:
                    latex_content += self._generate_case_section_latex(
                        subcase, variables_to_eliminate, step + 1, depth + 1
                    )
        else:
            # This is a final case - show final result
            latex_content += f"\\textbf{{Final Result for Case {case_number}:}}\n\n"
            
            if case_node['system']:
                latex_content += "\\left\\{\n\\begin{aligned}\n"
                for i, constraint in enumerate(case_node['system']):
                    if i > 0:
                        latex_content += " \\\\\n& \\wedge \\\\\n"
                    
                    expr, op, rhs = constraint
                    if rhs == 0:
                        latex_content += f"& {latex(expr)} {op} 0"
                    else:
                        latex_content += f"& {latex(expr)} {op} {latex(rhs)}"
                latex_content += "\n\\end{aligned}\n\\right\\}\n\n"
            else:
                latex_content += "No constraints (always true)\n\n"
        
        return latex_content
    
    def _show_variable_elimination_analysis(self, case_system, variable, case_id):
        """
        Show the mathematical analysis of variable elimination.
        """
        var_symbol = symbols(variable)
        
        # Find bounds for this variable
        lower_bounds = []
        upper_bounds = []
        other_constraints = []
        
        for constraint in case_system:
            expr, op, rhs = constraint
            if var_symbol in expr.free_symbols:
                # Try to solve for the variable
                bound_result = self.eliminator.solve_linear_inequality_for_variable(expr, op, rhs, variable)
                if bound_result:
                    bound_type, bound_expr = bound_result
                    if bound_type == 'lower':
                        lower_bounds.append((bound_expr, constraint))
                    else:
                        upper_bounds.append((bound_expr, constraint))
            else:
                other_constraints.append(constraint)
        
        latex_content = ""
        
        if lower_bounds:
            latex_content += f"\\textbf{{Lower bounds for ${latex(var_symbol)}$:}}\n"
            latex_content += "\\begin{itemize}\n"
            for bound_expr, original in lower_bounds:
                expr, op, rhs = original
                latex_content += f"\\item From ${latex(expr)} {op} {latex(rhs)}$: ${latex(var_symbol)} \\geq {latex(bound_expr)}$\n"
            latex_content += "\\end{itemize}\n\n"
        
        if upper_bounds:
            latex_content += f"\\textbf{{Upper bounds for ${latex(var_symbol)}$:}}\n"
            latex_content += "\\begin{itemize}\n"
            for bound_expr, original in upper_bounds:
                expr, op, rhs = original
                latex_content += f"\\item From ${latex(expr)} {op} {latex(rhs)}$: ${latex(var_symbol)} \\leq {latex(bound_expr)}$\n"
            latex_content += "\\end{itemize}\n\n"
        
        # Show case analysis reasoning
        if len(lower_bounds) > 1:
            latex_content += f"\\textbf{{Multiple lower bounds require case analysis:}}\n"
            latex_content += "\\begin{itemize}\n"
            for i, (bound_expr, _) in enumerate(lower_bounds, 1):
                latex_content += f"\\item Sub-case {i}: ${latex(bound_expr)}$ is the tightest lower bound\n"
            latex_content += "\\end{itemize}\n\n"
        elif len(upper_bounds) > 1:
            latex_content += f"\\textbf{{Multiple upper bounds require case analysis:}}\n"
            latex_content += "\\begin{itemize}\n"
            for i, (bound_expr, _) in enumerate(upper_bounds, 1):
                latex_content += f"\\item Sub-case {i}: ${latex(bound_expr)}$ is the tightest upper bound\n"
            latex_content += "\\end{itemize}\n\n"
        elif lower_bounds and upper_bounds:
            latex_content += f"\\textbf{{Both bounds present - elimination constraint:}}\n"
            lower_expr, _ = lower_bounds[0]
            upper_expr, _ = upper_bounds[0]
            latex_content += f"For ${latex(var_symbol)}$ to exist: ${latex(lower_expr)} \\leq {latex(upper_expr)}$\n\n"
        
        return latex_content


def test_nested_case_latex():
    """
    Test the nested case LaTeX generation.
    """
    print("=" * 80)
    print("TESTING NESTED CASE LATEX GENERATION")
    print("=" * 80)
    
    generator = NestedCaseLatexGenerator()
    
    # Test case with multiple lower bounds (creates subcases)
    system1 = ["x + 2*y >= 1", "x - y >= -1", "y <= 3"]
    variables1 = ['x']
    
    print("TEST 1: Multiple Lower Bounds (Creates Subcases)")
    print(f"System: {system1}")
    print(f"Variables to eliminate: {variables1}")
    print()
    
    latex_content1 = generator.generate_nested_case_latex(system1, variables1)
    
    # Save to file
    output_dir = "/workspaces/codespaces-blank/output_corrected"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename1 = f"{output_dir}/nested_case_test1_{timestamp}.tex"
    
    with open(filename1, 'w') as f:
        f.write(latex_content1)
    
    print(f"✅ Generated LaTeX file: {filename1}")
    
    # Test multi-variable case
    system2 = ["x + y >= 1", "x - z <= 2", "y - z >= 0"]
    variables2 = ['x', 'y']
    
    print("\nTEST 2: Multi-Variable with Nested Cases")
    print(f"System: {system2}")
    print(f"Variables to eliminate: {variables2}")
    print()
    
    latex_content2 = generator.generate_nested_case_latex(system2, variables2)
    
    filename2 = f"{output_dir}/nested_case_test2_{timestamp}.tex"
    
    with open(filename2, 'w') as f:
        f.write(latex_content2)
    
    print(f"✅ Generated LaTeX file: {filename2}")
    
    print("\n" + "=" * 60)
    print("PREVIEW OF GENERATED STRUCTURE:")
    print("=" * 60)
    
    # Show preview of the structure
    print("""
Expected LaTeX Structure:

Section: Eliminating Variable x
  Subsection: Case 1
    Current System: [original inequalities]
    Eliminating y from Case 1:
      Lower bounds for y: ...
      Multiple lower bounds require case analysis
    
    Subsubsection: Case 1.1  
      Current System: [case 1.1 constraints]
      Final Result for Case 1.1: [final constraints]
    
    Subsubsection: Case 1.2
      Current System: [case 1.2 constraints] 
      Final Result for Case 1.2: [final constraints]
  
  Subsection: Case 2
    Current System: [case 2 constraints]
    Eliminating y from Case 2:
      [analysis for case 2]
    
    Subsubsection: Case 2.1
      [case 2.1 complete solution]
""")


if __name__ == "__main__":
    test_nested_case_latex()
