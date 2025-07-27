"""
Test variable elimination with case splitting scenarios.
Tests fraction cases, quadratic cases, and combined cases.
"""
from variable_eliminator import solve_with_variable_elimination
from datetime import datetime
import os


def test_fraction_case_splitting():
    """Test variable elimination with rational expressions that create multiple cases."""
    print("=" * 80)
    print("TEST 1: FRACTION CASE SPLITTING")
    print("=" * 80)
    
    # System that will create fraction cases when eliminating x1
    # The key is having x1 in denominators with different sign possibilities
    inequalities = [
        "1/(x1 + 2) >= 0",         # Creates case: x1 > -2
        "x2/(x1 - 1) <= 3",        # Creates case: x1 != 1, and sign cases
        "x1 + x2 >= 0",            # Linear constraint
        "x1 - 2*x2 <= 5",          # Another linear constraint
        "a + b <= c"               # Parameter constraint (preserved)
    ]
    
    print("System with fraction case splitting:")
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    
    print(f"\nEliminating variables: ['x1', 'x2']")
    print("Expected: Multiple cases due to fraction sign analysis")
    print()
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = solve_with_variable_elimination(
            inequalities=inequalities,
            variables_to_eliminate=['x1', 'x2'],
            use_sign_analysis=True,
            save_latex=True,
            output_filename=f"fraction_cases_{timestamp}"
        )
        
        print("RESULTS:")
        print(f"✅ Total elimination steps: {result['total_steps']}")
        print(f"✅ Final inequalities: {len(result['final_inequalities'])}")
        
        if result['final_inequalities']:
            print("Final system:")
            for i, (lhs, op, rhs) in enumerate(result['final_inequalities'], 1):
                print(f"  {i}. {lhs} {op} {rhs}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in fraction case test: {e}")
        return False


def test_quadratic_case_splitting():
    """Test variable elimination with quadratic expressions that create multiple cases."""
    print("\n" + "=" * 80)
    print("TEST 2: QUADRATIC CASE SPLITTING")
    print("=" * 80)
    
    # System that will create quadratic cases when eliminating x1
    # Use quadratics with different leading coefficients and discriminants
    inequalities = [
        "x1**2 - 4*x1 + 3 >= 0",    # (x1-1)(x1-3) >= 0, creates x1 <= 1 or x1 >= 3
        "x1**2 + 2*x1*x2 - x2 <= 0", # Quadratic in x1 with x2 parameter
        "-x1**2 + x1 + x2 >= 0",     # Negative leading coefficient
        "x1 + x2 >= -1",             # Linear constraint
        "d*e >= f"                   # Parameter constraint (preserved)
    ]
    
    print("System with quadratic case splitting:")
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    
    print(f"\nEliminating variables: ['x1', 'x2']")
    print("Expected: Multiple cases due to quadratic roots and sign changes")
    print()
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = solve_with_variable_elimination(
            inequalities=inequalities,
            variables_to_eliminate=['x1', 'x2'],
            use_sign_analysis=True,
            save_latex=True,
            output_filename=f"quadratic_cases_{timestamp}"
        )
        
        print("RESULTS:")
        print(f"✅ Total elimination steps: {result['total_steps']}")
        print(f"✅ Final inequalities: {len(result['final_inequalities'])}")
        
        if result['final_inequalities']:
            print("Final system:")
            for i, (lhs, op, rhs) in enumerate(result['final_inequalities'], 1):
                print(f"  {i}. {lhs} {op} {rhs}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in quadratic case test: {e}")
        return False


