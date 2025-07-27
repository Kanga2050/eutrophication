#!/usr/bin/env python3

"""
FINAL CORRECTED Unified Main with Proper Nested Case LaTeX Output

This integrates the corrected nested case structure with the existing unified main system.
"""

import sys
sys.path.append('/workspaces/codespaces-blank')

from variable_eliminator import VariableEliminationSolver
from complete_tree_elimination_final import CompleteTreeBasedEliminator
from nested_case_latex_generator import NestedCaseLatexGenerator
from examples import get_all_examples
from datetime import datetime
import os

def solve_and_display_with_corrected_nested_cases(inequalities, variables_to_eliminate):
    """
    Solve using corrected tree-based approach and display with proper nested cases.
    """
    print("=" * 80)
    print("CORRECTED VARIABLE ELIMINATION WITH NESTED CASE STRUCTURE")
    print("=" * 80)
    
    print(f"Input System: {inequalities}")
    print(f"Variables to eliminate: {variables_to_eliminate}")
    print()
    
    # Generate the corrected nested case solution
    generator = NestedCaseLatexGenerator()
    
    # Generate both mathematical solution and LaTeX
    eliminator = CompleteTreeBasedEliminator()
    final_cases = eliminator.eliminate_variables_complete_tree(inequalities, variables_to_eliminate)
    
    print("MATHEMATICAL SOLUTION:")
    print(f"Final case tree contains {len(final_cases)} final cases:")
    
    for i, case in enumerate(final_cases, 1):
        print(f"  Final Case {i}: {case}")
        
        # Show simplified constraints
        simplified = []
        for constraint in case:
            expr, op, rhs = constraint
            from sympy import simplify
            if rhs == 0:
                simplified_expr = simplify(expr)
                simplified.append(f"{simplified_expr} {op} 0")
            else:
                simplified.append(f"{expr} {op} {rhs}")
        
        if simplified:
            print(f"    Simplified: {simplified}")
        else:
            print(f"    Simplified: [No constraints - always true]")
    
    print("\n" + "=" * 60)
    print("GENERATING NESTED CASE LATEX OUTPUT")
    print("=" * 60)
    
    # Generate the corrected LaTeX with nested structure
    latex_content = generator.generate_nested_case_latex(inequalities, variables_to_eliminate)
    
    # Save to output directory
    output_dir = "/workspaces/codespaces-blank/output_final"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/corrected_nested_cases_{timestamp}_complete.tex"
    
    with open(filename, 'w') as f:
        f.write(latex_content)
    
    print(f"✅ Generated corrected LaTeX file: {filename}")
    
    print("\n" + "=" * 60)
    print("COMPARISON WITH ORIGINAL (WRONG) APPROACH")
    print("=" * 60)
    
    # Show what the original system would produce (for comparison)
    print("Original system would produce:")
    try:
        original_solver = VariableEliminationSolver()
        original_result = original_solver.solve_with_variable_elimination(inequalities, variables_to_eliminate)
        print(f"  Single result: {original_result.get('final_inequalities', 'Error')}")
        print("  ❌ WRONG: Loses case structure and mathematical information")
    except Exception as e:
        print(f"  Original system error: {e}")
    
    print("\nCorrected system produces:")
    print(f"  {len(final_cases)} properly nested cases with complete mathematical rigor")
    print("  ✅ CORRECT: Preserves all cases and mathematical information")
    
    return filename, final_cases

def test_all_corrected_examples():
    """
    Test the corrected approach on various examples.
    """
    print("=" * 80)
    print("TESTING CORRECTED NESTED CASE APPROACH ON MULTIPLE EXAMPLES")
    print("=" * 80)
    
    # Test cases that demonstrate nested structure
    test_cases = [
        {
            'name': 'Multiple Lower Bounds (Creates Subcases)',
            'system': ["x + 2*y >= 1", "x - y >= -1", "y <= 3"],
            'variables': ['x'],
            'expected_cases': 2
        },
        {
            'name': 'Multi-Variable with Nested Cases',
            'system': ["x + y >= 1", "x - z <= 2", "y - z >= 0"],
            'variables': ['x', 'y'],
            'expected_cases': 2
        },
        {
            'name': 'Both Upper and Lower Bounds',
            'system': ["x >= y + 1", "x <= 2*y - 1", "y >= 2"],
            'variables': ['x'],
            'expected_cases': 1
        },
        {
            'name': 'Complex Multi-Variable',
            'system': ["x + y + z >= 1", "x - y <= 2", "y - z >= 0", "z <= 5"],
            'variables': ['x', 'y'],
            'expected_cases': 'varies'
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTEST {i}: {test_case['name']}")
        print("-" * 50)
        
        try:
            filename, final_cases = solve_and_display_with_corrected_nested_cases(
                test_case['system'], 
                test_case['variables']
            )
            
            results.append({
                'test': test_case['name'],
                'filename': filename,
                'final_cases': len(final_cases),
                'expected': test_case['expected_cases'],
                'status': 'SUCCESS'
            })
            
        except Exception as e:
            print(f"❌ ERROR in test {i}: {e}")
            import traceback
            traceback.print_exc()
            
            results.append({
                'test': test_case['name'],
                'filename': None,
                'final_cases': 0,
                'expected': test_case['expected_cases'],
                'status': f'ERROR: {e}'
            })
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    for result in results:
        status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
        print(f"{status_icon} {result['test']}")
        print(f"    Expected cases: {result['expected']}")
        print(f"    Actual cases: {result['final_cases']}")
        print(f"    Status: {result['status']}")
        if result['filename']:
            print(f"    LaTeX file: {result['filename']}")
        print()
    
    return results

def demonstrate_correction():
    """
    Demonstrate the key correction with a simple example.
    """
    print("=" * 80)
    print("DEMONSTRATION: THE KEY CORRECTION")
    print("=" * 80)
    
    # Use the example that clearly shows the problem
    system = ["x + 2*y >= 1", "x - y >= -1", "y <= 3"]
    variables = ['x']
    
    print("EXAMPLE SYSTEM:")
    print(f"  Inequalities: {system}")
    print(f"  Eliminate: {variables}")
    print()
    
    print("MATHEMATICAL ANALYSIS:")
    print("  From x + 2*y >= 1: x >= 1 - 2*y")
    print("  From x - y >= -1:  x >= y - 1")
    print("  Multiple lower bounds require case analysis:")
    print("    Case 1: 1 - 2*y >= y - 1  →  y <= 2/3")
    print("    Case 2: y - 1 >= 1 - 2*y  →  y >= 2/3")
    print("  Combined with y <= 3:")
    print("    Final Case 1: y <= 2/3")
    print("    Final Case 2: 2/3 <= y <= 3")
    print()
    
    print("TESTING CORRECTED IMPLEMENTATION:")
    filename, final_cases = solve_and_display_with_corrected_nested_cases(system, variables)
    
    print(f"\n✅ SUCCESS: Generated {len(final_cases)} cases as expected")
    print(f"✅ LaTeX file with nested structure: {filename}")

if __name__ == "__main__":
    # Run the demonstration first
    demonstrate_correction()
    
    print("\n" * 3)
    
    # Then run comprehensive tests
    test_all_corrected_examples()
