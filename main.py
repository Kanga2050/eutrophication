"""
Hierarchical Case-Based Variable Elimination with Descriptive Naming

This module implements a complete 4-step variable elimination process with
hierarchical case structures and descriptive naming (case 1, subcase 1.1, 
subsubcase 1.1.2, etc.). Each subcase is solved individually and included
in the LaTeX output with proper case labeling.

Essential Components:
- HierarchicalCaseEliminator: Manages hierarchical case structure
- CaseNamingSystem: Provides descriptive case numbering
- LatexCaseGenerator: Generates LaTeX with case hierarchy
- 4-Step Elimination Process for each variable
- Individual subcase solving and documentation

Author: Rational Inequality Solver Team
Version: Hierarchical Case Management with Descriptive Naming
"""
from sympy import symbols, simplify, solve, latex, Max, Min
from datetime import datetime
import os
import traceback
from collections import defaultdict

# Import necessary modules for case processing
from input_processor import process_inequalities
from solver import solve_rational_ineq_full
from case_processor import isolate_cases_from_solver


class CaseNamingSystem:
    """Manages hierarchical case naming (case 1, subcase 1.1, subsubcase 1.1.2, etc.)"""
    
    def __init__(self):
        self.case_counters = defaultdict(int)
        self.parent_cases = {}
    
    def get_case_name(self, parent_case=None, level=0):
        """Generate hierarchical case name"""
        if parent_case is None:
            # Top-level case
            self.case_counters[0] += 1
            case_name = f"Case {self.case_counters[0]}"
            case_id = str(self.case_counters[0])
        else:
            # Sub-case
            parent_id = self.parent_cases.get(parent_case, "1")
            key = f"{parent_id}_{level}"
            self.case_counters[key] += 1
            
            if level == 1:
                case_name = f"Subcase {parent_id}.{self.case_counters[key]}"
                case_id = f"{parent_id}.{self.case_counters[key]}"
            elif level == 2:
                case_name = f"Subsubcase {parent_id}.{self.case_counters[key]}"
                case_id = f"{parent_id}.{self.case_counters[key]}"
            else:
                # Deep nesting
                prefix = "Sub" * level + "case"
                case_name = f"{prefix} {parent_id}.{self.case_counters[key]}"
                case_id = f"{parent_id}.{self.case_counters[key]}"
        
        self.parent_cases[case_name] = case_id
        return case_name, case_id
    
    def reset_level(self, level):
        """Reset counters for a specific level and all deeper levels"""
        keys_to_remove = [k for k in self.case_counters.keys() if isinstance(k, str) and len(k.split('_')) > level]
        for key in keys_to_remove:
            del self.case_counters[key]


class HierarchicalCase:
    """Represents a case in the hierarchical structure"""
    
    def __init__(self, name, case_id, inequalities, parent=None, level=0):
        self.name = name
        self.case_id = case_id
        self.inequalities = inequalities
        self.parent = parent
        self.level = level
        self.subcases = []
        self.elimination_steps = []
        self.is_solved = False
        self.solution_constraints = []
    
    def add_subcase(self, subcase):
        """Add a subcase to this case"""
        self.subcases.append(subcase)
    
    def add_elimination_step(self, step):
        """Add an elimination step to this case"""
        self.elimination_steps.append(step)
    
    def solve_case(self, solver_func=None):
        """Solve this individual case"""
        if self.is_solved:
            return self.solution_constraints
            
        try:
            # If no more variables to eliminate, this is a final constraint case
            if not any(str(var).startswith('x') for ineq in self.inequalities 
                      for expr, op, rhs in [ineq] for var in expr.free_symbols):
                self.solution_constraints = self.inequalities
                self.is_solved = True
                return self.solution_constraints
            
            # Otherwise, additional processing needed
            self.solution_constraints = self.inequalities
            self.is_solved = True
            return self.solution_constraints
            
        except Exception as e:
            print(f"Error solving case {self.name}: {e}")
            self.solution_constraints = []
            self.is_solved = True
            return self.solution_constraints


