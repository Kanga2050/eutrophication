#!/usr/bin/env python3

"""
Comprehensive test of the fixed case-based variable elimination.
"""

from variable_eliminator import VariableEliminationSolver

def test_comprehensive_cases():
    """Test various cases to confirm filtering and case handling work correctly."""
    
    test_cases = [
        {
            "name": "Simple Linear System",
            "inequalities": [
                "x1 + x2 <= 5",
                "x1 - x2 >= 1"
            ],
            "eliminate": ["x1"],
            "expected_vars": ["x2"]
        },
        {
            "name": "System with Bounds",
            "inequalities": [
                "x1 + 2*x2 <= 10",
                "x1 >= 3*x2",
                "x2 >= 1",
                "x2 <= 3"
            ],
            "eliminate": ["x1"],
            "expected_vars": ["x2"]
        },
        {
            "name": "Multiple Variables",
            "inequalities": [
                "x1 + x2 + x3 <= 10",
                "x1 - x2 >= 0",
                "x3 >= 2"
            ],
            "eliminate": ["x1"],
            "expected_vars": ["x2", "x3"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print("="*80)
        print(f"TEST {i}: {test_case['name']}")
        print("="*80)
        
        print("System:")
        for j, ineq in enumerate(test_case['inequalities'], 1):
            print(f"  {j}. {ineq}")
        
        print(f"\nEliminating: {test_case['eliminate']}")
        print(f"Expected remaining variables: {test_case['expected_vars']}")
        
        # Create eliminator and solve
        eliminator = VariableEliminationSolver(use_sign_analysis=False)
        result = eliminator.solve_with_variable_elimination(
            test_case['inequalities'], 
            test_case['eliminate']
        )
        
        print("\nFinal inequalities:")
        if isinstance(result, dict) and 'final_inequalities' in result:
            for j, ineq in enumerate(result['final_inequalities'], 1):
                print(f"  {j}. {ineq}")
        
        print(f"Number of final inequalities: {len(result.get('final_inequalities', []))}")
        print("")

if __name__ == "__main__":
    test_comprehensive_cases()
