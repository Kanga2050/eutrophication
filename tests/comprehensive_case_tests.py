#!/usr/bin/env python3

"""
Comprehensive test cases for variable elimination with complex case splitting scenarios.
Tests all edge cases that can confuse the solver or create multiple cases.
"""

from variable_eliminator import VariableEliminationSolver
import traceback

def test_division_by_indeterminate():
    """Test cases involving division by expressions that could be zero."""
    print("="*80)
    print("TEST 1: DIVISION BY INDETERMINATE EXPRESSIONS")
    print("="*80)
    
    test_cases = [
        {
            "name": "Simple division by variable",
            "inequalities": [
                "x/y >= 1",  # y could be positive or negative
                "y != 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should split into y > 0 and y < 0 cases"
        },
        {
            "name": "Division by expression with variable",
            "inequalities": [
                "x/(y + 1) <= 2",  # y + 1 could be positive or negative
                "x >= 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should split into y + 1 > 0 and y + 1 < 0 cases"
        },
        {
            "name": "Multiple divisions",
            "inequalities": [
                "x/y >= 1",
                "x/z <= 3",
                "y != 0",
                "z != 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should create 4 cases: (y>0,z>0), (y>0,z<0), (y<0,z>0), (y<0,z<0)"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest 1.{i}: {test_case['name']}")
        print("-" * 50)
        print("Inequalities:")
        for ineq in test_case['inequalities']:
            print(f"  {ineq}")
        print(f"Eliminate: {test_case['eliminate']}")
        print(f"Expected: {test_case['expected_cases']}")
        print()
        
        try:
            solver = VariableEliminationSolver(use_sign_analysis=True)
            result = solver.solve_with_variable_elimination(test_case['inequalities'], test_case['eliminate'])
            
            print("Results:")
            for step in result['steps']:
                if step['step_number'] == 0:
                    continue
                if 'case_based_constraints' in step:
                    case_result = step['case_based_constraints']
                    if 'case_based_constraints' in case_result:
                        cases = case_result['case_based_constraints']
                        print(f"  Found {len(cases)} individual cases")
                        for j, case in enumerate(cases, 1):
                            if 'conditions' in case and case['conditions']:
                                print(f"    Case {j} conditions: {case['conditions']}")
            
            print(f"  Final inequalities: {len(result['final_inequalities'])}")
            
        except Exception as e:
            print(f"ERROR: {e}")
            print(f"Traceback: {traceback.format_exc()}")


def test_quadratic_cases():
    """Test quadratic inequalities that can split into multiple cases."""
    print("\n" + "="*80)
    print("TEST 2: QUADRATIC INEQUALITIES")
    print("="*80)
    
    test_cases = [
        {
            "name": "Simple quadratic",
            "inequalities": [
                "x**2 - 4 >= 0",  # Should split into x >= 2 OR x <= -2
                "y >= 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should create cases for x >= 2 and x <= -2"
        },
        {
            "name": "Quadratic with linear term",
            "inequalities": [
                "x**2 + x - 2 <= 0",  # (x+2)(x-1) <= 0, so -2 <= x <= 1
                "y >= 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should create interval -2 <= x <= 1"
        },
        {
            "name": "Quadratic in two variables",
            "inequalities": [
                "x**2 + y**2 <= 4",  # Circle constraint
                "x + y >= 1"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should handle circular constraint properly"
        },
        {
            "name": "Quadratic with parameter",
            "inequalities": [
                "x**2 + a*x + b >= 0",  # Discriminant cases
                "a >= 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should depend on discriminant a^2 - 4b"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest 2.{i}: {test_case['name']}")
        print("-" * 50)
        print("Inequalities:")
        for ineq in test_case['inequalities']:
            print(f"  {ineq}")
        print(f"Eliminate: {test_case['eliminate']}")
        print(f"Expected: {test_case['expected_cases']}")
        print()
        
        try:
            solver = VariableEliminationSolver(use_sign_analysis=True)
            result = solver.solve_with_variable_elimination(test_case['inequalities'], test_case['eliminate'])
            
            print("Results:")
            for step in result['steps']:
                if step['step_number'] == 0:
                    continue
                if 'case_based_constraints' in step:
                    case_result = step['case_based_constraints']
                    if 'case_based_constraints' in case_result:
                        cases = case_result['case_based_constraints']
                        print(f"  Found {len(cases)} individual cases")
                        for j, case in enumerate(cases, 1):
                            if 'bounds' in case:
                                print(f"    Case {j} bounds: {case['bounds']}")
                            if 'conditions' in case and case['conditions']:
                                print(f"    Case {j} conditions: {case['conditions']}")
            
            print(f"  Final inequalities: {len(result['final_inequalities'])}")
            
        except Exception as e:
            print(f"ERROR: {e}")
            print(f"Traceback: {traceback.format_exc()}")


def test_absolute_value_cases():
    """Test absolute value inequalities that create case splits."""
    print("\n" + "="*80)
    print("TEST 3: ABSOLUTE VALUE INEQUALITIES")
    print("="*80)
    
    test_cases = [
        {
            "name": "Simple absolute value",
            "inequalities": [
                "abs(x) <= 3",  # Should split into -3 <= x <= 3
                "y >= 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should create -3 <= x <= 3"
        },
        {
            "name": "Absolute value with expression",
            "inequalities": [
                "abs(x + 1) >= 2",  # Should split into x + 1 >= 2 OR x + 1 <= -2
                "y >= 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should create x >= 1 OR x <= -3"
        },
        {
            "name": "Multiple absolute values",
            "inequalities": [
                "abs(x) + abs(y) <= 5",
                "x >= 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should handle multiple absolute value cases"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest 3.{i}: {test_case['name']}")
        print("-" * 50)
        print("Inequalities:")
        for ineq in test_case['inequalities']:
            print(f"  {ineq}")
        print(f"Eliminate: {test_case['eliminate']}")
        print(f"Expected: {test_case['expected_cases']}")
        print()
        
        try:
            solver = VariableEliminationSolver(use_sign_analysis=True)
            result = solver.solve_with_variable_elimination(test_case['inequalities'], test_case['eliminate'])
            
            print("Results:")
            for step in result['steps']:
                if step['step_number'] == 0:
                    continue
                if 'case_based_constraints' in step:
                    case_result = step['case_based_constraints']
                    if 'case_based_constraints' in case_result:
                        cases = case_result['case_based_constraints']
                        print(f"  Found {len(cases)} individual cases")
                        for j, case in enumerate(cases, 1):
                            if 'bounds' in case:
                                print(f"    Case {j} bounds: {case['bounds']}")
                            if 'conditions' in case and case['conditions']:
                                print(f"    Case {j} conditions: {case['conditions']}")
            
            print(f"  Final inequalities: {len(result['final_inequalities'])}")
            
        except Exception as e:
            print(f"ERROR: {e}")
            print(f"Traceback: {traceback.format_exc()}")


def test_square_root_cases():
    """Test square root expressions that impose domain constraints."""
    print("\n" + "="*80)
    print("TEST 4: SQUARE ROOT DOMAIN CONSTRAINTS")
    print("="*80)
    
    test_cases = [
        {
            "name": "Simple square root",
            "inequalities": [
                "sqrt(x) >= 2",  # Requires x >= 0 and sqrt(x) >= 2
                "y >= 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should require x >= 4 (since sqrt(x) >= 2)"
        },
        {
            "name": "Square root in denominator",
            "inequalities": [
                "1/sqrt(x + 1) <= 3",  # Requires x + 1 > 0
                "y >= 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should require x > -1 and additional constraints"
        },
        {
            "name": "Multiple square roots",
            "inequalities": [
                "sqrt(x) + sqrt(y) >= 5",
                "x >= 0",
                "y >= 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should handle domain constraints for both square roots"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest 4.{i}: {test_case['name']}")
        print("-" * 50)
        print("Inequalities:")
        for ineq in test_case['inequalities']:
            print(f"  {ineq}")
        print(f"Eliminate: {test_case['eliminate']}")
        print(f"Expected: {test_case['expected_cases']}")
        print()
        
        try:
            solver = VariableEliminationSolver(use_sign_analysis=True)
            result = solver.solve_with_variable_elimination(test_case['inequalities'], test_case['eliminate'])
            
            print("Results:")
            for step in result['steps']:
                if step['step_number'] == 0:
                    continue
                if 'case_based_constraints' in step:
                    case_result = step['case_based_constraints']
                    if 'case_based_constraints' in case_result:
                        cases = case_result['case_based_constraints']
                        print(f"  Found {len(cases)} individual cases")
                        for j, case in enumerate(cases, 1):
                            if 'bounds' in case:
                                print(f"    Case {j} bounds: {case['bounds']}")
                            if 'conditions' in case and case['conditions']:
                                print(f"    Case {j} conditions: {case['conditions']}")
            
            print(f"  Final inequalities: {len(result['final_inequalities'])}")
            
        except Exception as e:
            print(f"ERROR: {e}")
            print(f"Traceback: {traceback.format_exc()}")


def test_rational_function_cases():
    """Test rational functions with sign analysis requirements."""
    print("\n" + "="*80)
    print("TEST 5: RATIONAL FUNCTION SIGN ANALYSIS")
    print("="*80)
    
    test_cases = [
        {
            "name": "Rational inequality",
            "inequalities": [
                "(x - 1)/(x + 2) >= 0",  # Sign changes at x = 1 and x = -2
                "y >= 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should split into x <= -2 OR x >= 1"
        },
        {
            "name": "Complex rational",
            "inequalities": [
                "(x**2 - 4)/(x + 1) <= 3",  # Multiple critical points
                "y >= 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should analyze signs at x = -2, -1, 2"
        },
        {
            "name": "Rational with parameters",
            "inequalities": [
                "(x - a)/(x - b) >= 1",  # Depends on relationship between a and b
                "a < b"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should depend on whether a < b or a > b"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest 5.{i}: {test_case['name']}")
        print("-" * 50)
        print("Inequalities:")
        for ineq in test_case['inequalities']:
            print(f"  {ineq}")
        print(f"Eliminate: {test_case['eliminate']}")
        print(f"Expected: {test_case['expected_cases']}")
        print()
        
        try:
            solver = VariableEliminationSolver(use_sign_analysis=True)
            result = solver.solve_with_variable_elimination(test_case['inequalities'], test_case['eliminate'])
            
            print("Results:")
            for step in result['steps']:
                if step['step_number'] == 0:
                    continue
                if 'case_based_constraints' in step:
                    case_result = step['case_based_constraints']
                    if 'case_based_constraints' in case_result:
                        cases = case_result['case_based_constraints']
                        print(f"  Found {len(cases)} individual cases")
                        for j, case in enumerate(cases, 1):
                            if 'bounds' in case:
                                print(f"    Case {j} bounds: {case['bounds']}")
                            if 'conditions' in case and case['conditions']:
                                print(f"    Case {j} conditions: {case['conditions']}")
            
            print(f"  Final inequalities: {len(result['final_inequalities'])}")
            
        except Exception as e:
            print(f"ERROR: {e}")
            print(f"Traceback: {traceback.format_exc()}")


def test_mixed_complex_cases():
    """Test combinations of different case-splitting scenarios."""
    print("\n" + "="*80)
    print("TEST 6: MIXED COMPLEX SCENARIOS")
    print("="*80)
    
    test_cases = [
        {
            "name": "Quadratic + Division",
            "inequalities": [
                "x**2/y >= 4",  # Combines quadratic and division
                "y != 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should combine quadratic cases with y > 0, y < 0"
        },
        {
            "name": "Absolute value + Rational",
            "inequalities": [
                "abs(x)/(x + 1) <= 2",  # Combines absolute value with rational
                "x != -1"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should handle abs(x) cases and denominator sign"
        },
        {
            "name": "Everything combined",
            "inequalities": [
                "sqrt(x**2 + 1)/(abs(y) + 1) >= 2",  # Square root + quadratic + absolute value + division
                "x >= 0",
                "y != 0"
            ],
            "eliminate": ["x"],
            "expected_cases": "Should handle all types of case splitting"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest 6.{i}: {test_case['name']}")
        print("-" * 50)
        print("Inequalities:")
        for ineq in test_case['inequalities']:
            print(f"  {ineq}")
        print(f"Eliminate: {test_case['eliminate']}")
        print(f"Expected: {test_case['expected_cases']}")
        print()
        
        try:
            solver = VariableEliminationSolver(use_sign_analysis=True)
            result = solver.solve_with_variable_elimination(test_case['inequalities'], test_case['eliminate'])
            
            print("Results:")
            for step in result['steps']:
                if step['step_number'] == 0:
                    continue
                if 'case_based_constraints' in step:
                    case_result = step['case_based_constraints']
                    if 'case_based_constraints' in case_result:
                        cases = case_result['case_based_constraints']
                        print(f"  Found {len(cases)} individual cases")
                        for j, case in enumerate(cases, 1):
                            if 'bounds' in case:
                                print(f"    Case {j} bounds: {case['bounds']}")
                            if 'conditions' in case and case['conditions']:
                                print(f"    Case {j} conditions: {case['conditions']}")
            
            print(f"  Final inequalities: {len(result['final_inequalities'])}")
            
        except Exception as e:
            print(f"ERROR: {e}")
            print(f"Traceback: {traceback.format_exc()}")


def run_comprehensive_tests():
    """Run all comprehensive test cases."""
    print("COMPREHENSIVE CASE SPLITTING TESTS")
    print("Testing all scenarios that can cause case splits or confusion")
    print("="*80)
    
    # Run all test categories
    test_division_by_indeterminate()
    test_quadratic_cases()
    test_absolute_value_cases()
    test_square_root_cases()
    test_rational_function_cases()
    test_mixed_complex_cases()
    
    print("\n" + "="*80)
    print("COMPREHENSIVE TESTING COMPLETE")
    print("="*80)
    print()
    print("Summary of what should be tested:")
    print("1. Division by indeterminate expressions (sign analysis)")
    print("2. Quadratic inequalities (multiple roots)")
    print("3. Absolute value expressions (case splitting)")
    print("4. Square root domain constraints")
    print("5. Rational function sign analysis")
    print("6. Mixed complex scenarios")
    print()
    print("Each test should show:")
    print("- Individual cases found")
    print("- Conditions for each case")
    print("- Bounds extracted")
    print("- How cases are combined")
    print("- Final elimination results")


if __name__ == "__main__":
    run_comprehensive_tests()
