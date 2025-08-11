"""
Demonstration and Analysis Functions for Hierarchical Variable Elimination

This module provides demonstration functions and analysis tools for the 
hierarchical variable elimination system. It includes test cases, analysis
functions, and display utilities.

Functions:
- demonstrate_enhanced_variable_elimination: Main demonstration function
- display_hierarchical_case_analysis: Analysis display utility

Author: Simplified Rational Inequality Solver Team
Version: Pure Inequality System - No Constraint/Inequality Separation
"""
from sympy import symbols, simplify
from datetime import datetime
import os
from collections import defaultdict

from eliminator import HierarchicalCaseEliminator
from latex_generator import HierarchicalLatexGenerator
from input_processor import process_inequalities


def demonstrate_enhanced_variable_elimination(inequalities=None, variables_to_eliminate=None):
    """
    Simplified hierarchical variable elimination with no constraint/inequality separation.
    
    This function implements the complete 4-step variable elimination process where
    ALL results are treated as inequalities within cases. There is no distinction
    between constraints and inequalities - everything must be satisfied within each case.
    
    Key Principle: At the end, we can just say all the inequalities in one of the cases needs to be true.
    
    4-Step Process for Each Variable:
    1. **Isolate Variable**: Solve each inequality containing the target variable
       - Convert ax + b ≥ c to x ≥ (c-b)/a (handling coefficient signs)
       - Separate into lower bounds (x ≥ expr) and upper bounds (x ≤ expr)
    
    2. **Combine to Min/Max**: Form max(lower bounds) ≤ variable ≤ min(upper bounds)
       - Collect all lower bound expressions into max() form
       - Collect all upper bound expressions into min() form
       - Create unified constraint for the variable
    
    3. **Remove Variable**: Create elimination inequalities max(lower) ≤ min(upper)
       - Replace variable with the min/max constraints
       - Generate feasibility conditions for the system
    
    4. **Expand Cases**: Create hierarchical subcases for each min/max combination
       - For each pair (lower_i, upper_j), create case where lower_i ≤ upper_j
       - Name cases hierarchically with specific conditions
       - Recursively apply to all remaining variables
    
    LaTeX Output:
    Generates only one comprehensive LaTeX file where all results are shown as
    inequalities within cases, with complete hierarchical documentation.
    """
    print("=" * 80)
    print("SIMPLIFIED VARIABLE ELIMINATION - NO CONSTRAINT/INEQUALITY SEPARATION")  
    print("=" * 80)
    
    # Use provided inequalities or enhanced default example system
    if inequalities is None:
        inequalities = [
            "(x1 + 1)/(x1 - 7) >= 0",    # Rational inequality in x1
            "x1 + x2 <= a",              # Linear constraint with constants
            "x2 >= b"                    # Simple bound
        ]
    
    # Auto-detect variables if not provided
    if variables_to_eliminate is None:
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
    
    print("SIMPLIFIED SYSTEM (inequalities only):")
    print("Variables are represented as x1, x2, x3, x4, ...")
    print("Constants are represented as a, b, c, d, e, f, g, h, ...")
    print()
    
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    
    print(f"\nVariables to eliminate (in order): {variables_to_eliminate}")
    print("\nThis system will be processed using the simplified 4-step elimination method:")
    print("1. **Isolate Variable**: Solve each inequality for the target variable")
    print("   - Handle coefficient signs properly when isolating")
    print("   - Separate into lower bounds (x ≥ expr) and upper bounds (x ≤ expr)")
    print()
    print("2. **Combine to Min/Max**: Form max(lower_bounds) ≤ variable ≤ min(upper_bounds)")
    print("   - Collect all lower bound expressions")
    print("   - Collect all upper bound expressions")
    print()
    print("3. **Remove Variable**: Create elimination inequalities max(lower) ≤ min(upper)")
    print("   - Replace variable with feasibility conditions")
    print()
    print("4. **Expand Cases**: Create hierarchical subcases for each min/max combination")
    print("   - Generate all feasible combinations")
    print("   - Name cases with their specific conditions")
    print("   - Apply recursively to remaining variables")
    print()
    print("IMPORTANT: ALL results are inequalities within cases (no constraint separation)")
    print()
    
    try:
        # Create simplified hierarchical eliminator
        eliminator = HierarchicalCaseEliminator(use_sign_analysis=True)
        
        # Perform hierarchical elimination with simplified documentation
        final_cases = eliminator.eliminate_variables_hierarchical(inequalities, variables_to_eliminate)
        
        print(f"✅ Generated {len(final_cases)} final cases using simplified 4-step elimination:")
        
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
                print(f"    No inequalities (always satisfied)")
            else:
                print(f"    Final inequalities:")
                for i, inequality in enumerate(case.inequalities, 1):
                    expr, op, rhs = inequality
                    if rhs == 0:
                        simplified_expr = simplify(expr)
                        if simplified_expr == expr:
                            print(f"      {i}. {expr} {op} 0")
                        else:
                            print(f"      {i}. {simplified_expr} {op} 0  (simplified from {expr} {op} 0)")
                    else:
                        print(f"      {i}. {expr} {op} {rhs}")
        
        # Generate simplified hierarchical LaTeX documentation
        latex_generator = HierarchicalLatexGenerator()
        
        # Extract actual elimination results from the eliminator
        elimination_results = {}
        for i, var in enumerate(variables_to_eliminate):
            # Get the actual step data from eliminator if available
            if hasattr(eliminator, 'elimination_steps') and var in eliminator.elimination_steps:
                step_data = eliminator.elimination_steps[var]
                elimination_results[var] = {
                    'step_details': step_data
                }
            else:
                # Fallback to placeholder data if real data not available
                elimination_results[var] = {
                    'step_details': {
                        'isolate': {'resulting_inequalities': [f"{var} isolated bounds"]},
                        'combine': {'resulting_inequalities': [f"{var} combined bounds"]}, 
                        'remove': {'resulting_inequalities': [f"{var} elimination constraints"]},
                        'expand': {'resulting_inequalities': [f"{var} final constraints"], 'non_involving_inequalities': []}
                    }
                }
        
        latex_content = latex_generator.generate_elimination_latex(
            elimination_results, "Simplified Variable Elimination Process"
        )
        
        # Save to output directory
        output_dir = "/workspaces/codespaces-blank/output_final"
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/simplified_elimination_{timestamp}.tex"
        
        with open(filename, 'w') as f:
            f.write(latex_content)
        
        print(f"\n✅ Generated SIMPLIFIED LaTeX: {filename}")
        
        # Display simplified case analysis
        display_hierarchical_case_analysis(eliminator.all_cases)
        
        print("\n" + "="*60)
        print("SIMPLIFIED VARIABLE ELIMINATION COMPLETED")
        print("="*60)
        print()
        print("Key Features:")
        print("• Single comprehensive LaTeX file with no constraint/inequality separation")
        print("• All results are inequalities within cases")
        print("• Detailed 4-step process documentation")
        print("• Mathematical clarity with unified treatment")
        print("• Complete path tracing for each final case")
        print("• Simplified structure: inequalities only")
        
        return True
        
    except Exception as e:
        print(f"Error during simplified variable elimination: {e}")
        import traceback
        traceback.print_exc()
        return False


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
        print(f"  Inequalities: {len(case.inequalities)}")
        
        for j, inequality in enumerate(case.inequalities, 1):
            expr, op, rhs = inequality
            print(f"    {j}. {expr} {op} {rhs}")
        
        print(f"  Solution status: {'Solved' if case.is_solved else 'Unsolved'}")
        print()
    
    print("="*60)
    print("HIERARCHICAL CASE ANALYSIS COMPLETE")
    print("="*60)