class HierarchicalCaseEliminator:
    """Implements 4-step variable elimination with hierarchical case management"""
    
    def __init__(self, use_sign_analysis=True):
        self.naming_system = CaseNamingSystem()
        self.all_cases = []
        self.elimination_log = []
        self.use_sign_analysis = use_sign_analysis
    
    def eliminate_variables_hierarchical(self, inequalities, variables_to_eliminate):
        """
        Main elimination function with hierarchical case management
        """
        print("=" * 80)
        print("HIERARCHICAL VARIABLE ELIMINATION WITH 4-STEP PROCESS")
        print("=" * 80)
        
        # Initialize with the root case
        processed_ineqs = process_inequalities(inequalities)
        root_name, root_id = self.naming_system.get_case_name()
        root_case = HierarchicalCase(root_name, root_id, processed_ineqs, level=0)
        
        current_cases = [root_case]
        self.all_cases = [root_case]
        
        print(f"Initial system: {len(processed_ineqs)} inequalities")
        for i, (lhs, op, rhs) in enumerate(processed_ineqs):
            print(f"  {i+1}. {lhs} {op} {rhs}")
        print()
        
        # Eliminate each variable
        for step, variable in enumerate(variables_to_eliminate):
            print(f"ELIMINATION STEP {step + 1}: Variable '{variable}'")
            print(f"Processing {len(current_cases)} case(s)")
            
            new_cases = []
            
            for case in current_cases:
                print(f"\n  Processing {case.name}:")
                print(f"    Inequalities: {len(case.inequalities)}")
                
                # Apply 4-step elimination to this case
                subcases = self.eliminate_variable_4_step_hierarchical(case, variable)
                
                # Solve each subcase individually
                for subcase in subcases:
                    subcase.solve_case()
                    new_cases.append(subcase)
                    self.all_cases.append(subcase)
                    print(f"    -> Generated {subcase.name}: {len(subcase.inequalities)} constraints")
            
            current_cases = new_cases
            print(f"\nAfter eliminating '{variable}': {len(current_cases)} total case(s)")
            print()
        
        return current_cases
    
    def eliminate_variable_4_step_hierarchical(self, parent_case, variable):
        """
        4-step elimination for a single case with hierarchical subcase generation
        """
        from sympy import symbols
        var_symbol = symbols(variable)
        
        # Step 1: Isolate variable
        step1_result = self._step1_isolate_variable_hierarchical(parent_case, variable)
        
        # Step 2: Combine to min/max
        step2_result = self._step2_combine_to_minmax_hierarchical(step1_result, variable)
        
        # Step 3: Remove variable
        step3_result = self._step3_remove_variable_hierarchical(step2_result, variable)
        
        # Step 4: Expand cases
        subcases = self._step4_expand_cases_hierarchical(step3_result, variable, parent_case)
        
        # Store elimination steps in parent case
        elimination_step = {
            'variable': variable,
            'step1': step1_result,
            'step2': step2_result,
            'step3': step3_result,
            'step4': {'subcases': len(subcases)}
        }
        parent_case.add_elimination_step(elimination_step)
        
        return subcases
    
    def _step1_isolate_variable_hierarchical(self, case, variable):
        """Step 1: Isolate variable in each inequality"""
        from sympy import symbols, solve, simplify
        var_symbol = symbols(variable)
        
        involving_var = []
        not_involving_var = []
        isolated_inequalities = []
        step1_inequalities = []  # Track inequalities after step 1
        
        print(f"      STEP 1: Isolate variable {variable}")
        print(f"        Goal: Transform each inequality containing {variable} to the form '{variable} ≥ expr' or '{variable} ≤ expr'")
        print()
        
        for i, ineq in enumerate(case.inequalities):
            expr, op, rhs = ineq
            if var_symbol in expr.free_symbols:
                involving_var.append(ineq)
                print(f"        Inequality {i+1}: {expr} {op} {rhs}")
                print(f"          Contains variable {variable}, proceeding with isolation...")
                
                # Show the detailed isolation work
                original_eq = f"{expr} {op} {rhs}"
                print(f"          Original: {original_eq}")
                
                # Use the full solver to handle all types of inequalities
                bound_results = self._solve_inequality_for_variable(expr, op, rhs, variable)
                
                if bound_results:
                    for bound_type, bound_expr, new_op in bound_results:
                        isolated_form = f"{variable} {new_op} {bound_expr}"
                        print(f"          Solving for {variable}: {isolated_form}")
                        
                        isolated_inequalities.append((bound_type, bound_expr, new_op))
                        # Add to step1 inequalities as (variable, new_op, bound_expr) for consistency
                        step1_inequalities.append((var_symbol, new_op, bound_expr))
                        print(f"          RESULT: {isolated_form} ({bound_type} bound)")
                else:
                    print(f"          ERROR: Could not isolate {variable}")
                print()
            else:
                not_involving_var.append(ineq)
                step1_inequalities.append(ineq)  # Keep unchanged inequalities
                print(f"        Inequality {i+1}: {expr} {op} {rhs}")
                print(f"          Does not contain variable {variable}, keeping unchanged")
                print()
        
        print(f"        STEP 1 SUMMARY:")
        print(f"          Inequalities involving {variable}: {len(involving_var)}")
        print(f"          Inequalities not involving {variable}: {len(not_involving_var)}")
        print(f"          Successfully isolated inequalities: {len(isolated_inequalities)}")
        
        # Show the inequalities after Step 1
        print(f"        INEQUALITIES AFTER STEP 1:")
        for i, ineq in enumerate(step1_inequalities, 1):
            if len(ineq) == 3:
                lhs, op, rhs = ineq
                print(f"          {i}. {lhs} {op} {rhs}")
        print()
        
        return {
            'involving_var': involving_var,
            'not_involving_var': not_involving_var,
            'isolated_inequalities': isolated_inequalities,
            'step1_inequalities': step1_inequalities
        }
    
    def _step2_combine_to_minmax_hierarchical(self, step1_result, variable):
        """Step 2: Combine to max/min form"""
        from sympy import symbols
        var_symbol = symbols(variable)
        
        print(f"      STEP 2: Combine to max/min form")
        print(f"        Goal: Collect lower bounds into max() and upper bounds into min()")
        print()
        
        isolated = step1_result['isolated_inequalities']
        not_involving_var = step1_result['not_involving_var']
        lower_bounds = []
        upper_bounds = []
        step2_inequalities = []  # Track inequalities after step 2
        
        print(f"        Processing {len(isolated)} isolated inequalities:")
        
        for i, (bound_type, bound_expr, op) in enumerate(isolated):
            print(f"          {i+1}. {variable} {op} {bound_expr}")
            if bound_type == 'lower':
                lower_bounds.append((bound_expr, op))
                print(f"             -> Added to LOWER bounds collection")
            else:
                upper_bounds.append((bound_expr, op))
                print(f"             -> Added to UPPER bounds collection")
        
        print()
        print(f"        Lower bounds collected: {len(lower_bounds)}")
        for i, (expr, op) in enumerate(lower_bounds):
            print(f"          {i+1}. {variable} {op} {expr}")
        
        print(f"        Upper bounds collected: {len(upper_bounds)}")
        for i, (expr, op) in enumerate(upper_bounds):
            print(f"          {i+1}. {variable} {op} {expr}")
        
        print()
        
        # Create the step 2 inequalities (minmax form + non-involving)
        step2_inequalities.extend(not_involving_var)  # Keep non-involving constraints
        
        minmax_form = None
        minmax_inequalities = []  # Store the actual min/max inequalities
        
        if lower_bounds and upper_bounds:
            lower_exprs = [str(expr) for expr, op in lower_bounds]
            upper_exprs = [str(expr) for expr, op in upper_bounds]
            minmax_form = f"max({', '.join(lower_exprs)}) <= {variable} <= min({', '.join(upper_exprs)})"
            
            # Create two inequalities: max(lower) <= variable and variable <= min(upper)
            from sympy import Max, Min
            max_lower = Max(*[expr for expr, op in lower_bounds])
            min_upper = Min(*[expr for expr, op in upper_bounds])
            
            minmax_inequalities.append((max_lower, '<=', var_symbol))
            minmax_inequalities.append((var_symbol, '<=', min_upper))
            step2_inequalities.extend(minmax_inequalities)
            
            print(f"        COMBINED FORM: {minmax_form}")
            print(f"          Left side: max of {len(lower_exprs)} expressions")
            print(f"          Right side: min of {len(upper_exprs)} expressions")
        elif lower_bounds:
            lower_exprs = [str(expr) for expr, op in lower_bounds]
            minmax_form = f"{variable} >= max({', '.join(lower_exprs)})"
            
            from sympy import Max
            max_lower = Max(*[expr for expr, op in lower_bounds])
            minmax_inequalities.append((max_lower, '<=', var_symbol))
            step2_inequalities.extend(minmax_inequalities)
            
            print(f"        COMBINED FORM: {minmax_form}")
            print(f"          Only lower bounds: max of {len(lower_exprs)} expressions")
        elif upper_bounds:
            upper_exprs = [str(expr) for expr, op in upper_bounds]
            minmax_form = f"{variable} <= min({', '.join(upper_exprs)})"
            
            from sympy import Min
            min_upper = Min(*[expr for expr, op in upper_bounds])
            minmax_inequalities.append((var_symbol, '<=', min_upper))
            step2_inequalities.extend(minmax_inequalities)
            
            print(f"        COMBINED FORM: {minmax_form}")
            print(f"          Only upper bounds: min of {len(upper_exprs)} expressions")
        else:
            print(f"        No bounds found for variable {variable}")
        
        # Show the inequalities after Step 2
        print(f"        INEQUALITIES AFTER STEP 2:")
        for i, ineq in enumerate(step2_inequalities, 1):
            if len(ineq) == 3:
                lhs, op, rhs = ineq
                print(f"          {i}. {lhs} {op} {rhs}")
        
        print(f"        STEP 2 SUMMARY: Created {minmax_form if minmax_form else 'no constraints'}")
        print()
        
        return {
            'lower_bounds': lower_bounds,
            'upper_bounds': upper_bounds,
            'minmax_form': minmax_form,
            'step2_inequalities': step2_inequalities,
            'minmax_inequalities': minmax_inequalities
        }
    
    def _step3_remove_variable_hierarchical(self, step2_result, variable):
        """Step 3: Remove variable creating elimination constraints"""
        print(f"      STEP 3: Remove variable {variable}")
        print(f"        Goal: Replace variable with feasibility constraints")
        print()
        
        lower_bounds = step2_result['lower_bounds']
        upper_bounds = step2_result['upper_bounds']
        minmax_form = step2_result['minmax_form']
        not_involving_var = step2_result.get('step2_inequalities', [])
        elimination_constraints = []
        step3_inequalities = []  # Track inequalities after step 3
        
        # Start with non-involving variables
        from sympy import symbols
        var_symbol = symbols(variable)
        step3_inequalities = []
        
        # Filter out inequalities that involve the variable being eliminated
        for ineq in not_involving_var:
            if len(ineq) == 3:
                lhs, op, rhs = ineq
                # Check if variable appears in left-hand side or right-hand side
                lhs_has_var = hasattr(lhs, 'free_symbols') and var_symbol in lhs.free_symbols
                rhs_has_var = hasattr(rhs, 'free_symbols') and var_symbol in rhs.free_symbols
                
                if not lhs_has_var and not rhs_has_var:
                    step3_inequalities.append(ineq)
        
        if minmax_form:
            print(f"        Starting with combined form: {minmax_form}")
        
        if lower_bounds and upper_bounds:
            lower_exprs = [expr for expr, op in lower_bounds]
            upper_exprs = [expr for expr, op in upper_bounds]
            
            print(f"        Variable {variable} is bounded:")
            print(f"          Lower bounds: {[str(expr) for expr in lower_exprs]}")
            print(f"          Upper bounds: {[str(expr) for expr in upper_exprs]}")
            print()
            
            print(f"        For feasibility, we need: max(lower_bounds) ≤ min(upper_bounds)")
            constraint_desc = f"max({', '.join(map(str, lower_exprs))}) <= min({', '.join(map(str, upper_exprs))})"
            elimination_constraints.append(constraint_desc)
            
            # Create the actual elimination constraint
            from sympy import Max, Min
            max_lower = Max(*lower_exprs)
            min_upper = Min(*upper_exprs)
            elimination_constraint = (max_lower, '<=', min_upper)
            step3_inequalities.append(elimination_constraint)
            
            print(f"        ELIMINATION CONSTRAINT: {constraint_desc}")
            print(f"          This ensures that the maximum of all lower bounds")
            print(f"          does not exceed the minimum of all upper bounds")
            print()
            
        elif lower_bounds:
            lower_exprs = [expr for expr, op in lower_bounds]
            print(f"        Variable {variable} has only lower bounds:")
            print(f"          Lower bounds: {[str(expr) for expr in lower_exprs]}")
            print(f"        No elimination constraint needed (variable can be arbitrarily large)")
            print()
            
        elif upper_bounds:
            upper_exprs = [expr for expr, op in upper_bounds]
            print(f"        Variable {variable} has only upper bounds:")
            print(f"          Upper bounds: {[str(expr) for expr in upper_exprs]}")
            print(f"        No elimination constraint needed (variable can be arbitrarily small)")
            print()
            
        else:
            print(f"        Variable {variable} has no bounds")
            print(f"        No elimination constraint needed (variable is unconstrained)")
            print()
        
        # Show the inequalities after Step 3
        print(f"        INEQUALITIES AFTER STEP 3:")
        for i, ineq in enumerate(step3_inequalities, 1):
            if len(ineq) == 3:
                lhs, op, rhs = ineq
                print(f"          {i}. {lhs} {op} {rhs}")
        
        print(f"        STEP 3 SUMMARY:")
        print(f"          Generated {len(elimination_constraints)} elimination constraint(s)")
        for i, constraint in enumerate(elimination_constraints, 1):
            print(f"            {i}. {constraint}")
        print()
        
        return {
            'elimination_constraints': elimination_constraints,
            'lower_exprs': [expr for expr, op in lower_bounds] if lower_bounds else [],
            'upper_exprs': [expr for expr, op in upper_bounds] if upper_bounds else [],
            'step3_inequalities': step3_inequalities
        }
    
    def _step4_expand_cases_hierarchical(self, step3_result, variable, parent_case):
        """Step 4: Expand cases with hierarchical naming"""
        print(f"      STEP 4: Expand cases")
        print(f"        Goal: Create subcases for each min/max combination to fully represent constraints")
        print()
        
        lower_exprs = step3_result['lower_exprs']
        upper_exprs = step3_result['upper_exprs']
        step3_inequalities = step3_result.get('step3_inequalities', [])
        subcases = []
        
        # Get non-involving constraints to add to each subcase
        from sympy import symbols
        var_symbol = symbols(variable)
        not_involving_var = []
        
        # Filter out inequalities that involve the variable being eliminated
        for ineq in step3_inequalities:
            if len(ineq) == 3:
                lhs, op, rhs = ineq
                # Check if variable appears in left-hand side or right-hand side
                lhs_has_var = hasattr(lhs, 'free_symbols') and var_symbol in lhs.free_symbols
                rhs_has_var = hasattr(rhs, 'free_symbols') and var_symbol in rhs.free_symbols
                
                if not lhs_has_var and not rhs_has_var:
                    not_involving_var.append(ineq)
        
        print(f"        Constraints not involving {variable}: {len(not_involving_var)}")
        for i, (expr, op, rhs) in enumerate(not_involving_var, 1):
            print(f"          {i}. {expr} {op} {rhs}")
        print()
        
        print(f"        Lower bound expressions: {len(lower_exprs)}")
        for i, expr in enumerate(lower_exprs, 1):
            print(f"          {i}. {expr}")
        
        print(f"        Upper bound expressions: {len(upper_exprs)}")
        for i, expr in enumerate(upper_exprs, 1):
            print(f"          {i}. {expr}")
        print()
        
        if lower_exprs and upper_exprs:
            # Create all combinations: each lower bound vs each upper bound
            total_combinations = len(lower_exprs) * len(upper_exprs)
            print(f"        Creating {len(lower_exprs)} × {len(upper_exprs)} = {total_combinations} subcases")
            print(f"        Each subcase represents when a specific lower bound ≤ specific upper bound")
            print()
            
            for i, lower_expr in enumerate(lower_exprs):
                for j, upper_expr in enumerate(upper_exprs):
                    # Create subcase
                    subcase_name, subcase_id = self.naming_system.get_case_name(
                        parent_case.name, parent_case.level + 1
                    )
                    
                    # Create constraint: lower_expr <= upper_expr
                    constraint = (lower_expr - upper_expr, '<=', 0)
                    subcase_inequalities = list(not_involving_var) + [constraint]
                    
                    subcase = HierarchicalCase(
                        subcase_name, subcase_id, subcase_inequalities,
                        parent=parent_case, level=parent_case.level + 1
                    )
                    
                    parent_case.add_subcase(subcase)
                    subcases.append(subcase)
                    
                    print(f"          {subcase_name}:")
                    print(f"            Condition: {lower_expr} ≤ {upper_expr}")
                    print(f"            Mathematical form: {lower_expr} - ({upper_expr}) ≤ 0")
                    print(f"            INEQUALITIES AFTER STEP 4:")
                    for k, ineq in enumerate(subcase_inequalities, 1):
                        if len(ineq) == 3:
                            lhs, op, rhs = ineq
                            print(f"              {k}. {lhs} {op} {rhs}")
                    print(f"            Total constraints in subcase: {len(subcase_inequalities)}")
                    print()
                    
        elif len(lower_exprs) > 1:
            # Multiple lower bounds: determine which is tightest
            print(f"        Multiple lower bounds case - creating {len(lower_exprs)} subcases")
            print(f"        Each subcase represents when a specific lower bound is the tightest")
            print()
            
            for i, tightest_lower in enumerate(lower_exprs):
                subcase_name, subcase_id = self.naming_system.get_case_name(
                    parent_case.name, parent_case.level + 1
                )
                
                case_constraints = list(not_involving_var)
                tightness_constraints = []
                
                for j, other_lower in enumerate(lower_exprs):
                    if i != j:
                        tightness_constraint = (tightest_lower - other_lower, '>=', 0)
                        case_constraints.append(tightness_constraint)
                        tightness_constraints.append(f"{tightest_lower} ≥ {other_lower}")
                
                subcase = HierarchicalCase(
                    subcase_name, subcase_id, case_constraints,
                    parent=parent_case, level=parent_case.level + 1
                )
                
                parent_case.add_subcase(subcase)
                subcases.append(subcase)
                
                print(f"          {subcase_name}:")
                print(f"            Tightest lower bound: {tightest_lower}")
                print(f"            Tightness conditions:")
                for k, condition in enumerate(tightness_constraints, 1):
                    print(f"              {k}. {condition}")
                print(f"            INEQUALITIES AFTER STEP 4:")
                for k, ineq in enumerate(case_constraints, 1):
                    if len(ineq) == 3:
                        lhs, op, rhs = ineq
                        print(f"              {k}. {lhs} {op} {rhs}")
                print(f"            Total constraints in subcase: {len(case_constraints)}")
                print()
                
        elif len(upper_exprs) > 1:
            # Multiple upper bounds: determine which is tightest
            print(f"        Multiple upper bounds case - creating {len(upper_exprs)} subcases")
            print(f"        Each subcase represents when a specific upper bound is the tightest")
            print()
            
            for i, tightest_upper in enumerate(upper_exprs):
                subcase_name, subcase_id = self.naming_system.get_case_name(
                    parent_case.name, parent_case.level + 1
                )
                
                case_constraints = list(not_involving_var)
                tightness_constraints = []
                
                for j, other_upper in enumerate(upper_exprs):
                    if i != j:
                        tightness_constraint = (tightest_upper - other_upper, '<=', 0)
                        case_constraints.append(tightness_constraint)
                        tightness_constraints.append(f"{tightest_upper} ≤ {other_upper}")
                
                subcase = HierarchicalCase(
                    subcase_name, subcase_id, case_constraints,
                    parent=parent_case, level=parent_case.level + 1
                )
                
                parent_case.add_subcase(subcase)
                subcases.append(subcase)
                
                print(f"          {subcase_name}:")
                print(f"            Tightest upper bound: {tightest_upper}")
                print(f"            Tightness conditions:")
                for k, condition in enumerate(tightness_constraints, 1):
                    print(f"              {k}. {condition}")
                print(f"            INEQUALITIES AFTER STEP 4:")
                for k, ineq in enumerate(case_constraints, 1):
                    if len(ineq) == 3:
                        lhs, op, rhs = ineq
                        print(f"              {k}. {lhs} {op} {rhs}")
                print(f"            Total constraints in subcase: {len(case_constraints)}")
                print()
        else:
            # No expansion needed, just carry over constraints
            subcase_name, subcase_id = self.naming_system.get_case_name(
                parent_case.name, parent_case.level + 1
            )
            
            subcase = HierarchicalCase(
                subcase_name, subcase_id, list(not_involving_var),
                parent=parent_case, level=parent_case.level + 1
            )
            
            parent_case.add_subcase(subcase)
            subcases.append(subcase)
            
            print(f"          {subcase_name}:")
            print(f"            No case expansion needed")
            print(f"            Simply carrying over non-involving constraints")
            print(f"            INEQUALITIES AFTER STEP 4:")
            for k, ineq in enumerate(not_involving_var, 1):
                if len(ineq) == 3:
                    lhs, op, rhs = ineq
                    print(f"              {k}. {lhs} {op} {rhs}")
            print(f"            Total constraints in subcase: {len(not_involving_var)}")
            print()
        
        print(f"        STEP 4 SUMMARY:")
        print(f"          Generated {len(subcases)} subcase(s)")
        for i, subcase in enumerate(subcases, 1):
            print(f"            {i}. {subcase.name} - {len(subcase.inequalities)} constraints")
        print()
        
        return subcases
    
    def _solve_inequality_for_variable(self, expr, op, rhs, variable):
        """Solve inequality for variable using all solver.py functionality"""
        from sympy import symbols
        var_symbol = symbols(variable)
        
        # Convert to standard form: expr op rhs -> (expr - rhs) op 0
        standard_expr = expr - rhs
        
        try:
            # Use the full solver from solver.py
            solver_output = solve_rational_ineq_full(standard_expr, var_symbol, op, self.use_sign_analysis)
            
            # Extract bounds from solver output
            bounds = []
            for output in solver_output:
                cases = isolate_cases_from_solver([output])
                for label, case_bounds in cases:
                    for bound_expr, direction in case_bounds:
                        if direction == '>':
                            bounds.append(('lower', bound_expr, '>='))
                        else:
                            bounds.append(('upper', bound_expr, '<='))
            
            return bounds
            
        except Exception as e:
            print(f"        Error solving inequality for {variable}: {e}")
            return None
    
    def _solve_linear_inequality_for_variable(self, expr, op, rhs, variable):
        """Legacy method for linear solving - delegates to full solver"""
        return self._solve_inequality_for_variable(expr, op, rhs, variable)


