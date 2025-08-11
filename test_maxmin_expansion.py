#!/usr/bin/env python3
"""
Test script specifically for Max/Min case expansion in Step 4
"""

from eliminator import HierarchicalCaseEliminator

def test_maxmin_expansion():
    print("=" * 60)
    print("TESTING MAX/MIN CASE EXPANSION IN STEP 4")
    print("=" * 60)
    
    # Test case with multiple bounds that should require Max/Min expansion
    inequalities = [
        ('x', '>=', 'a'),      # Lower bound 1: x >= a
        ('x', '>=', 'b'),      # Lower bound 2: x >= b  
        ('x', '<=', 'c'),      # Upper bound 1: x <= c
        ('x', '<=', 'd'),      # Upper bound 2: x <= d
        ('y', '>=', '0')       # Non-involving inequality
    ]
    
    print("Input system (designed to test Max/Min expansion):")
    for i, (lhs, op, rhs) in enumerate(inequalities, 1):
        print(f"  {i}. {lhs} {op} {rhs}")
    print()
    
    print("Expected behavior:")
    print("  - Step 1: Isolate x in each inequality")
    print("  - Step 2: Combine to max(a, b) <= x <= min(c, d)")  
    print("  - Step 3: Remove x with max(a, b) <= min(c, d)")
    print("  - Step 4: Expand into multiple cases:")
    print("    * Case 1: a >= b and c <= d and a <= c")
    print("    * Case 2: a >= b and d <= c and a <= d") 
    print("    * Case 3: b >= a and c <= d and b <= c")
    print("    * Case 4: b >= a and d <= c and b <= d")
    print()
    
    # Enable sign analysis with positive assumptions
    print("Configuration: Using sign analysis with positive variable assumptions")
    eliminator = HierarchicalCaseEliminator(use_sign_analysis=True)
    
    # Add positive assumptions for all variables and constants
    for var_name in ['x', 'y', 'a', 'b', 'c', 'd']:
        eliminator.sign_analyzer.add_assumption(var_name, 'positive')
    
    print("Running elimination...")
    try:
        final_cases = eliminator.eliminate_variables_hierarchical(inequalities, ['x'])
        
        print(f"\nRESULTS:")
        print(f"Generated {len(final_cases)} final case(s)")
        print()
        
        for i, case in enumerate(final_cases, 1):
            print(f"Case {i} ({case.name}):")
            print(f"  Level: {case.level}")
            print(f"  Inequalities ({len(case.inequalities)}):")
            
            for j, ineq in enumerate(case.inequalities, 1):
                if isinstance(ineq, tuple) and len(ineq) == 3:
                    lhs, op, rhs = ineq
                    print(f"    {j}. {lhs} {op} {rhs}")
                else:
                    print(f"    {j}. {ineq}")
            print()
        
        # Check if Max/Min expressions were properly expanded
        print("VERIFICATION:")
        max_min_found = False
        for case in final_cases:
            for ineq in case.inequalities:
                if isinstance(ineq, tuple) and len(ineq) == 3:
                    lhs, op, rhs = ineq
                    if 'Max(' in str(lhs) or 'Min(' in str(lhs) or 'Max(' in str(rhs) or 'Min(' in str(rhs):
                        max_min_found = True
                        print(f"  ❌ Max/Min expression found in {case.name}: {lhs} {op} {rhs}")
        
        if not max_min_found:
            print("  ✅ No Max/Min expressions found - all cases properly expanded!")
        
        if len(final_cases) >= 4:
            print("  ✅ Expected number of cases generated (4 or more)")
        else:
            print(f"  ⚠️  Only {len(final_cases)} cases generated, expected 4")
            
    except Exception as e:
        print(f"ERROR during elimination: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_maxmin_expansion()
