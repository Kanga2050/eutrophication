"""
Test manual verification with sign analysis disabled
"""

from variable_eliminator import solve_with_variable_elimination

def test_without_sign_analysis():
    """Test case with sign analysis disabled to get proper case splitting."""
    
    print("=" * 80)
    print("MANUAL VERIFICATION TEST (WITHOUT SIGN ANALYSIS)")
    print("=" * 80)
    
    # Define our test system
    inequalities = [
        'x1 + x2 <= 3',     # Upper bound: x1 <= 3 - x2
        'x1 - x2 >= 1',     # Lower bound: x1 >= x2 + 1  
        'x1/(x2 + 2) >= 0'  # Case splitting needed
    ]
    
    print("Test System:")
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    print()
    
    # Run our solver WITHOUT sign analysis to get proper case splitting
    result = solve_with_variable_elimination(
        inequalities, 
        ['x1'], 
        use_sign_analysis=False,  # This should give us proper case analysis
        save_latex=True,
        output_filename='manual_verification_no_sign_analysis'
    )
    
    print("\n" + "=" * 80)
    print("SOLVER OUTPUT WITHOUT SIGN ANALYSIS")
    print("=" * 80)
    
    # Show the step details
    step_1 = result['steps'][1]  # x1 elimination step
    case_result = step_1['case_based_constraints']
    
    print("Solver found case-based constraints:")
    for case in case_result['case_based_constraints']:
        print(f"  Case: {case['case_description']}")
        for bound_expr, direction in case['bounds']:
            print(f"    x1 {direction} {bound_expr}")
        for cond_lhs, cond_op, cond_rhs in case['conditions']:
            print(f"    Condition: {cond_lhs} {cond_op} {cond_rhs}")
        print()
    
    print("Final inequalities after elimination:")
    for lhs, op, rhs in result['final_inequalities']:
        print(f"  {lhs} {op} {rhs}")
    
    return result

if __name__ == "__main__":
    test_without_sign_analysis()