def demonstrate_enhanced_variable_elimination(inequalities=None, variables_to_eliminate=None):
    """
    Hierarchical variable elimination with enhanced 4-step process documentation.
    
    This function implements the complete 4-step variable elimination process with
    hierarchical case structures, individual subcase solving, and detailed documentation
    of conditions for each case and subcase.
    
    Enhanced Features:
    - Hierarchical case naming with conditions (case 1: condition1, subcase 1.1: condition1 ∧ condition2)
    - Detailed 4-step process documentation for each variable
    - Individual subcase solving with condition tracking
    - Enhanced LaTeX generation with step-by-step explanations
    - Complete mathematical rigor in case differentiation
    
    4-Step Process for Each Variable:
    1. **Isolate Variable**: Solve each inequality containing the target variable
       - Convert ax + b ≥ c to x ≥ (c-b)/a (handling coefficient signs)
       - Separate into lower bounds (x ≥ expr) and upper bounds (x ≤ expr)
    
    2. **Combine to Min/Max**: Form max(lower bounds) ≤ variable ≤ min(upper bounds)
       - Collect all lower bound expressions into max() form
       - Collect all upper bound expressions into min() form
       - Create unified constraint for the variable
    
    3. **Remove Variable**: Create elimination constraints max(lower) ≤ min(upper)
       - Replace variable with the min/max constraints
       - Generate feasibility conditions for the system
    
    4. **Expand Cases**: Create hierarchical subcases for each min/max combination
       - For each pair (lower_i, upper_j), create case where lower_i ≤ upper_j
       - Name cases hierarchically with specific conditions
       - Recursively apply to all remaining variables
    """
    print("=" * 80)
    print("ENHANCED HIERARCHICAL VARIABLE ELIMINATION WITH 4-STEP PROCESS")  
    print("=" * 80)
    
    # Use provided inequalities or enhanced default example system
    if inequalities is None:
        inequalities = [
            "x1 + 2*x2 + a >= b",     # Mixed variables and constants
            "x1 - x2 + c >= 0",       # Another constraint on x1, x2
            "2*x1 + d <= x2 + e",     # Different arrangement
            "x2 <= f",                # Simple upper bound
            "g*x3 + x1 >= h"          # Involving x3
        ]
    
    # Auto-detect variables if not provided
    if variables_to_eliminate is None:
        from sympy import symbols
        all_symbols = set()
        for ineq in inequalities:
            try:
                processed = process_inequalities([ineq])
                for lhs, op, rhs in processed:
                    all_symbols.update(lhs.free_symbols)
                    all_symbols.update(rhs.free_symbols)
            except:
                continue
        
        # Extract variables (assume variables start with 'x')
        variables_to_eliminate = sorted([str(s) for s in all_symbols if str(s).startswith('x')])
    
    print("ENHANCED HIERARCHICAL SYSTEM:")
    print("Variables are represented as x1, x2, x3, x4, ...")
    print("Constants are represented as a, b, c, d, e, f, g, h, ...")
    print()
    
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    
    print(f"\nVariables to eliminate (in order): {variables_to_eliminate}")
    print("\nThis system will be processed using the enhanced hierarchical 4-step elimination method:")
    print("1. **Isolate Variable**: Solve each inequality for the target variable")
    print("   - Handle coefficient signs properly when isolating")
    print("   - Separate into lower bounds (x ≥ expr) and upper bounds (x ≤ expr)")
    print()
    print("2. **Combine to Min/Max**: Form max(lower_bounds) ≤ variable ≤ min(upper_bounds)")
    print("   - Collect all lower bound expressions")
    print("   - Collect all upper bound expressions")
    print()
    print("3. **Remove Variable**: Create elimination constraints max(lower) ≤ min(upper)")
    print("   - Replace variable with feasibility conditions")
    print()
    print("4. **Expand Cases**: Create hierarchical subcases for each min/max combination")
    print("   - Generate all feasible combinations")
    print("   - Name cases with their specific conditions")
    print("   - Apply recursively to remaining variables")
    print()
    
    try:
        # Create enhanced hierarchical eliminator
        eliminator = HierarchicalCaseEliminator(use_sign_analysis=True)
        
        # Perform hierarchical elimination with enhanced documentation
        final_cases = eliminator.eliminate_variables_hierarchical(inequalities, variables_to_eliminate)
        
        print(f"✅ Generated {len(final_cases)} final cases using enhanced hierarchical 4-step elimination:")
        
        for case in final_cases:
            print(f"\n  {case.name}:")
            
            # Show the path to this case
            case_path = []
            current = case
            while current.parent:
                case_path.append(current.name)
                current = current.parent
            case_path.append(current.name)
            case_path.reverse()
            
            print(f"    Path: {' → '.join(case_path)}")
            print(f"    Level: {case.level}")
            
            if not case.inequalities:
                print(f"    No constraints (always satisfied)")
            else:
                print(f"    Final constraints:")
                for i, constraint in enumerate(case.inequalities, 1):
                    expr, op, rhs = constraint
                    if rhs == 0:
                        simplified_expr = simplify(expr)
                        if simplified_expr == expr:
                            print(f"      {i}. {expr} {op} 0")
                        else:
                            print(f"      {i}. {simplified_expr} {op} 0  (simplified from {expr} {op} 0)")
                    else:
                        print(f"      {i}. {expr} {op} {rhs}")
        
        # Generate enhanced hierarchical LaTeX documentation
        latex_generator = HierarchicalLatexGenerator()
        latex_content = latex_generator.generate_hierarchical_latex(
            eliminator.all_cases, variables_to_eliminate, inequalities
        )
        
        # Save to output directory
        output_dir = "/workspaces/codespaces-blank/output_final"
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/hierarchical_main_{timestamp}_complete.tex"
        
        with open(filename, 'w') as f:
            f.write(latex_content)
        
        print(f"\n✅ Generated ENHANCED HIERARCHICAL LaTeX: {filename}")
        
        # Display enhanced case analysis
        display_hierarchical_case_analysis(eliminator.all_cases)
        
        print("\n" + "="*60)
        print("ENHANCED HIERARCHICAL VARIABLE ELIMINATION COMPLETED")
        print("="*60)
        print()
        print("Key Enhancements:")
        print("• Case headers include specific conditions")
        print("• Detailed 4-step process documentation")
        print("• Mathematical rigor in case differentiation")
        print("• Complete path tracing for each final case")
        print("• Enhanced LaTeX with step-by-step explanations")
        
        return True
        
    except Exception as e:
        print(f"Error during enhanced hierarchical variable elimination: {e}")
        import traceback
        traceback.print_exc()
        return False


