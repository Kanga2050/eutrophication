"""
Core Variable Elimination Engine for Hierarchical Variable Elimination

This module implements the main HierarchicalCaseEliminator class that provides
the 4-step variable elimination process with hierarchical case management.
All results are treated as inequalities within cases - no constraint/inequality separation.

Classes:
- HierarchicalCaseEliminator: Main elimination engine with 4-step process

Author: Simplified Rational Inequality Solver Team
Version: Pure Inequality System - No Constraint/Inequality Separation
"""
from sympy import symbols, simplify, solve, latex, Max, Min, sympify, S
import traceback
from collections import defaultdict

from case_system import CaseNamingSystem, HierarchicalCase
from input_processor import process_inequalities
from sign_analyzer import create_default_analyzer


class HierarchicalCaseEliminator:
    """Implements 4-step variable elimination with hierarchical case management - inequalities only"""
    
    def __init__(self, use_sign_analysis=True):
        self.naming_system = CaseNamingSystem()
        self.all_cases = []
        self.elimination_log = []
        self.elimination_steps = {}  # Store detailed step information for LaTeX generation
        self.use_sign_analysis = use_sign_analysis
        self.sign_analyzer = create_default_analyzer() if use_sign_analysis else None
        
        # Add positive assumptions for common variables and constants
        if self.sign_analyzer:
            # Assume all single-letter variables and constants are positive
            common_vars = ['x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'u', 'v', 'w']
            for var in common_vars:
                self.sign_analyzer.add_assumption(var, 'positive')
            print(f"        Sign analyzer configured with positive assumptions for: {', '.join(common_vars)}")
    
    def _check_inequality_validity(self, inequality):
        """
        Check if an inequality is valid, removing impossible cases and tautologies.
        Enhanced with sign analysis for positive variable assumptions.
        
        Args:
            inequality: Tuple of (lhs, op, rhs)
            
        Returns:
            'valid', 'tautology', or 'impossible'
        """
        lhs, op, rhs = inequality
        
        try:
            # Convert to SymPy expressions
            lhs_sym = sympify(lhs) if isinstance(lhs, str) else lhs
            rhs_sym = sympify(rhs) if isinstance(rhs, str) else rhs
            
            # Check if both sides are numbers
            lhs_val = None
            rhs_val = None
            
            try:
                lhs_val = float(lhs_sym)
                rhs_val = float(rhs_sym)
            except (TypeError, ValueError):
                # One or both sides are not numeric
                pass
            
            # If both sides are numeric, evaluate directly
            if lhs_val is not None and rhs_val is not None:
                if op == '<=':
                    if lhs_val <= rhs_val:
                        print(f"          TAUTOLOGY: {lhs_val} <= {rhs_val} is always true")
                        return 'tautology'
                    else:
                        print(f"          IMPOSSIBLE: {lhs_val} <= {rhs_val} is always false")
                        return 'impossible'
                elif op == '>=':
                    if lhs_val >= rhs_val:
                        print(f"          TAUTOLOGY: {lhs_val} >= {rhs_val} is always true")
                        return 'tautology'
                    else:
                        print(f"          IMPOSSIBLE: {lhs_val} >= {rhs_val} is always false")
                        return 'impossible'
                elif op == '<':
                    if lhs_val < rhs_val:
                        print(f"          TAUTOLOGY: {lhs_val} < {rhs_val} is always true")
                        return 'tautology'
                    else:
                        print(f"          IMPOSSIBLE: {lhs_val} < {rhs_val} is always false")
                        return 'impossible'
                elif op == '>':
                    if lhs_val > rhs_val:
                        print(f"          TAUTOLOGY: {lhs_val} > {rhs_val} is always true")
                        return 'tautology'
                    else:
                        print(f"          IMPOSSIBLE: {lhs_val} > {rhs_val} is always false")
                        return 'impossible'
            
            # Enhanced sign analysis with positive assumptions
            if self.sign_analyzer:
                # Check if lhs - rhs has a definite sign
                diff_expr = lhs_sym - rhs_sym
                sign = self.sign_analyzer.analyze_sign(diff_expr)
                
                if sign == 'positive':
                    # lhs > rhs always
                    if op in ['>', '>=']:
                        print(f"          TAUTOLOGY: {lhs} > {rhs} (sign analysis)")
                        return 'tautology'
                    elif op in ['<', '<=']:
                        print(f"          IMPOSSIBLE: {lhs} < {rhs} when {lhs} > {rhs} (sign analysis)")
                        return 'impossible'
                elif sign == 'negative':
                    # lhs < rhs always
                    if op in ['<', '<=']:
                        print(f"          TAUTOLOGY: {lhs} < {rhs} (sign analysis)")
                        return 'tautology'
                    elif op in ['>', '>=']:
                        print(f"          IMPOSSIBLE: {lhs} > {rhs} when {lhs} < {rhs} (sign analysis)")
                        return 'impossible'
                elif sign == 'zero':
                    # lhs = rhs always
                    if op in ['<=', '>=']:
                        print(f"          TAUTOLOGY: {lhs} = {rhs} (sign analysis)")
                        return 'tautology'
                    elif op in ['<', '>']:
                        print(f"          IMPOSSIBLE: {lhs} != {rhs} when {lhs} = {rhs} (sign analysis)")
                        return 'impossible'
                
                # Special case: check for impossible orderings with positive assumptions
                # e.g., if a > 0, b > 0, c > 0, d > 0, then some combinations are impossible
                if self._check_positive_variable_contradictions(lhs_sym, op, rhs_sym):
                    print(f"          IMPOSSIBLE: {lhs} {op} {rhs} contradicts positive variable assumptions")
                    return 'impossible'
            
            return 'valid'
            
        except Exception as e:
            print(f"          Warning: Could not check inequality validity: {e}")
            return 'valid'
    
    def _check_positive_variable_contradictions(self, lhs, op, rhs):
        """
        Check for contradictions that arise from positive variable assumptions.
        Returns True if the inequality is impossible given positive assumptions.
        """
        try:
            # Look for patterns like 'a >= a' which should be tautologies, not kept
            if lhs == rhs:
                if op in ['<=', '>=']:
                    return False  # This should be caught as tautology above
                elif op in ['<', '>']:
                    return True   # x < x or x > x is impossible
            
            # Check for obviously contradictory patterns
            # E.g., if we have both 'a >= b' and 'b >= a' in the same case, 
            # this implies a = b, which might create contradictions with strict inequalities
            
            return False  # For now, let the sign analyzer handle most cases
            
        except Exception:
            return False
    
    def _filter_inequalities(self, inequalities):
        """
        Filter inequalities, removing impossible ones and noting tautologies.
        
        Args:
            inequalities: List of (lhs, op, rhs) tuples
            
        Returns:
            Tuple of (filtered_inequalities, is_impossible_case)
        """
        filtered = []
        is_impossible = False
        
        print(f"        Checking {len(inequalities)} inequalities for validity...")
        
        for i, inequality in enumerate(inequalities):
            lhs, op, rhs = inequality
            print(f"          Inequality {i+1}: {lhs} {op} {rhs}")
            
            validity = self._check_inequality_validity(inequality)
            
            if validity == 'impossible':
                print(f"          -> Case is IMPOSSIBLE due to this inequality")
                is_impossible = True
                break  # No need to check other inequalities
            elif validity == 'tautology':
                print(f"          -> Inequality is always true, removing from case")
                # Don't add tautologies to the filtered list
            else:
                print(f"          -> Inequality is valid, keeping")
                filtered.append(inequality)
        
        print(f"        Result: {len(filtered)} inequalities remain, impossible={is_impossible}")
        return filtered, is_impossible
    
    def eliminate_variables_hierarchical(self, inequalities, variables_to_eliminate):
        """
        Main elimination function with hierarchical case management - inequalities only
        """
        print("=" * 80)
        print("HIERARCHICAL VARIABLE ELIMINATION WITH 4-STEP PROCESS")
        print("ALL RESULTS ARE INEQUALITIES - NO CONSTRAINT/INEQUALITY SEPARATION")
        print("=" * 80)
        
        # Initialize with the root case
        processed_ineqs = process_inequalities(inequalities)
        
        # Filter initial inequalities
        filtered_ineqs, is_impossible = self._filter_inequalities(processed_ineqs)
        
        if is_impossible:
            print("SYSTEM IS IMPOSSIBLE: Initial inequalities are contradictory")
            print("No solution exists for this system")
            return []
        
        print(f"Initial system: {len(filtered_ineqs)} inequalities (after filtering)")
        for i, (lhs, op, rhs) in enumerate(filtered_ineqs):
            print(f"  {i+1}. {lhs} {op} {rhs}")
        print()
        
        root_name, root_id = self.naming_system.get_case_name()
        root_case = HierarchicalCase(root_name, root_id, filtered_ineqs, level=0)
        
        current_cases = [root_case]
        self.all_cases = [root_case]
        
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
                    print(f"    -> Generated {subcase.name}: {len(subcase.inequalities)} inequalities")
            
            current_cases = new_cases
            print(f"\nAfter eliminating '{variable}': {len(current_cases)} total case(s)")
            print()
        
        return current_cases
    
    def eliminate_variable_4_step_hierarchical(self, parent_case, variable):
        """
        4-step elimination for a single case with hierarchical subcase generation
        """
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
        
        # Store detailed step information for LaTeX generation with ALL inequalities at each step
        self.elimination_steps[variable] = {
            'isolate': {
                'all_inequalities': [f"{ineq[0]} {ineq[1]} {ineq[2]}" for ineq in step1_result.get('step1_inequalities', [])],
                'isolated_inequalities': [f"{ineq[0]} {ineq[1]} {ineq[2]}" for ineq in step1_result.get('isolated_inequalities', [])],
                'non_involving_inequalities': [f"{ineq[0]} {ineq[1]} {ineq[2]}" for ineq in step1_result.get('not_involving_var', [])]
            },
            'combine': {
                'combined_constraint': step2_result.get('combined_constraint', f"{variable} bounds combined"),
                'all_constraints_after_combine': step2_result.get('all_constraints_after_combine', [])
            },
            'remove': {
                'elimination_constraints': [f"{constraint[0]} {constraint[1]} {constraint[2]}" if isinstance(constraint, tuple) and len(constraint) == 3 else str(constraint) for constraint in step3_result.get('elimination_constraints', [])],
                'all_constraints_after_remove': [f"{ineq[0]} {ineq[1]} {ineq[2]}" if isinstance(ineq, tuple) and len(ineq) == 3 else str(ineq) for ineq in step3_result.get('all_constraints_after_remove', [])]
            },
            'expand': {
                'subcases': [],
                'final_cases': []
            }
        }
        
        # Capture detailed information for each generated subcase
        for i, subcase in enumerate(subcases):
            case_info = {
                'case_name': subcase.name,
                'case_level': subcase.level,
                'inequalities': [f"{ineq[0]} {ineq[1]} {ineq[2]}" if isinstance(ineq, tuple) and len(ineq) == 3 else str(ineq) for ineq in subcase.inequalities]
            }
            self.elimination_steps[variable]['expand']['subcases'].append(case_info)
        
        return subcases
    
    def _step1_isolate_variable_hierarchical(self, case, variable):
        """Step 1: Isolate variable in each inequality"""
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
            # Convert to SymPy expressions if they're strings
            if isinstance(expr, str):
                expr_sym = sympify(expr)
            else:
                expr_sym = expr
                
            # Ensure expr_sym is a SymPy expression with free_symbols attribute
            if not hasattr(expr_sym, 'free_symbols'):
                # If it's a number or other non-symbolic type, convert to SymPy
                expr_sym = sympify(expr_sym)
                
            # Check if expression contains the variable
            if var_symbol in expr_sym.free_symbols:
                involving_var.append(ineq)
                print(f"        Inequality {i+1}: {expr} {op} {rhs}")
                print(f"          Contains variable {variable}, proceeding with isolation...")
                
                # Show the detailed isolation work
                original_eq = f"{expr} {op} {rhs}"
                print(f"          Original: {original_eq}")
                
                # Use the full solver to handle all types of inequalities
                bound_results = self._solve_inequality_for_variable(expr, op, rhs, variable)
                
                # Convert bounds to inequalities
                for bound_type, bound_expr, bound_op in bound_results:
                    if bound_type == 'lower':
                        # Lower bound: x >= bound_expr  
                        isolated_ineq = (var_symbol, bound_op, bound_expr)
                        print(f"          -> Lower bound: {variable} {bound_op} {bound_expr}")
                    else:  # upper bound
                        # Upper bound: x <= bound_expr
                        isolated_ineq = (var_symbol, bound_op, bound_expr)
                        print(f"          -> Upper bound: {variable} {bound_op} {bound_expr}")
                    
                    isolated_inequalities.append(isolated_ineq)
                    step1_inequalities.append(isolated_ineq)
                
                print()
            else:
                not_involving_var.append(ineq)
                step1_inequalities.append(ineq)  # These stay the same
                print(f"        Inequality {i+1}: {expr} {op} {rhs}")
                print(f"          Does not contain {variable}, keeping as-is")
                print()
        
        print(f"        STEP 1 SUMMARY:")
        print(f"          Inequalities involving {variable}: {len(involving_var)}")
        print(f"          Inequalities not involving {variable}: {len(not_involving_var)}")
        print(f"          Generated isolated inequalities: {len(isolated_inequalities)}")
        print(f"          Total inequalities after Step 1: {len(step1_inequalities)}")
        print()
        
        return {
            'involving_var': involving_var,
            'not_involving_var': not_involving_var,
            'isolated_inequalities': isolated_inequalities,
            'all_inequalities': step1_inequalities,
            'step1_inequalities': step1_inequalities  # For LaTeX generation
        }
    
    def _step2_combine_to_minmax_hierarchical(self, step1_result, variable):
        """Step 2: Combine bounds to min/max expressions"""
        print(f"      STEP 2: Combine to min/max")
        print(f"        Goal: Group bounds into max(lower_bounds) ≤ {variable} ≤ min(upper_bounds)")
        print()
        
        isolated_inequalities = step1_result['isolated_inequalities']
        lower_bounds = []
        upper_bounds = []
        
        for var_expr, op, bound_expr in isolated_inequalities:
            if op in ['>=', '>']:
                lower_bounds.append((bound_expr, op))
                print(f"        Lower bound: {variable} {op} {bound_expr}")
            elif op in ['<=', '<']:
                upper_bounds.append((bound_expr, op))
                print(f"        Upper bound: {variable} {op} {bound_expr}")
        
        print()
        print(f"        Found {len(lower_bounds)} lower bound(s) and {len(upper_bounds)} upper bound(s)")
        
        # Create min/max expressions
        if lower_bounds:
            if len(lower_bounds) == 1:
                max_expr = lower_bounds[0][0]
                max_op = lower_bounds[0][1]
                print(f"        Max of lower bounds: max({max_expr}) = {max_expr}")
            else:
                exprs = [expr for expr, op in lower_bounds]
                max_expr = Max(*exprs)
                max_op = '>=' if any(op == '>' for expr, op in lower_bounds) else '>='
                print(f"        Max of lower bounds: max({', '.join(map(str, exprs))}) = {max_expr}")
        else:
            max_expr = None
            max_op = None
            print(f"        No lower bounds")
        
        if upper_bounds:
            if len(upper_bounds) == 1:
                min_expr = upper_bounds[0][0]
                min_op = upper_bounds[0][1]
                print(f"        Min of upper bounds: min({min_expr}) = {min_expr}")
            else:
                exprs = [expr for expr, op in upper_bounds]
                min_expr = Min(*exprs)
                min_op = '<=' if any(op == '<' for expr, op in upper_bounds) else '<='
                print(f"        Min of upper bounds: min({', '.join(map(str, exprs))}) = {min_expr}")
        else:
            min_expr = None
            min_op = None
            print(f"        No upper bounds")
        
        # Create combined constraint
        if max_expr is not None and min_expr is not None:
            combined_constraint = f"max({max_expr}) {max_op} {variable} {min_op} min({min_expr})"
            print(f"        Combined constraint: {combined_constraint}")
        elif max_expr is not None:
            combined_constraint = f"{variable} {max_op} {max_expr}"
            print(f"        Combined constraint: {combined_constraint}")
        elif min_expr is not None:
            combined_constraint = f"{variable} {min_op} {min_expr}"
            print(f"        Combined constraint: {combined_constraint}")
        else:
            combined_constraint = "No bounds on " + variable
            print(f"        Combined constraint: {combined_constraint}")
        
        print()
        # Generate step2 inequalities for LaTeX documentation
        step2_inequalities = []
        step2_inequalities.extend(step1_result['not_involving_var'])  # Non-involving inequalities
        
        # Don't add the combined constraint as a tuple - it will be handled separately
        
        return {
            'lower_bounds': lower_bounds,
            'upper_bounds': upper_bounds,
            'max_expr': max_expr,
            'min_expr': min_expr,
            'max_op': max_op,
            'min_op': min_op,
            'combined_constraint': combined_constraint,
            'not_involving_var': step1_result['not_involving_var'],
            'step2_inequalities': step2_inequalities,  # For LaTeX generation
            'all_constraints_after_combine': step2_inequalities,  # Complete constraint set after step 2
            'minmax_form': combined_constraint  # For LaTeX generation
        }
    
    def _step3_remove_variable_hierarchical(self, step2_result, variable):
        """Step 3: Remove variable by creating elimination constraints"""
        print(f"      STEP 3: Remove variable {variable}")
        print(f"        Goal: Create elimination constraints from max(lower) ≤ min(upper)")
        print()
        
        max_expr = step2_result['max_expr']
        min_expr = step2_result['min_expr']
        
        elimination_constraints = []
        
        if max_expr is not None and min_expr is not None:
            # Create constraint: max_expr <= min_expr
            elimination_constraint = (max_expr, '<=', min_expr)
            elimination_constraints.append(elimination_constraint)
            print(f"        Elimination constraint: {max_expr} <= {min_expr}")
            print(f"        This ensures the bounds are consistent")
        else:
            print(f"        No elimination constraint needed (only one-sided bounds)")
        
        # Include inequalities not involving the variable
        remaining_inequalities = list(step2_result['not_involving_var'])
        
        print(f"        Inequalities not involving {variable}: {len(remaining_inequalities)}")
        for i, (expr, op, rhs) in enumerate(remaining_inequalities, 1):
            print(f"          {i}. {expr} {op} {rhs}")
        
        # Combine all constraints
        all_constraints = elimination_constraints + remaining_inequalities
        
        print(f"        Total constraints after removing {variable}: {len(all_constraints)}")
        for i, (lhs, op, rhs) in enumerate(all_constraints, 1):
            print(f"          {i}. {lhs} {op} {rhs}")
        print()
        
        return {
            'elimination_constraints': elimination_constraints,
            'remaining_inequalities': remaining_inequalities,
            'all_constraints': all_constraints,
            'all_constraints_after_remove': all_constraints,  # Complete constraint set after step 3
            'lower_bounds': step2_result['lower_bounds'],
            'upper_bounds': step2_result['upper_bounds'],
            'step3_inequalities': all_constraints  # For LaTeX generation
        }
    
    def _step4_expand_cases_hierarchical(self, step3_result, variable, parent_case):
        """Step 4: Expand cases for different min/max combinations"""
        print(f"      STEP 4: Expand cases")
        print(f"        Goal: Create hierarchical subcases for min/max combinations")
        print()
        
        lower_bounds = step3_result['lower_bounds']
        upper_bounds = step3_result['upper_bounds']
        remaining_inequalities = step3_result['remaining_inequalities']
        elimination_constraints = step3_result['elimination_constraints']
        
        subcases = []
        
        # Check if we need to expand Max/Min expressions
        if len(lower_bounds) <= 1 and len(upper_bounds) <= 1:
            # Simple case: no case expansion needed
            print(f"        Simple case: {len(lower_bounds)} lower, {len(upper_bounds)} upper bounds")
            
            all_constraints = elimination_constraints + remaining_inequalities
            filtered_constraints, is_impossible = self._filter_inequalities(all_constraints)
            
            if not is_impossible:
                subcase_name, subcase_id = self.naming_system.get_case_name(
                    parent_case.name, parent_case.level + 1, force_single_case=True
                )
                
                subcase = HierarchicalCase(
                    subcase_name, subcase_id, filtered_constraints, 
                    parent=parent_case, level=parent_case.level + 1
                )
                
                parent_case.add_subcase(subcase)
                subcases.append(subcase)
                
                print(f"            Generated {subcase_name}")
                print(f"            No case expansion needed")
                print(f"            Simply carrying over non-involving constraints")
                print(f"            INEQUALITIES AFTER STEP 4 (filtered):")
                for k, ineq in enumerate(filtered_constraints, 1):
                    if len(ineq) == 3:
                        lhs, op, rhs = ineq
                        print(f"              {k}. {lhs} {op} {rhs}")
                print(f"            Total constraints in subcase: {len(filtered_constraints)}")
                print()
            else:
                print(f"            Case is impossible after filtering")
        else:
            # Complex case: multiple bounds require case expansion
            print(f"        Complex case: {len(lower_bounds)} lower, {len(upper_bounds)} upper bounds")
            print(f"        Expanding Max/Min expressions into individual cases")
            
            # Generate all combinations where each lower bound could be the maximum
            # and each upper bound could be the minimum
            case_count = 0
            
            if lower_bounds and upper_bounds:
                # Generate cases for each (lower_i, upper_j) combination
                for i, (lower_expr, lower_op) in enumerate(lower_bounds):
                    for j, (upper_expr, upper_op) in enumerate(upper_bounds):
                        case_count += 1
                        case_constraints = []
                        
                        # Add constraint that this lower bound is >= all other lower bounds
                        for k, (other_lower, other_op) in enumerate(lower_bounds):
                            if k != i:
                                case_constraints.append((lower_expr, '>=', other_lower))
                        
                        # Add constraint that this upper bound is <= all other upper bounds  
                        for k, (other_upper, other_op) in enumerate(upper_bounds):
                            if k != j:
                                case_constraints.append((upper_expr, '<=', other_upper))
                        
                        # Add the main elimination constraint: lower <= upper
                        case_constraints.append((lower_expr, '<=', upper_expr))
                        
                        # Add all remaining inequalities
                        case_constraints.extend(remaining_inequalities)
                        
                        # Filter for validity
                        filtered_constraints, is_impossible = self._filter_inequalities(case_constraints)
                        
                        if not is_impossible:
                            subcase_name, subcase_id = self.naming_system.get_case_name(
                                parent_case.name, parent_case.level + 1
                            )
                            
                            subcase = HierarchicalCase(
                                subcase_name, subcase_id, filtered_constraints, 
                                parent=parent_case, level=parent_case.level + 1
                            )
                            
                            parent_case.add_subcase(subcase)
                            subcases.append(subcase)
                            
                            print(f"            Generated {subcase_name}: {lower_expr} <= {upper_expr}")
                            print(f"              Total constraints: {len(filtered_constraints)}")
                        else:
                            print(f"            Case {case_count} is impossible")
            
            elif lower_bounds and not upper_bounds:
                # Only lower bounds - generate cases for which one is maximum
                for i, (lower_expr, lower_op) in enumerate(lower_bounds):
                    case_count += 1
                    case_constraints = []
                    
                    # Add constraints that this lower bound is >= all others
                    for k, (other_lower, other_op) in enumerate(lower_bounds):
                        if k != i:
                            case_constraints.append((lower_expr, '>=', other_lower))
                    
                    # Add all remaining inequalities
                    case_constraints.extend(remaining_inequalities)
                    
                    # Filter for validity
                    filtered_constraints, is_impossible = self._filter_inequalities(case_constraints)
                    
                    if not is_impossible:
                        subcase_name, subcase_id = self.naming_system.get_case_name(
                            parent_case.name, parent_case.level + 1
                        )
                        
                        subcase = HierarchicalCase(
                            subcase_name, subcase_id, filtered_constraints, 
                            parent=parent_case, level=parent_case.level + 1
                        )
                        
                        parent_case.add_subcase(subcase)
                        subcases.append(subcase)
                        
                        print(f"            Generated {subcase_name}: max = {lower_expr}")
                        print(f"              Total constraints: {len(filtered_constraints)}")
                    else:
                        print(f"            Case {case_count} is impossible")
            
            elif upper_bounds and not lower_bounds:
                # Only upper bounds - generate cases for which one is minimum
                for j, (upper_expr, upper_op) in enumerate(upper_bounds):
                    case_count += 1
                    case_constraints = []
                    
                    # Add constraints that this upper bound is <= all others
                    for k, (other_upper, other_op) in enumerate(upper_bounds):
                        if k != j:
                            case_constraints.append((upper_expr, '<=', other_upper))
                    
                    # Add all remaining inequalities
                    case_constraints.extend(remaining_inequalities)
                    
                    # Filter for validity
                    filtered_constraints, is_impossible = self._filter_inequalities(case_constraints)
                    
                    if not is_impossible:
                        subcase_name, subcase_id = self.naming_system.get_case_name(
                            parent_case.name, parent_case.level + 1
                        )
                        
                        subcase = HierarchicalCase(
                            subcase_name, subcase_id, filtered_constraints, 
                            parent=parent_case, level=parent_case.level + 1
                        )
                        
                        parent_case.add_subcase(subcase)
                        subcases.append(subcase)
                        
                        print(f"            Generated {subcase_name}: min = {upper_expr}")
                        print(f"              Total constraints: {len(filtered_constraints)}")
                    else:
                        print(f"            Case {case_count} is impossible")
            
            print(f"        STEP 4 SUMMARY:")
            print(f"          Generated {len(subcases)} subcase(s)")
            for i, subcase in enumerate(subcases, 1):
                print(f"            {i}. {subcase.name} - {len(subcase.inequalities)} constraints")
            print()
        
        # CRITICAL: Always generate at least one subcase to continue elimination
        if not subcases:
            print(f"        No valid subcases generated, creating fallback case")
            # Create a fallback case with the original constraints
            subcase_name, subcase_id = self.naming_system.get_case_name(
                parent_case.name, parent_case.level + 1, force_single_case=True
            )
            
            # Use the constraints that don't involve the variable
            fallback_constraints = remaining_inequalities
            
            subcase = HierarchicalCase(
                subcase_name, subcase_id, fallback_constraints, 
                parent=parent_case, level=parent_case.level + 1
            )
            
            parent_case.add_subcase(subcase)
            subcases.append(subcase)
            
            print(f"            Generated fallback {subcase_name}")
            print(f"            FALLBACK INEQUALITIES:")
            for k, ineq in enumerate(fallback_constraints, 1):
                if len(ineq) == 3:
                    lhs, op, rhs = ineq
                    print(f"              {k}. {lhs} {op} {rhs}")
            print(f"            Total constraints in fallback: {len(fallback_constraints)}")
            print()
        
        print(f"        STEP 4 SUMMARY:")
        print(f"          Generated {len(subcases)} subcase(s)")
        for i, subcase in enumerate(subcases, 1):
            print(f"            {i}. {subcase.name} - {len(subcase.inequalities)} constraints")
        print()
        
        return subcases
    
    def _solve_inequality_for_variable(self, expr, op, rhs, variable):
        """Solve inequality for variable using optimized approach for simple cases"""
        var_symbol = symbols(variable)
        
        try:
            # Convert strings to SymPy expressions if needed
            if isinstance(expr, str):
                expr_sym = sympify(expr)
            else:
                expr_sym = expr
                
            if isinstance(rhs, str):
                rhs_sym = sympify(rhs)
            else:
                rhs_sym = rhs
            
            print(f"          Solving: {expr} {op} {rhs}")
            
            # Check if this is a simple linear case: variable compared to expression not involving variable
            if expr_sym == var_symbol:
                # Case: x op rhs -> x op rhs (already in correct form)
                print(f"          Simple case: {variable} {op} {rhs}")
                if op in ['>=', '>']:
                    return [('lower', rhs_sym, op)]
                else:  # op in ['<=', '<']
                    return [('upper', rhs_sym, op)]
            
            # Ensure rhs_sym has free_symbols attribute for next check
            if not hasattr(rhs_sym, 'free_symbols'):
                rhs_sym = sympify(rhs_sym)
            
            # Check if rhs contains the variable and expr doesn't
            elif var_symbol not in expr_sym.free_symbols and var_symbol in rhs_sym.free_symbols:
                # Case: expr op f(x) -> need to solve f(x) op expr and flip
                print(f"          Flipped case: need to solve for {variable} in RHS")
                # This requires more complex analysis - fall back to full solver
                pass
            
            # Check for coefficient extraction: a*x + b op c -> x op (c-b)/a
            elif expr_sym.is_Add and len(expr_sym.args) <= 2:
                terms_with_var = [term for term in expr_sym.args if var_symbol in term.free_symbols]
                terms_without_var = [term for term in expr_sym.args if var_symbol not in term.free_symbols]
                
                if len(terms_with_var) == 1:
                    var_term = terms_with_var[0]
                    const_term = sum(terms_without_var) if terms_without_var else 0
                    
                    # Extract coefficient: var_term = coeff * variable + const_in_var_term
                    if var_term == var_symbol:
                        # Case: x + const op rhs -> x op rhs - const
                        new_rhs = rhs_sym - const_term
                        print(f"          Linear case: {variable} {op} {new_rhs}")
                        if op in ['>=', '>']:
                            return [('lower', new_rhs, op)]
                        else:
                            return [('upper', new_rhs, op)]
                    elif var_term.is_Mul and len(var_term.args) == 2:
                        # Case: coeff*x + const op rhs -> x op (rhs - const)/coeff
                        if var_symbol in var_term.args:
                            coeff = var_term.args[0] if var_term.args[1] == var_symbol else var_term.args[1]
                            new_rhs = (rhs_sym - const_term) / coeff
                            new_rhs = simplify(new_rhs)
                            
                            # Check coefficient sign to determine if we flip the inequality
                            if coeff > 0:
                                print(f"          Linear case (positive coeff): {variable} {op} {new_rhs}")
                                if op in ['>=', '>']:
                                    return [('lower', new_rhs, op)]
                                else:
                                    return [('upper', new_rhs, op)]
                            elif coeff < 0:
                                # Flip the inequality when dividing by negative coefficient
                                flipped_op = {'>=': '<=', '<=': '>=', '>': '<', '<': '>'}[op]
                                print(f"          Linear case (negative coeff): {variable} {flipped_op} {new_rhs}")
                                if flipped_op in ['>=', '>']:
                                    return [('lower', new_rhs, flipped_op)]
                                else:
                                    return [('upper', new_rhs, flipped_op)]
            
            # For complex cases, fall back to the full solver
            print(f"          Complex case: using full solver")
            ineq_expr = expr_sym - rhs_sym
            print(f"          Converted to: {ineq_expr} {op} 0")
            
            from solver import solve_rational_ineq_full
            case_outputs = solve_rational_ineq_full(ineq_expr, var_symbol, op, self.use_sign_analysis)
            
            print(f"          Solver returned {len(case_outputs)} case(s):")
            for i, case_output in enumerate(case_outputs, 1):
                print(f"            Case {i}: {case_output}")
            
            # Extract bounds from all solver cases
            all_bounds = []
            for i, case_output in enumerate(case_outputs):
                bounds = self._extract_bounds_from_single_case(case_output, variable, op, i+1)
                all_bounds.extend(bounds)
            
            if all_bounds:
                print(f"          Total extracted bounds: {len(all_bounds)}")
                for bound_type, bound_expr, bound_op in all_bounds:
                    print(f"            {bound_type}: {variable} {bound_op} {bound_expr}")
                return all_bounds
            else:
                print(f"          Warning: No bounds extracted, using fallback")
                # Intelligent fallback based on the original operation
                if op in ['>=', '>']:
                    return [('lower', 0, op)]
                else:
                    return [('upper', 0, op)]
                    
        except Exception as e:
            print(f"        Error solving inequality for {variable}: {e}")
            # Provide a reasonable fallback
            if op in ['>=', '>']:
                return [('lower', 0, op)]
            else:
                return [('upper', 0, op)]
    
    def _extract_bounds_from_single_case(self, case_output, variable, original_op, case_num):
        """Extract variable bounds from a single solver case output"""
        import re
        
        bounds = []
        
        print(f"          Parsing case {case_num}: {case_output[:100]}...")
        
        # Split the case output into lines
        lines = case_output.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Look for explicit "Linear condition" patterns first
            linear_condition_match = re.search(r'Linear condition:\s*x\s*(>=|<=|>|<)\s*(.+)', line)
            if linear_condition_match:
                op_symbol = linear_condition_match.group(1)
                expr_str = linear_condition_match.group(2)
                
                try:
                    bound_expr = sympify(expr_str.strip())
                    bound_expr = simplify(bound_expr)
                    
                    print(f"          Found linear condition: x {op_symbol} {bound_expr}")
                    
                    # Determine bound type
                    if op_symbol in ['>=', '≥']:
                        bounds.append(('lower', bound_expr, '>='))
                    elif op_symbol in ['<=', '≤']:
                        bounds.append(('upper', bound_expr, '<='))
                    elif op_symbol == '>':
                        bounds.append(('lower', bound_expr, '>'))
                    elif op_symbol == '<':
                        bounds.append(('upper', bound_expr, '<'))
                        
                except Exception as e:
                    print(f"          Error parsing linear condition: {e}")
                    continue
            
            # Look for patterns like "x >= expr", "x <= expr", "x > expr", "x < expr"
            # Handle both ASCII and Unicode inequality symbols
            direct_patterns = [
                rf'{variable}\s*(>=|≥)\s*(.+)',
                rf'{variable}\s*(<=|≤)\s*(.+)', 
                rf'{variable}\s*(>)\s*(.+)',
                rf'{variable}\s*(<)\s*(.+)',
            ]
            
            for pattern in direct_patterns:
                match = re.search(pattern, line)
                if match:
                    op_symbol = match.group(1)
                    expr_str = match.group(2)
                    
                    try:
                        bound_expr = sympify(expr_str.strip())
                        bound_expr = simplify(bound_expr)
                        
                        print(f"          Found direct pattern: {variable} {op_symbol} {bound_expr}")
                        
                        # Determine bound type
                        if op_symbol in ['>=', '≥']:
                            bounds.append(('lower', bound_expr, '>='))
                        elif op_symbol in ['<=', '≤']:
                            bounds.append(('upper', bound_expr, '<='))
                        elif op_symbol == '>':
                            bounds.append(('lower', bound_expr, '>'))
                        elif op_symbol == '<':
                            bounds.append(('upper', bound_expr, '<'))
                            
                    except Exception as e:
                        print(f"          Error parsing direct pattern: {e}")
                        continue
                    break  # Found a match, no need to check other patterns
            
            # Look for flipped patterns: "expression op variable" 
            flipped_patterns = [
                rf'(.+)\s*(<=|≤)\s*{variable}',  # expr <= x
                rf'(.+)\s*(>=|≥)\s*{variable}',  # expr >= x  
                rf'(.+)\s*(<)\s*{variable}',     # expr < x
                rf'(.+)\s*(>)\s*{variable}'      # expr > x
            ]
            
            for pattern in flipped_patterns:
                match = re.search(pattern, line)
                if match:
                    expr_str = match.group(1)
                    op_symbol = match.group(2)
                    
                    try:
                        bound_expr = sympify(expr_str.strip())
                        bound_expr = simplify(bound_expr)
                        
                        print(f"          Found flipped pattern: {bound_expr} {op_symbol} {variable}")
                        
                        # Flip the inequality direction since expr op variable => variable flip_op expr
                        if op_symbol in ['<=', '≤']:
                            bounds.append(('lower', bound_expr, '>='))
                            print(f"          Converted to: {variable} >= {bound_expr}")
                        elif op_symbol in ['>=', '≥']:
                            bounds.append(('upper', bound_expr, '<='))
                            print(f"          Converted to: {variable} <= {bound_expr}")
                        elif op_symbol == '<':
                            bounds.append(('lower', bound_expr, '>'))
                            print(f"          Converted to: {variable} > {bound_expr}")
                        elif op_symbol == '>':
                            bounds.append(('upper', bound_expr, '<'))
                            print(f"          Converted to: {variable} < {bound_expr}")
                            
                    except Exception as e:
                        print(f"          Error parsing flipped pattern: {e}")
                        continue
                    break  # Found a match, no need to check other patterns
            
            # Look for quadratic solution patterns
            quadratic_patterns = [
                rf'{variable}\s*(<|<=|≤)\s*(.+?)\s*or\s*{variable}\s*(>|>=|≥)\s*(.+)',  # x < a or x > b
                rf'(.+?)\s*(<|<=|≤)\s*{variable}\s*(<|<=|≤)\s*(.+)',  # a < x < b
            ]
            
            for pattern in quadratic_patterns:
                match = re.search(pattern, line)
                if match:
                    print(f"          Found quadratic pattern: {line}")
                    # This would need more complex parsing for quadratic cases
                    # For now, skip these as they require case analysis
                    continue
        
        print(f"          Case {case_num} bounds extracted: {len(bounds)}")
        for bound_type, expr, op in bounds:
            print(f"            {bound_type}: {variable} {op} {expr}")
        
        return bounds
    
    def _solve_linear_inequality_for_variable(self, expr, op, rhs, variable):
        """Legacy method for linear solving - delegates to simplified solver"""
        return self._solve_inequality_for_variable(expr, op, rhs, variable)
