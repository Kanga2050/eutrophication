#!/usr/bin/env python3

"""
CORRECTED Multi-Case Variable Elimination

This implements the proper tree-based approach where each case from 
variable elimination is processed independently through all subsequent steps.

Key fix: When variable elimination produces multiple cases, each case
should be processed separately as independent constraint systems.
"""

import sys
sys.path.append('/workspaces/codespaces-blank')

from variable_eliminator import VariableEliminationSolver  
from sympy import symbols, sympify
from input_processor import process_inequalities
from case_processor import isolate_cases_from_solver

class TreeBasedVariableEliminator:
    """
    Corrected variable eliminator that maintains case tree structure.
    """
    
    def __init__(self):
        self.solver = VariableEliminationSolver()
    
    def eliminate_variables_tree_based(self, inequalities, variables_to_eliminate):
        """
        Eliminate variables maintaining complete case tree structure.
        
        Returns: List of final case systems, each case is a list of constraints
        """
        
        # Start with single case containing all initial inequalities
        current_cases = [process_inequalities(inequalities)]
        
        print(f"Starting with {len(current_cases)} case(s)")
        print(f"Initial system: {current_cases[0]}")
        print()
        
        # Eliminate each variable in sequence
        for step, variable in enumerate(variables_to_eliminate, 1):
            print(f"STEP {step}: Eliminating variable '{variable}'")
            print(f"Processing {len(current_cases)} case(s)")
            
            new_cases = []
            
            # Process each current case independently
            for case_idx, case_system in enumerate(current_cases):
                print(f"\n  Processing Case {case_idx + 1}: {case_system}")
                
                # Eliminate variable from this specific case
                case_results = self._eliminate_variable_from_case(case_system, variable)
                
                print(f"    -> Generated {len(case_results)} new case(s)")
                for sub_idx, sub_case in enumerate(case_results):
                    print(f"      Sub-case {sub_idx + 1}: {sub_case}")
                
                new_cases.extend(case_results)
            
            current_cases = new_cases
            print(f"\nAfter eliminating '{variable}': {len(current_cases)} total case(s)\n")
        
        return current_cases
    
    def _eliminate_variable_from_case(self, case_system, variable):
        """
        Eliminate variable from a single case system.
        Returns list of resulting case systems.
        """
        
        # Find inequalities involving the variable
        var_symbol = symbols(variable)
        involving_var = []
        not_involving_var = []
        
        for ineq in case_system:
            expr, op, rhs = ineq
            if var_symbol in expr.free_symbols:
                involving_var.append(ineq)
            else:
                not_involving_var.append(ineq)
        
        if not involving_var:
            # Variable doesn't appear, return original case
            return [case_system]
        
        print(f"    Inequalities involving {variable}: {involving_var}")
        print(f"    Inequalities not involving {variable}: {not_involving_var}")
        
        # For each inequality involving the variable, solve for bounds
        lower_bounds = []
        upper_bounds = []
        conditions = []
        
        for ineq in involving_var:
            bounds_result = self._get_variable_bounds(ineq, variable)
            
            if bounds_result:
                bound_type, bound_expr, bound_conditions = bounds_result
                if bound_type == 'lower':
                    lower_bounds.append((bound_expr, bound_conditions))
                elif bound_type == 'upper':
                    upper_bounds.append((bound_expr, bound_conditions))
                conditions.extend(bound_conditions)
        
        # Generate all possible case combinations
        return self._generate_elimination_cases(
            not_involving_var, lower_bounds, upper_bounds, conditions
        )
    
    def _get_variable_bounds(self, inequality, variable):
        """
        Extract variable bounds from a single inequality.
        Returns (bound_type, bound_expression, conditions) or None
        """
        expr, op, rhs = inequality
        var_symbol = symbols(variable)
        
        # Try to solve for the variable
        from solver import solve_rational_ineq_full
        
        # Convert to standard form: expression op 0
        if op == '>=':
            std_expr = expr - rhs
            std_op = '>='
        elif op == '<=':
            std_expr = expr - rhs  
            std_op = '<='
        elif op == '>':
            std_expr = expr - rhs
            std_op = '>'
        elif op == '<':
            std_expr = expr - rhs
            std_op = '<'
        else:
            return None
        
        # Use existing solver to get cases
        try:
            solver_result = solve_rational_ineq_full(std_expr, var_symbol, std_op)
            
            if not solver_result or len(solver_result) == 0:
                return None
            
            # Extract first case for simplicity
            # TODO: Handle multiple cases properly
            first_case = solver_result[0]
            
            if 'lower_bound' in first_case:
                return 'lower', first_case['lower_bound'], first_case.get('conditions', [])
            elif 'upper_bound' in first_case:
                return 'upper', first_case['upper_bound'], first_case.get('conditions', [])
                
        except Exception as e:
            print(f"    Warning: Could not solve {inequality} for {variable}: {e}")
            return None
    
    def _generate_elimination_cases(self, base_constraints, lower_bounds, upper_bounds, conditions):
        """
        Generate all valid case combinations from variable elimination.
        """
        
        cases = []
        
        # If no bounds found, return base constraints
        if not lower_bounds and not upper_bounds:
            return [base_constraints]
        
        # Case 1: Only lower bounds - variable is unconstrained above
        if lower_bounds and not upper_bounds:
            # Need all lower bounds to be consistent
            case_constraints = list(base_constraints)
            
            # Add maximum of lower bounds constraint
            if len(lower_bounds) == 1:
                bound_expr, bound_conds = lower_bounds[0]
                # Add the bound condition (bound expression should be satisfiable)
                case_constraints.extend(bound_conds)
            else:
                # Multiple lower bounds - need max to be well-defined
                # For now, add all conditions
                for bound_expr, bound_conds in lower_bounds:
                    case_constraints.extend(bound_conds)
            
            cases.append(case_constraints)
        
        # Case 2: Only upper bounds - variable is unconstrained below  
        elif upper_bounds and not lower_bounds:
            case_constraints = list(base_constraints)
            
            # Add minimum of upper bounds constraint
            if len(upper_bounds) == 1:
                bound_expr, bound_conds = upper_bounds[0]
                case_constraints.extend(bound_conds)
            else:
                # Multiple upper bounds - need min to be well-defined
                for bound_expr, bound_conds in upper_bounds:
                    case_constraints.extend(bound_conds)
            
            cases.append(case_constraints)
        
        # Case 3: Both lower and upper bounds - need max(lower) <= min(upper)
        else:
            case_constraints = list(base_constraints)
            
            # Add constraint that max(lower) <= min(upper)
            # This is the key elimination constraint
            for lower_expr, lower_conds in lower_bounds:
                for upper_expr, upper_conds in upper_bounds:
                    # Create constraint: lower_bound <= upper_bound
                    elimination_constraint = (lower_expr - upper_expr, '<=', 0)
                    
                    sub_case = list(base_constraints)
                    sub_case.append(elimination_constraint)
                    sub_case.extend(lower_conds)
                    sub_case.extend(upper_conds)
                    
                    cases.append(sub_case)
        
        return cases if cases else [base_constraints]