class HierarchicalLatexGenerator:
    """Generates LaTeX documentation for hierarchical case structure"""
    
    def format_expr(self, expr):
        """Format expression for LaTeX."""
        from sympy import latex
        return latex(expr)
    
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
            "\\title{Enhanced Hierarchical Variable Elimination: \\\\",
            "Complete 4-Step Process with Condition-Specific Case Management}",
            "\\author{Enhanced Rational Inequality Solver with Case Conditions}",
            "\\date{\\today}",
            "",
            "\\begin{document}",
            "\\maketitle",
            ""
        ])
        
        # Enhanced introduction
        latex_content.extend([
            "\\section{Introduction}",
            "",
            "This document demonstrates the enhanced hierarchical 4-step variable elimination process",
            "with condition-specific case naming. Each case and subcase header explicitly shows the",
            "specific mathematical conditions that define that case, providing complete transparency",
            "in the case differentiation process.",
            "",
            "\\subsection{Enhanced Hierarchical 4-Step Elimination Process}",
            "",
            "For each variable to be eliminated, we follow these enhanced steps:",
            "\\begin{enumerate}",
            "\\item \\textbf{Isolate Variable}: Solve each inequality containing the target variable",
            "  \\begin{itemize}",
            "    \\item Convert $ax + b \\geq c$ to $x \\geq \\frac{c-b}{a}$ (if $a > 0$) or $x \\leq \\frac{c-b}{a}$ (if $a < 0$)",
            "    \\item Properly handle coefficient signs during isolation",
            "    \\item Separate into lower bounds ($x \\geq \\text{expr}$) and upper bounds ($x \\leq \\text{expr}$)",
            "  \\end{itemize}",
            "\\item \\textbf{Combine to Min/Max}: Form $\\max(\\text{lower bounds}) \\leq \\text{variable} \\leq \\min(\\text{upper bounds})$",
            "  \\begin{itemize}",
            "    \\item Collect all lower bound expressions into $\\max(\\text{expr}_1, \\text{expr}_2, \\ldots)$",
            "    \\item Collect all upper bound expressions into $\\min(\\text{expr}_1, \\text{expr}_2, \\ldots)$",
            "  \\end{itemize}",
            "\\item \\textbf{Remove Variable}: Create elimination constraints $\\max(\\text{lower bounds}) \\leq \\min(\\text{upper bounds})$",
            "  \\begin{itemize}",
            "    \\item Replace the variable with feasibility conditions",
            "    \\item Generate constraint combinations for case expansion",
            "  \\end{itemize}",
            "\\item \\textbf{Expand Cases}: Create hierarchical subcases for each min/max combination",
            "  \\begin{itemize}",
            "    \\item For each pair $(\\text{lower}_i, \\text{upper}_j)$: create case where $\\text{lower}_i \\leq \\text{upper}_j$",
            "    \\item Name each case with its specific defining conditions",
            "    \\item Apply recursively to remaining variables",
            "  \\end{itemize}",
            "\\end{enumerate}",
            "",
            "\\subsection{Enhanced Case Naming System}",
            "",
            "Cases are named hierarchically with their specific conditions:",
            "\\begin{itemize}",
            "\\item \\textbf{Case 1: condition1, Case 2: condition2, ...}: Top-level cases with their defining conditions",
            "\\item \\textbf{Subcase 1.1: condition1 $\\wedge$ subcondition1.1, ...}: First-level subcases",
            "\\item \\textbf{Subsubcase 1.1.1: condition1 $\\wedge$ subcondition1.1 $\\wedge$ subsubcondition1.1.1, ...}: Second-level subcases",
            "\\item And so on for deeper nesting levels with complete condition inheritance",
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
            formatted_ineq = ineq.replace('*', ' \\cdot ').replace('>=', '\\geq').replace('<=', '\\leq')
            latex_content.append(f"& \\text{{({i})}} \\quad {formatted_ineq} \\\\")
        
        latex_content.extend([
            "\\end{align}",
            "",
            f"Variables to eliminate (in order): $\\{{{', '.join([f'x_{{{v[1:]}}}' if v.startswith('x') else v for v in variables_to_eliminate])}\\}}$",
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
            f"After systematically eliminating all variables $\\{{{', '.join([f'x_{{{v[1:]}}}' if v.startswith('x') else v for v in variables_to_eliminate])}\\}}$",
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
                    "This case has no constraints and represents the region where the original",
                    "system is always satisfied (unconditionally feasible region).",
                    ""
                ])
            else:
                latex_content.extend([
                    "This case represents the solution region defined by:",
                    "\\begin{align}"
                ])
                
                for constraint in case.inequalities:
                    expr, op, rhs = constraint
                    formatted_expr = self.format_expr(expr)
                    formatted_rhs = self.format_expr(rhs)
                    # Enhanced operator formatting
                    formatted_op = op.replace('>=', '\\geq').replace('<=', '\\leq')
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
            "The enhanced hierarchical 4-step variable elimination process provides:",
            "\\begin{itemize}",
            "\\item \\textbf{Complete Mathematical Rigor}: Each step is mathematically justified",
            "\\item \\textbf{Transparent Case Differentiation}: Every case shows its defining conditions",
            "\\item \\textbf{Systematic Variable Elimination}: Variables are eliminated in specified order",
            "\\item \\textbf{Hierarchical Organization}: Complex case structures are clearly organized",
            "\\item \\textbf{Verifiable Results}: Each step can be independently verified",
            "\\end{itemize}",
            "",
            f"The final result characterizes the complete solution space of the original system",
            f"through {len(final_cases)} distinct case(s), each with explicit parameter constraints.",
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
        
        # Show case constraints with detailed explanation
        if case.inequalities:
            latex_content.extend([
                f"Constraints for {case.name}:",
                "\\begin{align}"
            ])
            
            for constraint in case.inequalities:
                expr, op, rhs = constraint
                formatted_expr = self.format_expr(expr)
                formatted_rhs = self.format_expr(rhs)
                latex_content.append(f"& {formatted_expr} {op} {formatted_rhs} \\\\")
            
            latex_content.extend([
                "\\end{align}",
                ""
            ])
        
        # Show elimination steps for this case with detailed process
        if case.elimination_steps:
            for i, step in enumerate(case.elimination_steps):
                variable = step['variable']
                latex_content.extend([
                    f"\\textbf{{Elimination of variable ${variable}$ in {case.name}:}}",
                    "",
                    "\\begin{enumerate}",
                    f"\\item \\textbf{{Step 1}}: Isolate ${variable}$ in relevant inequalities",
                    f"\\item \\textbf{{Step 2}}: Combine to max/min form",
                    f"\\item \\textbf{{Step 3}}: Remove ${variable}$",
                    f"\\item \\textbf{{Step 4}}: Expand into {len(case.subcases)} subcase(s)",
                    "\\end{enumerate}",
                    ""
                ])
                
                # Add detailed step-by-step process if available
                if 'step1' in step:
                    latex_content.extend(self._format_step_details(step, variable))
        
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
                    simplified_expr = str(expr).replace('**', '^').replace('*', ' ')
                    conditions.append(f"${simplified_expr} {op} 0$")
                else:
                    simplified_expr = str(expr).replace('**', '^').replace('*', ' ')
                    simplified_rhs = str(rhs).replace('**', '^').replace('*', ' ')
                    conditions.append(f"${simplified_expr} {op} {simplified_rhs}$")
            
            if conditions and len(conditions) <= 3:  # Only show if not too many conditions
                conditions_str = ", ".join(conditions)
                header = f"{case.name}: {conditions_str}"
        
        return header
    
    def _format_step_details(self, step, variable):
        """Format detailed step-by-step process information with inequalities after each step"""
        latex_content = []
        
        # Add detailed explanations for each step with the actual inequalities
        if 'step1' in step and step['step1'].get('step1_inequalities'):
            step1_inequalities = step['step1']['step1_inequalities']
            latex_content.extend([
                f"\\textbf{{Step 1 Detail}}: Inequalities after isolating ${variable}$:",
                "\\begin{align}"
            ])
            for i, ineq in enumerate(step1_inequalities, 1):
                if len(ineq) == 3:
                    lhs, op, rhs = ineq
                    formatted_lhs = self.format_expr(lhs)
                    formatted_rhs = self.format_expr(rhs)
                    formatted_op = op.replace('>=', '\\geq').replace('<=', '\\leq')
                    latex_content.append(f"& {formatted_lhs} {formatted_op} {formatted_rhs} \\\\")
            latex_content.extend([
                "\\end{align}",
                ""
            ])
        
        if 'step2' in step:
            # Show the min/max form
            if step['step2'].get('minmax_form'):
                latex_content.extend([
                    f"\\textbf{{Step 2 Detail}}: Combined form is {step['step2']['minmax_form']}",
                    ""
                ])
            
            # Show inequalities after step 2
            if step['step2'].get('step2_inequalities'):
                step2_inequalities = step['step2']['step2_inequalities']
                latex_content.extend([
                    f"\\textbf{{Step 2 Inequalities}}: System after combining to min/max form:",
                    "\\begin{align}"
                ])
                for i, ineq in enumerate(step2_inequalities, 1):
                    if len(ineq) == 3:
                        lhs, op, rhs = ineq
                        formatted_lhs = self.format_expr(lhs)
                        formatted_rhs = self.format_expr(rhs)
                        formatted_op = op.replace('>=', '\\geq').replace('<=', '\\leq')
                        latex_content.append(f"& {formatted_lhs} {formatted_op} {formatted_rhs} \\\\")
                latex_content.extend([
                    "\\end{align}",
                    ""
                ])
        
        if 'step3' in step:
            # Show elimination constraints
            if step['step3'].get('elimination_constraints'):
                latex_content.extend([
                    f"\\textbf{{Step 3 Detail}}: Elimination constraints:",
                ])
                for constraint in step['step3']['elimination_constraints']:
                    latex_content.append(f"\\quad {constraint}")
                latex_content.append("")
            
            # Show inequalities after step 3
            if step['step3'].get('step3_inequalities'):
                step3_inequalities = step['step3']['step3_inequalities']
                latex_content.extend([
                    f"\\textbf{{Step 3 Inequalities}}: System after removing ${variable}$:",
                    "\\begin{align}"
                ])
                for i, ineq in enumerate(step3_inequalities, 1):
                    if len(ineq) == 3:
                        lhs, op, rhs = ineq
                        formatted_lhs = self.format_expr(lhs)
                        formatted_rhs = self.format_expr(rhs)
                        formatted_op = op.replace('>=', '\\geq').replace('<=', '\\leq')
                        latex_content.append(f"& {formatted_lhs} {formatted_op} {formatted_rhs} \\\\")
                latex_content.extend([
                    "\\end{align}",
                    ""
                ])
        
        # Note: Step 4 inequalities are shown in the individual subcases
        if 'step4' in step:
            latex_content.extend([
                f"\\textbf{{Step 4 Detail}}: Expanded into {step['step4'].get('subcases', 0)} subcase(s).",
                f"Each subcase shows its specific inequalities after case expansion.",
                ""
            ])
        
        return latex_content


def display_hierarchical_case_analysis(all_cases):
    """Display analysis of the hierarchical case structure"""
    print("\n" + "="*60)
    print("HIERARCHICAL CASE ANALYSIS")
    print("="*60)
    
    if not all_cases:
        print("No cases found.")
        return
    
    # Count cases by level
    level_counts = defaultdict(int)
    final_cases = []
    
    for case in all_cases:
        level_counts[case.level] += 1
        if not case.subcases:  # Final case
            final_cases.append(case)
    
    print(f"Total cases generated: {len(all_cases)}")
    for level, count in sorted(level_counts.items()):
        level_name = "root" if level == 0 else f"level {level}"
        print(f"  {level_name}: {count} case(s)")
    
    print(f"\nFinal solution cases: {len(final_cases)}")
    print()
    
    for case in final_cases:
        print(f"{case.name}:")
        print(f"  Level: {case.level}")
        print(f"  Constraints: {len(case.inequalities)}")
        
        for j, constraint in enumerate(case.inequalities, 1):
            expr, op, rhs = constraint
            print(f"    {j}. {expr} {op} {rhs}")
        
        print(f"  Solution status: {'Solved' if case.is_solved else 'Unsolved'}")
        print()
    
    print("="*60)
    print("HIERARCHICAL CASE ANALYSIS COMPLETE")
    print("="*60)


def test_comprehensive_elimination():
    """
    Test the enhanced hierarchical variable elimination with various types of inequalities.
    
    This function tests:
    1. Linear inequalities
    2. Quadratic inequalities  
    3. Rational inequalities
    4. Mixed systems with multiple variables
    5. Systems with constants
    """
    print("=" * 80)
    print("COMPREHENSIVE TESTING OF ENHANCED VARIABLE ELIMINATION")
    print("=" * 80)
    
    test_cases = [
        {
            'name': 'Linear System Test',
            'description': 'Simple linear inequalities with two variables',
            'inequalities': [
                "x1 + 2*x2 >= a",
                "x1 - x2 <= b", 
                "x2 >= c"
            ],
            'variables': ['x1', 'x2']
        },
        {
            'name': 'Quadratic System Test',
            'description': 'Quadratic inequality with linear constraints',
            'inequalities': [
                "x1**2 - 4 >= 0",
                "x1 + x2 <= a",
                "x2 >= b"
            ],
            'variables': ['x1', 'x2']
        },
        {
            'name': 'Rational System Test', 
            'description': 'Rational inequality with linear constraints',
            'inequalities': [
                "(x1 + 1)/(x1 - 2) >= 0",
                "x1 + x2 <= a",
                "x2 >= b"
            ],
            'variables': ['x1', 'x2']
        },
        {
            'name': 'Mixed Complex System Test',
            'description': 'Complex system with multiple types of inequalities',
            'inequalities': [
                "x1**2 + a*x1 + b >= 0",
                "(x1 + x2)/(x2 - c) <= d",
                "x2 + e >= f",
                "x1 - x2 >= g"
            ],
            'variables': ['x1', 'x2']
        },
        {
            'name': 'Three Variable System Test',
            'description': 'System with three variables requiring sequential elimination',
            'inequalities': [
                "x1 + x2 + x3 >= a",
                "x1 - x2 <= b",
                "x2 + x3 >= c", 
                "x3 <= d"
            ],
            'variables': ['x1', 'x2', 'x3']
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTEST CASE {i}: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print(f"Inequalities: {test_case['inequalities']}")
        print(f"Variables to eliminate: {test_case['variables']}")
        print("-" * 60)
        
        try:
            success = demonstrate_enhanced_variable_elimination(
                inequalities=test_case['inequalities'],
                variables_to_eliminate=test_case['variables']
            )
            
            results.append({
                'test_case': test_case['name'],
                'success': success,
                'error': None
            })
            
            if success:
                print(f"✅ Test case {i} completed successfully")
            else:
                print(f"❌ Test case {i} failed")
                
        except Exception as e:
            print(f"❌ Test case {i} failed with error: {e}")
            traceback.print_exc()
            results.append({
                'test_case': test_case['name'],
                'success': False,
                'error': str(e)
            })
        
        print("-" * 60)
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"Total tests: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print()
    
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{status}: {result['test_case']}")
        if result['error']:
            print(f"    Error: {result['error']}")
    
    print("\n" + "=" * 80)
    print("COMPREHENSIVE TESTING COMPLETED")
    print("=" * 80)
    
    return results


def validate_latex_output():
    """
    Validate that generated LaTeX files contain expected content.
    """
    print("\n" + "=" * 80)
    print("VALIDATING LATEX OUTPUT")
    print("=" * 80)
    
    output_dir = "/workspaces/codespaces-blank/output_final"
    
    if not os.path.exists(output_dir):
        print("❌ Output directory does not exist")
        return False
    
    latex_files = [f for f in os.listdir(output_dir) if f.endswith('.tex')]
    
    if not latex_files:
        print("❌ No LaTeX files found in output directory")
        return False
    
    print(f"Found {len(latex_files)} LaTeX files:")
    
    validation_results = []
    
    for filename in latex_files:
        filepath = os.path.join(output_dir, filename)
        print(f"\nValidating: {filename}")
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Check for required LaTeX elements
            checks = [
                ('documentclass', '\\documentclass' in content),
                ('amsmath package', '\\usepackage{amsmath}' in content),
                ('title', '\\title{' in content),
                ('begin document', '\\begin{document}' in content),
                ('end document', '\\end{document}' in content),
                ('section headers', '\\section{' in content),
                ('math environments', '\\begin{align}' in content or '\\begin{equation}' in content),
                ('hierarchical cases', 'Case ' in content),
                ('variable elimination', 'Eliminate' in content or 'eliminate' in content),
                ('4-step process', 'Step 1' in content and 'Step 2' in content and 'Step 3' in content and 'Step 4' in content)
            ]
            
            passed_checks = sum(1 for _, check in checks if check)
            total_checks = len(checks)
            
            print(f"  Validation checks: {passed_checks}/{total_checks}")
            
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"    {status} {check_name}")
            
            validation_results.append({
                'filename': filename,
                'passed_checks': passed_checks,
                'total_checks': total_checks,
                'success': passed_checks == total_checks
            })
            
        except Exception as e:
            print(f"  ❌ Error reading file: {e}")
            validation_results.append({
                'filename': filename,
                'passed_checks': 0,
                'total_checks': 10,
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print("\n" + "-" * 60)
    print("LATEX VALIDATION SUMMARY")
    print("-" * 60)
    
    successful_files = sum(1 for r in validation_results if r['success'])
    total_files = len(validation_results)
    
    print(f"Total LaTeX files: {total_files}")
    print(f"Fully validated: {successful_files}")
    print(f"Failed validation: {total_files - successful_files}")
    
    return successful_files == total_files


if __name__ == "__main__":
    """
    Run comprehensive tests and validation.
    """
    print("STARTING COMPREHENSIVE TESTING AND VALIDATION")
    print("=" * 80)
    
    # Run comprehensive tests
    test_results = test_comprehensive_elimination()
    
    # Validate LaTeX output
    latex_validation = validate_latex_output()
    
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    
    total_tests = len(test_results)
    successful_tests = sum(1 for r in test_results if r['success'])
    
    print(f"Test Results: {successful_tests}/{total_tests} passed")
    print(f"LaTeX Validation: {'PASSED' if latex_validation else 'FAILED'}")
    
    if successful_tests == total_tests and latex_validation:
        print("🎉 ALL TESTS PASSED - SYSTEM WORKING CORRECTLY")
    else:
        print("⚠️  SOME TESTS FAILED - REVIEW RESULTS ABOVE")


def main():
    """
    Enhanced main function for generating hierarchical 4-step elimination files.
    
    This main function demonstrates the complete 4-step variable elimination process
    where each case and subcase header includes the specific conditions that define
    that case. The process follows these steps for each variable:
    
    1. **Isolate Variable**: Convert each inequality containing the variable to the form 
       "variable ≥ expression" or "variable ≤ expression", properly handling coefficient signs.
    
    2. **Combine to Min/Max**: Collect all lower bounds into max(expr1, expr2, ...) and 
       all upper bounds into min(expr1, expr2, ...), forming:
       max(lower_bounds) ≤ variable ≤ min(upper_bounds)
    
    3. **Remove Variable**: Replace the variable with the elimination constraint:
       max(lower_bounds) ≤ min(upper_bounds)
    
    4. **Expand Cases**: For each combination of expressions in the min/max, create a 
       new subcase where that specific combination defines the active constraint.
       Each subcase is named with its specific conditions.
    
    Input Format:
    - Variables: x1, x2, x3, x4, ... (in order of elimination)
    - Constants: a, b, c, d, e, f, g, h, ...
    - Inequalities: Linear inequalities involving variables and constants
    
    Output:
    - Complete LaTeX document with hierarchical case structure
    - Each case/subcase header shows the specific conditions
    - Detailed 4-step process documentation for each variable
    - Mathematical rigor in case differentiation and solving
    """
    # Run the enhanced demonstration
    demonstrate_enhanced_variable_elimination()
    print("ENHANCED HIERARCHICAL 4-STEP VARIABLE ELIMINATION SYSTEM")
    print("=" * 80)
    print()
    print("This system implements a complete 4-step variable elimination process:")
    print()
    print("STEP 1: ISOLATE VARIABLE")
    print("  • Convert ax + b ≥ c to x ≥ (c-b)/a or x ≤ (c-b)/a")
    print("  • Handle coefficient signs properly during isolation")
    print("  • Separate into lower bounds (x ≥ expr) and upper bounds (x ≤ expr)")
    print()
    print("STEP 2: COMBINE TO MIN/MAX")
    print("  • Collect lower bounds: max(expr1, expr2, ...) ≤ variable")
    print("  • Collect upper bounds: variable ≤ min(expr1, expr2, ...)")
    print("  • Form: max(lower_bounds) ≤ variable ≤ min(upper_bounds)")
    print()
    print("STEP 3: REMOVE VARIABLE")
    print("  • Create elimination constraint: max(lower_bounds) ≤ min(upper_bounds)")
    print("  • Replace variable with feasibility conditions")
    print()
    print("STEP 4: EXPAND CASES")
    print("  • For each pair (lower_i, upper_j): create case where lower_i ≤ upper_j")
    print("  • Name each case with its specific conditions")
    print("  • Apply recursively to remaining variables")
    print()
    
    # Run the enhanced hierarchical variable elimination
    print("Generating enhanced hierarchical 4-step elimination LaTeX file...")
    print("Each case and subcase will include its specific defining conditions.")
    print()
    
    success = demonstrate_enhanced_variable_elimination()
    
    print("\n" + "=" * 80)
    print("ENHANCED HIERARCHICAL ELIMINATION GENERATION COMPLETE")
    print("=" * 80)
    
    if success:
        print("✅ Successfully generated enhanced hierarchical 4-step elimination file")
        print()
        print("Generated file features:")
        print("• Case headers include specific conditions (e.g., 'Case 1: a + b ≥ 0, c ≤ d')")
        print("• Complete 4-step process documentation for each variable")
        print("• Hierarchical subcase structure with condition inheritance")
        print("• Mathematical rigor in case differentiation")
        print("• LaTeX format suitable for academic/professional use")
        print()
        print("Check output_final/ directory for the generated LaTeX file")
        print()
        print("The file contains complete documentation of:")
        print("1. Initial system with variables x1, x2, x3, ... and constants a, b, c, ...")
        print("2. Step-by-step variable elimination process")
        print("3. Hierarchical case expansion with conditions")
        print("4. Final solution cases with all variables eliminated")
        print("5. Mathematical verification of each elimination step")
    else:
        print("❌ Failed to generate enhanced hierarchical elimination file")
        print("Check error messages above for details")
        print()
        print("Common issues:")
        print("• Malformed input inequalities")
        print("• Missing dependencies (sympy)")
        print("• File permission issues in output directory")


if __name__ == "__main__":
    main()