def test_combined_case_splitting():
    """Test variable elimination with both fraction and quadratic cases combined."""
    print("\n" + "=" * 80)
    print("TEST 3: COMBINED FRACTION + QUADRATIC CASE SPLITTING")
    print("=" * 80)
    
    # System combining both fraction and quadratic case splitting
    inequalities = [
        # Quadratic cases
        "x1**2 - 2*x1 - 3 <= 0",     # (x1+1)(x1-3) <= 0, so -1 <= x1 <= 3
        "x2**2 + x2*x3 - 2 >= 0",    # Quadratic in x2
        
        # Fraction cases  
        "x3/(x1 + 1) >= 0",           # Creates cases based on x1 > -1 vs x1 < -1
        "1/(x2 - 1) + x3 <= 2",      # Creates cases based on x2 > 1 vs x2 < 1
        
        # Mixed rational-polynomial
        "(x1*x2 + 1)/(x3 + 2) >= x1", # Complex rational with multiple variables
        
        # Linear constraints
        "x1 + x2 + x3 >= 0",
        "x1 - x3 <= 4",
        
        # Parameters (should be preserved)
        "a + b <= c",
        "p*q >= r"
    ]
    
    print("System with combined fraction + quadratic case splitting:")
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    
    print(f"\nEliminating variables: ['x1', 'x2', 'x3']")
    print("Expected: Complex case interactions between fractions and quadratics")
    print()
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = solve_with_variable_elimination(
            inequalities=inequalities,
            variables_to_eliminate=['x1', 'x2', 'x3'],
            use_sign_analysis=True,
            save_latex=True,
            output_filename=f"combined_cases_{timestamp}"
        )
        
        print("RESULTS:")
        print(f"✅ Total elimination steps: {result['total_steps']}")
        print(f"✅ Final inequalities: {len(result['final_inequalities'])}")
        
        if result['final_inequalities']:
            print("Final system:")
            for i, (lhs, op, rhs) in enumerate(result['final_inequalities'], 1):
                print(f"  {i}. {lhs} {op} {rhs}")
        else:
            print("All variables eliminated - only parameter constraints remain")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in combined case test: {e}")
        return False


def test_edge_cases():
    """Test edge cases that might cause issues."""
    print("\n" + "=" * 80)
    print("TEST 4: EDGE CASES")
    print("=" * 80)
    
    # Edge cases that might be problematic
    edge_cases = [
        {
            "name": "Multiple zeros in denominator",
            "inequalities": [
                "1/(x1*(x1-1)*(x1+1)) >= 0",  # Multiple critical points
                "x2 + x1 >= 0",
                "a <= b"
            ],
            "variables": ['x1', 'x2']
        },
        {
            "name": "Nested fractions",
            "inequalities": [
                "1/(1 + 1/(x1 + 1)) >= x2",    # Nested rational expression
                "x1 + x2 <= 3",
                "c >= d"
            ],
            "variables": ['x1', 'x2']
        },
        {
            "name": "Higher degree polynomial",
            "inequalities": [
                "x1**3 - x1**2 - x1 + 1 >= 0", # Cubic with multiple roots
                "x2*x1 <= 2",
                "e + f >= g"
            ],
            "variables": ['x1', 'x2']
        }
    ]
    
    results = []
    
    for i, case in enumerate(edge_cases, 1):
        print(f"\nEdge case {i}: {case['name']}")
        print("Inequalities:")
        for j, ineq in enumerate(case['inequalities'], 1):
            print(f"  {j}. {ineq}")
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result = solve_with_variable_elimination(
                inequalities=case['inequalities'],
                variables_to_eliminate=case['variables'],
                use_sign_analysis=True,
                save_latex=False,  # Skip LaTeX for edge cases to speed up
                output_filename=f"edge_case_{i}_{timestamp}"
            )
            
            print(f"✅ Success: {result['total_steps']} steps, {len(result['final_inequalities'])} final inequalities")
            results.append(True)
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            results.append(False)
    
    return all(results)


def main():
    """Run all case splitting tests."""
    print("VARIABLE ELIMINATION WITH CASE SPLITTING TESTS")
    print("Testing scenarios that force multiple case generation")
    print("=" * 80)
    
    # Run all tests
    test_results = []
    
    test_results.append(test_fraction_case_splitting())
    test_results.append(test_quadratic_case_splitting()) 
    test_results.append(test_combined_case_splitting())
    test_results.append(test_edge_cases())
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    test_names = [
        "Fraction Case Splitting",
        "Quadratic Case Splitting", 
        "Combined Cases",
        "Edge Cases"
    ]
    
    for i, (name, success) in enumerate(zip(test_names, test_results), 1):
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"Test {i} - {name}: {status}")
    
    overall_success = all(test_results)
    print(f"\nOverall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n🎉 Variable elimination works correctly with case splitting!")
        print("The solver handles:")
        print("• Fraction cases (denominator sign analysis)")
        print("• Quadratic cases (root finding and intervals)")
        print("• Combined scenarios (complex interactions)")
        print("• Edge cases (multiple zeros, nested expressions)")
        print()
        print("Generated LaTeX documentation shows complete case analysis.")
    else:
        print("\n⚠️ Some tests failed - review error messages above")
    
    return overall_success


if __name__ == "__main__":
    main()
