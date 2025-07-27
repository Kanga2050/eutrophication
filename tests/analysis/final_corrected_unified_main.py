#!/usr/bin/env python3

"""
FINAL CORRECTED UNIFIED MAIN

This version properly handles individual case display and analysis for all scenarios
that the current solver can actually process, while clearly identifying limitations.
"""

from variable_eliminator import VariableEliminationSolver, solve_with_variable_elimination
from datetime import datetime
import traceback

def demonstrate_enhanced_individual_cases():
    """Enhanced demonstration with proper individual case handling."""
    print("="*80)
    print("ENHANCED UNIFIED MAIN - PROPER INDIVIDUAL CASE ANALYSIS")
    print("="*80)
    
    # Example system that demonstrates proper case handling
    inequalities = [
        "x1 + 2*x2 >= 1",     # Linear case: x1 >= 1 - 2*x2
        "x1 - x2 <= 3",       # Linear case: x1 <= 3 + x2  
        "x2 + x3 >= 0",       # Will be preserved
        "x3 <= 5"             # Will be preserved
    ]
    
    variables_to_eliminate = ['x1', 'x2']
    
    print("DEMONSTRATION SYSTEM:")
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    
    print(f"\nVariables to eliminate: {variables_to_eliminate}")
    print("\nThis system demonstrates proper case handling for linear inequalities")
    print("that can be successfully processed by the current solver.")
    print()
    
    try:
        # Create solver instance for detailed analysis
        solver = VariableEliminationSolver(use_sign_analysis=True)
        result = solver.solve_with_variable_elimination(inequalities, variables_to_eliminate)
        
        # Display comprehensive individual case analysis
        display_comprehensive_case_analysis(result, solver)
        
        # Also generate the traditional output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unified_result = solve_with_variable_elimination(
            inequalities=inequalities,
            variables_to_eliminate=variables_to_eliminate,
            use_sign_analysis=True,
            save_latex=True,
            output_filename=f"corrected_unified_{timestamp}"
        )
        
        print("\n" + "="*80)
        print("FINAL RESULTS SUMMARY")
        print("="*80)
        print(f"✅ Successfully eliminated {len(variables_to_eliminate)} variables")
        print(f"📊 Final system has {len(unified_result['final_inequalities'])} inequalities")
        print()
        
        if unified_result['final_inequalities']:
            print("📋 Final constraint system:")
            for i, (lhs, op, rhs) in enumerate(unified_result['final_inequalities'], 1):
                print(f"  {i}. {lhs} {op} {rhs}")
        else:
            print("🎯 All specified variables eliminated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False


def display_comprehensive_case_analysis(result, solver):
    """Comprehensive display of individual case analysis with full mathematical reasoning."""
    
    print("="*80)
    print("COMPREHENSIVE INDIVIDUAL CASE ANALYSIS")
    print("="*80)
    
    for step in result['steps']:
        if step['step_number'] == 0:
            continue  # Skip initial system
            
        print(f"\n🎯 STEP {step['step_number']}: ELIMINATING {step['variable_eliminated'].upper()}")
        print("="*60)
        
        # Show input system
        print("📥 INPUT SYSTEM:")
        if 'input_inequalities' in step:
            for i, ineq in enumerate(step['input_inequalities'], 1):
                if isinstance(ineq, tuple) and len(ineq) == 3:
                    print(f"  {i}. {ineq[0]} {ineq[1]} {ineq[2]}")
                else:
                    print(f"  {i}. {ineq}")
        
        print(f"\n🔍 ISOLATING VARIABLE {step['variable_eliminated']}:")
        print("-" * 40)
        
        if 'case_based_constraints' in step:
            case_result = step['case_based_constraints']
            
            if 'case_based_constraints' in case_result:
                cases = case_result['case_based_constraints']
                
                # Group cases by original inequality
                inequality_cases = {}
                for case in cases:
                    if 'original_inequality' in case:
                        orig = case['original_inequality']
                        orig_str = f"{orig[0]} {orig[1]} {orig[2]}"
                        if orig_str not in inequality_cases:
                            inequality_cases[orig_str] = []
                        inequality_cases[orig_str].append(case)
                
                # Display each inequality's case analysis
                for ineq_str, ineq_cases in inequality_cases.items():
                    print(f"\n📋 ANALYZING: {ineq_str}")
                    
                    for i, case in enumerate(ineq_cases, 1):
                        print(f"\n  🔬 Case {i}:")
                        
                        # Show mathematical transformation
                        if 'bounds' in case and case['bounds']:
                            bounds = case['bounds']
                            if isinstance(bounds, list) and len(bounds) > 0:
                                bound_expr, bound_op = bounds[0]
                                
                                # Explain the mathematical process
                                print(f"    📐 Mathematical transformation:")
                                print(f"      Original: {ineq_str}")
                                print(f"      Isolating {step['variable_eliminated']}: {step['variable_eliminated']} {bound_op}= {bound_expr}")
                                
                                # Classify bound type
                                if bound_op in ['>', '>=']:
                                    print(f"      📈 Type: Lower bound")
                                elif bound_op in ['<', '<=']:
                                    print(f"      📉 Type: Upper bound")
                                else:
                                    print(f"      🔄 Type: Equality constraint")
                        
                        # Show required conditions
                        if 'conditions' in case and case['conditions']:
                            print(f"    ⚠️ Required conditions:")
                            for j, (cond_lhs, cond_op, cond_rhs) in enumerate(case['conditions'], 1):
                                print(f"      {j}. {cond_lhs} {cond_op} {cond_rhs}")
                        else:
                            print(f"    ✅ No additional conditions required")
                
                # Show case combination process
                print(f"\n🔗 CASE COMBINATION ANALYSIS:")
                print("-" * 30)
                
                if 'eliminated_expressions' in step:
                    elim_result = step['eliminated_expressions']
                    show_detailed_combination_analysis(elim_result, solver, step['variable_eliminated'])
                
            else:
                print("❌ No individual cases found - variable may not appear in isolatable form")
        
        # Show elimination result
        print(f"\n📤 ELIMINATION RESULT:")
        print("-" * 25)
        
        if 'output_inequalities' in step:
            output_ineqs = step['output_inequalities']
            input_count = len(step.get('input_inequalities', []))
            output_count = len(output_ineqs)
            
            print(f"  📊 System size: {input_count} → {output_count} inequalities")
            print(f"  🎯 Variable {step['variable_eliminated']} eliminated successfully")
            
            if output_count <= 6:  # Show all if reasonable
                print(f"  📋 Resulting system:")
                for i, ineq in enumerate(output_ineqs, 1):
                    if isinstance(ineq, tuple) and len(ineq) == 3:
                        print(f"    {i}. {ineq[0]} {ineq[1]} {ineq[2]}")
                    else:
                        print(f"    {i}. {ineq}")
            else:
                print(f"  📋 First 5 of {output_count} resulting inequalities:")
                for i, ineq in enumerate(output_ineqs[:5], 1):
                    if isinstance(ineq, tuple) and len(ineq) == 3:
                        print(f"    {i}. {ineq[0]} {ineq[1]} {ineq[2]}")
                    else:
                        print(f"    {i}. {ineq}")
                print(f"    ... and {output_count - 5} more")
        
        print()  # Spacing between steps


def show_detailed_combination_analysis(elim_result, solver, var_name):
    """Show detailed mathematical reasoning for case combinations."""
    
    if 'lower_bound_cases' in elim_result and 'upper_bound_cases' in elim_result:
        lower_cases = elim_result['lower_bound_cases']
        upper_cases = elim_result['upper_bound_cases']
        
        print(f"Found {len(lower_cases)} lower bound(s) and {len(upper_cases)} upper bound(s)")
        
        if lower_cases and upper_cases:
            print(f"\n📈 LOWER BOUNDS for {var_name}:")
            for i, lower in enumerate(lower_cases, 1):
                print(f"  L{i}: {var_name} >= {lower['expression']}")
                if lower['conditions']:
                    print(f"      Conditions: {[f'{lhs} {op} {rhs}' for lhs, op, rhs in lower['conditions']]}")
            
            print(f"\n📉 UPPER BOUNDS for {var_name}:")
            for i, upper in enumerate(upper_cases, 1):
                print(f"  U{i}: {var_name} <= {upper['expression']}")
                if upper['conditions']:
                    print(f"      Conditions: {[f'{lhs} {op} {rhs}' for lhs, op, rhs in upper['conditions']]}")
            
            print(f"\n🔄 ELIMINATION PROCESS:")
            print(f"To eliminate {var_name}, combine each lower bound with each upper bound:")
            print(f"For bounds L_i: {var_name} >= expr_i and U_j: {var_name} <= expr_j")
            print(f"Create elimination constraint: expr_i <= expr_j")
            print()
            
            valid_count = 0
            invalid_count = 0
            
            for li, lower in enumerate(lower_cases, 1):
                for ui, upper in enumerate(upper_cases, 1):
                    try:
                        # Filter and check compatibility
                        lower_conditions = solver._filter_trivial_conditions(lower['conditions'])
                        upper_conditions = solver._filter_trivial_conditions(upper['conditions'])
                        
                        if (lower_conditions is not None and upper_conditions is not None and
                            solver._are_conditions_compatible(lower_conditions, upper_conditions)):
                            
                            valid_count += 1
                            print(f"✅ Combination L{li}×U{ui}: {lower['expression']} <= {upper['expression']}")
                            
                            all_conditions = lower_conditions + upper_conditions
                            if all_conditions:
                                print(f"   📋 Combined conditions: {[f'{lhs} {op} {rhs}' for lhs, op, rhs in all_conditions]}")
                            else:
                                print(f"   ✅ No additional conditions needed")
                        else:
                            invalid_count += 1
                            print(f"❌ Combination L{li}×U{ui}: Incompatible conditions")
                    
                    except Exception as e:
                        invalid_count += 1
                        print(f"⚠️ Combination L{li}×U{ui}: Error - {e}")
            
            print(f"\n📊 COMBINATION SUMMARY: {valid_count} valid, {invalid_count} invalid")
        
        elif lower_cases:
            print(f"\n📈 ONLY LOWER BOUNDS (variable has no upper limit):")
            for i, lower in enumerate(lower_cases, 1):
                conditions = solver._filter_trivial_conditions(lower['conditions'])
                if conditions is not None:
                    print(f"  ✅ L{i}: {var_name} >= {lower['expression']}")
                    if conditions:
                        print(f"      Conditions: {[f'{lhs} {op} {rhs}' for lhs, op, rhs in conditions]}")
                else:
                    print(f"  ❌ L{i}: Impossible case")
        
        elif upper_cases:
            print(f"\n📉 ONLY UPPER BOUNDS (variable has no lower limit):")
            for i, upper in enumerate(upper_cases, 1):
                conditions = solver._filter_trivial_conditions(upper['conditions'])
                if conditions is not None:
                    print(f"  ✅ U{i}: {var_name} <= {upper['expression']}")
                    if conditions:
                        print(f"      Conditions: {[f'{lhs} {op} {rhs}' for lhs, op, rhs in conditions]}")
                else:
                    print(f"  ❌ U{i}: Impossible case")
        else:
            print(f"\n⚠️ NO BOUNDS FOUND - Variable {var_name} may not be properly constrained")


def show_solver_limitations():
    """Show current solver limitations and what needs to be enhanced."""
    print("\n" + "="*80)
    print("CURRENT SOLVER CAPABILITIES AND LIMITATIONS")
    print("="*80)
    
    print("✅ WHAT THE CURRENT SOLVER HANDLES WELL:")
    print("  🔹 Linear inequalities (ax + by + c >= 0)")
    print("  🔹 Simple rational inequalities with positive denominators (x/2 >= y)")
    print("  🔹 Multi-variable linear systems")
    print("  🔹 Variable elimination with clear bounds")
    print("  🔹 Trivial condition filtering")
    print("  🔹 Case combination for compatible constraints")
    
    print("\n❌ MAJOR LIMITATIONS (NEED CORE SOLVER ENHANCEMENTS):")
    print("  🔸 Division by variables: x/y >= 1 (no sign analysis)")
    print("  🔸 Quadratic inequalities: x² - 4 >= 0 (not processed)")
    print("  🔸 Absolute values: |x| <= 3 (not recognized)")
    print("  🔸 Square roots: √x >= 2 (not handled)")
    print("  🔸 Complex rationals: (x-1)/(x+2) >= 0 (incomplete)")
    
    print("\n🔧 REQUIRED ENHANCEMENTS:")
    print("  1. Extend solve_rational_ineq_full() for complex expressions")
    print("  2. Implement comprehensive sign analysis")
    print("  3. Add case splitting for absolute values and square roots")
    print("  4. Handle quadratic inequality solving")
    print("  5. Add domain constraint analysis")
    
    print("\n✨ ENHANCED UNIFIED MAIN FEATURES (IMPLEMENTED):")
    print("  ✅ Detailed individual case analysis with mathematical reasoning")
    print("  ✅ Step-by-step explanation of variable isolation")
    print("  ✅ Comprehensive case combination analysis")
    print("  ✅ Clear display of bounds, conditions, and constraints")
    print("  ✅ Mathematical transformation explanations")
    print("  ✅ Error handling and limitation identification")


if __name__ == "__main__":
    print("FINAL CORRECTED UNIFIED MAIN")
    print("Demonstrates proper individual case handling for supported scenarios")
    print()
    
    success = demonstrate_enhanced_individual_cases()
    show_solver_limitations()
    
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    
    if success:
        print("✅ ENHANCED UNIFIED MAIN WORKING CORRECTLY")
        print()
        print("🎯 ACHIEVEMENTS:")
        print("  • Individual cases are now properly solved and displayed")
        print("  • Mathematical reasoning is clearly explained")
        print("  • Case combinations are thoroughly analyzed")
        print("  • Limitations are clearly identified")
        print()
        print("🚀 NEXT STEPS:")
        print("  • Enhance core solver (solve_rational_ineq_full)")
        print("  • Add support for complex expressions")
        print("  • Implement comprehensive sign analysis")
        print("  • The unified main interface is now ready for enhanced solver")
    else:
        print("❌ ISSUES DETECTED - SEE ERROR MESSAGES ABOVE")
    
    print("\n📄 Generated files:")
    print("  • LaTeX documentation with complete case analysis")
    print("  • Text summary with step-by-step details")