def test_corrected_approach():
    """Test the corrected tree-based approach"""
    
    print("=" * 80)
    print("TESTING CORRECTED TREE-BASED VARIABLE ELIMINATION")
    print("=" * 80)
    
    eliminator = TreeBasedVariableEliminator()
    
    # Test 1: Simple linear case
    print("TEST 1: Simple Linear Case")
    print("-" * 40)
    
    system1 = ["x + 2*y >= 1", "x - y >= -1", "y <= 3"]
    variables1 = ['x']
    
    print(f"System: {system1}")
    print(f"Eliminate: {variables1}")
    print()
    
    result1 = eliminator.eliminate_variables_tree_based(system1, variables1)
    
    print("FINAL RESULT:")
    for i, case in enumerate(result1, 1):
        print(f"  Case {i}: {case}")
    
    print("\n" + "=" * 60)
    print("EXPECTED vs ACTUAL ANALYSIS:")
    print("Expected: Should get constraint like '1 - 2*y <= y - 1' -> 'y <= 2/3'")
    print(f"Actual: {len(result1)} case(s) generated")
    
    # Test 2: Multi-variable case
    print("\n" + "=" * 60)
    print("TEST 2: Multi-Variable Case")
    print("-" * 40)
    
    system2 = ["x + y >= 1", "x - z <= 2", "y + z >= 0"]
    variables2 = ['x', 'y']
    
    print(f"System: {system2}")
    print(f"Eliminate: {variables2}")
    print()
    
    result2 = eliminator.eliminate_variables_tree_based(system2, variables2)
    
    print("FINAL RESULT:")
    for i, case in enumerate(result2, 1):
        print(f"  Case {i}: {case}")


if __name__ == "__main__":
    test_corrected_approach()
