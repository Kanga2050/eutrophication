#!/usr/bin/env python3

"""
Corrected unified main that properly handles individual cases for the scenarios 
that the current solver can actually process.
"""

from variable_eliminator import VariableEliminationSolver
from datetime import datetime

def demonstrate_corrected_simple_cases():
    """Demonstrate proper case handling for simple scenarios that work."""
    print("="*80)
    print("CORRECTED UNIFIED MAIN - SIMPLE CASES THAT WORK")
    print("="*80)
    
    # Test cases that the current solver can actually handle
    test_cases = [
        {
            "name": "Linear inequalities with elimination",
            "inequalities": [
                "x + y >= 0",
                "x - y <= 1",
                "z >= 2"
            ],
            "eliminate": ["x"],
            "expected": "Should combine x >= -y and x <= y + 1 to get constraint on y"
        },
        {
            "name": "Simple rational with known denominator sign",
            "inequalities": [
                "x/2 >= y",  # Denominator is positive
                "y <= 3"
            ],
            "eliminate": ["x"],
            "expected": "Should get x >= 2*y"
        },
        {
            "name": "Multi-variable linear system",
            "inequalities": [
                "x + 2*y + z >= 1",
                "x - z >= -1", 
                "y <= 5"
            ],
            "eliminate": ["x"],
            "expected": "Should eliminate x and relate y, z"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: {test_case['name']}")
        print('='*60)
        print("System:")
        for ineq in test_case['inequalities']:
            print(f"  {ineq}")
        print(f"Eliminate: {test_case['eliminate']}")
        print(f"Expected: {test_case['expected']}")
        print()
        
        try:
            # Create solver and get detailed results
            solver = VariableEliminationSolver(use_sign_analysis=True)
            result = solver.solve_with_variable_elimination(test_case['inequalities'], test_case['eliminate'])
            
            # Display detailed individual case analysis
            display_enhanced_case_analysis(result, solver, test_case['eliminate'][0])
            
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()


def display_enhanced_case_analysis(result, solver, eliminated_var):
    """Enhanced display of individual cases with mathematical reasoning."""
    
    for step in result['steps']:
        if step['step_number'] == 0:
            continue
            
        print(f"🔍 DETAILED ANALYSIS: Eliminating {step['variable_eliminated']}")
        print("-" * 50)
        
        if 'case_based_constraints' in step:
            case_result = step['case_based_constraints']
            
            # Show inequalities involving the variable
            print("📋 Original inequalities containing the variable:")
            if 'case_based_constraints' in case_result:
                cases = case_result['case_based_constraints']
                processed_inequalities = set()
                
                for i, case in enumerate(cases, 1):
                    if 'original_inequality' in case:
                        orig = case['original_inequality']
                        ineq_str = f"{orig[0]} {orig[1]} {orig[2]}"
                        if ineq_str not in processed_inequalities:
                            print(f"  {len(processed_inequalities) + 1}. {ineq_str}")
                            processed_inequalities.add(ineq_str)
                
                print(f"\n🔄 Individual Case Analysis:")
                print(f"Found {len(cases)} cases from isolation process:")
                
                for i, case in enumerate(cases, 1):
                    print(f"\n  📋 Case {i}:")
                    if 'original_inequality' in case:
                        orig = case['original_inequality']
                        print(f"    From: {orig[0]} {orig[1]} {orig[2]}")
                    
                    # Show mathematical transformation
                    if 'bounds' in case and case['bounds']:
                        bounds = case['bounds']
                        if isinstance(bounds, list) and len(bounds) > 0:
                            bound_expr, bound_op = bounds[0]
                            print(f"    Mathematical analysis:")
                            print(f"      Isolating {step['variable_eliminated']}: {step['variable_eliminated']} {bound_op}= {bound_expr}")
                    
                    # Show conditions
                    if 'conditions' in case and case['conditions']:
                        print(f"    Required conditions:")
                        for j, (cond_lhs, cond_op, cond_rhs) in enumerate(case['conditions'], 1):
                            print(f"      {j}. {cond_lhs} {cond_op} {cond_rhs}")
                    else:
                        print(f"    No additional conditions")
                
                # Show case combination analysis
                if 'eliminated_expressions' in step:
                    elim_result = step['eliminated_expressions']
                    show_case_combination_analysis(elim_result, solver, step['variable_eliminated'])
            
            # Show final result
            if 'output_inequalities' in step:
                output_ineqs = step['output_inequalities']
                print(f"\n📊 RESULT after eliminating {step['variable_eliminated']}:")
                print(f"  System reduced from input to {len(output_ineqs)} inequalities:")
                
                for i, ineq in enumerate(output_ineqs, 1):
                    if isinstance(ineq, tuple) and len(ineq) == 3:
                        print(f"    {i}. {ineq[0]} {ineq[1]} {ineq[2]}")
                    else:
                        print(f"    {i}. {ineq}")
        print()


def show_case_combination_analysis(elim_result, solver, var_name):
    """Show detailed case combination analysis."""
    print(f"\n  🔗 Case Combination Analysis:")
    
    if 'lower_bound_cases' in elim_result and 'upper_bound_cases' in elim_result:
        lower_cases = elim_result['lower_bound_cases']
        upper_cases = elim_result['upper_bound_cases']
        
        if lower_cases and upper_cases:
            print(f"    Combining {len(lower_cases)} lower bounds with {len(upper_cases)} upper bounds:")
            
            for li, lower in enumerate(lower_cases, 1):
                print(f"    📈 Lower Bound Case {li}: {var_name} >= {lower['expression']}")
                if lower['conditions']:
                    print(f"      Conditions: {[f'{lhs} {op} {rhs}' for lhs, op, rhs in lower['conditions']]}")
            
            for ui, upper in enumerate(upper_cases, 1):
                print(f"    📉 Upper Bound Case {ui}: {var_name} <= {upper['expression']}")
                if upper['conditions']:
                    print(f"      Conditions: {[f'{lhs} {op} {rhs}' for lhs, op, rhs in upper['conditions']]}")
            
            print(f"\n    🔄 Elimination Process:")
            print(f"    For each valid combination of lower and upper bounds:")
            print(f"    Create constraint: lower_bound <= upper_bound")
            
            valid_combinations = 0
            for li, lower in enumerate(lower_cases, 1):
                for ui, upper in enumerate(upper_cases, 1):
                    try:
                        lower_conditions = solver._filter_trivial_conditions(lower['conditions'])
                        upper_conditions = solver._filter_trivial_conditions(upper['conditions'])
                        
                        if (lower_conditions is not None and upper_conditions is not None and
                            solver._are_conditions_compatible(lower_conditions, upper_conditions)):
                            valid_combinations += 1
                            print(f"    ✅ Combination L{li}×U{ui}: {lower['expression']} <= {upper['expression']}")
                            all_conditions = lower_conditions + upper_conditions
                            if all_conditions:
                                print(f"       With conditions: {[f'{lhs} {op} {rhs}' for lhs, op, rhs in all_conditions]}")
                        else:
                            print(f"    ❌ Combination L{li}×U{ui}: Incompatible conditions")
                    except Exception as e:
                        print(f"    ⚠️ Error in combination L{li}×U{ui}: {e}")
            
            if valid_combinations == 0:
                print(f"    ⚠️ No valid combinations found!")
        
        elif lower_cases:
            print(f"    Only lower bounds found ({len(lower_cases)} cases):")
            for i, lower in enumerate(lower_cases, 1):
                print(f"    📈 Case {i}: {var_name} >= {lower['expression']}")
                if lower['conditions']:
                    filtered_conditions = solver._filter_trivial_conditions(lower['conditions'])
                    if filtered_conditions:
                        print(f"      Conditions: {[f'{lhs} {op} {rhs}' for lhs, op, rhs in filtered_conditions]}")
        
        elif upper_cases:
            print(f"    Only upper bounds found ({len(upper_cases)} cases):")
            for i, upper in enumerate(upper_cases, 1):
                print(f"    📉 Case {i}: {var_name} <= {upper['expression']}")
                if upper['conditions']:
                    filtered_conditions = solver._filter_trivial_conditions(upper['conditions'])
                    if filtered_conditions:
                        print(f"      Conditions: {[f'{lhs} {op} {rhs}' for lhs, op, rhs in filtered_conditions]}")
        else:
            print(f"    No bounds found for {var_name}")


def demonstrate_working_vs_broken():
    """Compare working simple cases vs broken complex cases."""
    print("\n" + "="*80)
    print("COMPARISON: WHAT WORKS vs WHAT'S BROKEN")
    print("="*80)
    
    print("✅ WORKING CASES:")
    print("- Linear inequalities: x + y >= 0")
    print("- Simple rationals with positive denominators: x/2 >= y")
    print("- Multi-variable linear systems")
    print("- Basic elimination with clear lower/upper bounds")
    
    print("\n❌ BROKEN CASES:")
    print("- Division by variables: x/y >= 1 (no sign analysis)")
    print("- Quadratic inequalities: x**2 - 4 >= 0 (not processed)")
    print("- Absolute values: abs(x) <= 3 (not recognized)")
    print("- Square roots: sqrt(x) >= 2 (not handled)")
    print("- Complex rational functions: (x-1)/(x+2) >= 0 (incomplete analysis)")
    
    print("\n🔧 WHAT NEEDS TO BE FIXED:")
    print("1. Enhance solve_rational_ineq_full() to handle complex expressions")
    print("2. Add proper sign analysis for all rational expressions")
    print("3. Implement case splitting for abs(), sqrt(), quadratics")
    print("4. Create complete case combination logic")
    print("5. Add domain constraint handling")


if __name__ == "__main__":
    demonstrate_corrected_simple_cases()
    demonstrate_working_vs_broken()
    
    print("\n" + "="*80)
    print("SUMMARY: CORRECTED UNIFIED MAIN STATUS")
    print("="*80)
    print("""
This corrected unified main demonstrates proper individual case analysis
for the scenarios that the current solver can handle. It shows:

✅ WHAT WORKS NOW:
- Enhanced display of individual cases with mathematical reasoning
- Detailed case combination analysis  
- Clear explanation of bounds and conditions
- Proper filtering of trivial conditions

❌ WHAT STILL NEEDS MAJOR FIXES:
- The underlying solver (solve_rational_ineq_full) needs enhancement
- Case splitting for complex expressions (quadratics, abs, sqrt)
- Complete sign analysis for rational expressions
- Domain constraint handling

The unified main interface is now much better, but the core solver
needs fundamental improvements to handle complex mathematical cases.
""")