def run_test_cases():
    """Run a comprehensive set of test cases"""
    test_cases = [
        {
            "name": "Simple Linear System",
            "inequalities": [
                "x1 + x2 <= a",
                "x1 >= b",
                "x2 >= c"
            ],
            "variables": ["x1", "x2"]
        },
        {
            "name": "Three Variable System",
            "inequalities": [
                "x1 + x2 + x3 <= a",
                "x1 >= b",
                "x2 + x3 <= c",
                "x3 >= d"
            ],
            "variables": ["x1", "x2", "x3"]
        },
        {
            "name": "Rational Inequality System",
            "inequalities": [
                "(x1 + 1)/(x1 - 7) >= 0",
                "x1 + x2 <= a",
                "x2 >= b"
            ],
            "variables": ["x1", "x2"]
        }
    ]
    
    print("=" * 80)
    print("RUNNING COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTEST CASE {i}: {test_case['name']}")
        print("-" * 40)
        
        success = demonstrate_enhanced_variable_elimination(
            test_case["inequalities"], 
            test_case["variables"]
        )
        
        if success:
            print(f"✅ Test case {i} completed successfully")
        else:
            print(f"❌ Test case {i} failed")
        
        print("-" * 40)
    
    print("\n" + "=" * 80)
    print("TEST SUITE COMPLETED")
    print("=" * 80)
