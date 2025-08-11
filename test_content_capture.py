#!/usr/bin/env python3

"""
Test script to verify that actual mathematical expressions are captured
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, '/workspaces/codespaces-blank')

def test_basic_elimination():
    """Test with simple inequalities to capture actual mathematical expressions"""
    
    try:
        print("="*60)
        print("TESTING MATHEMATICAL CONTENT CAPTURE")
        print("="*60)
        
        # Import required modules
        from eliminator import HierarchicalCaseEliminator
        from demo import demonstrate_enhanced_variable_elimination
        
        # Simple test case with real mathematical expressions
        inequalities = [
            ('n_l', '<=', 'n_u'),
            ('1 + A_1*S_l - n_l - A_2*n_l*a_u', '>=', '0'),
            ('B_1*n_l - 1 - a_l - B_2*Z_u', '>=', '0')
        ]
        
        variables_to_eliminate = ['n_l']
        
        print("Input inequalities:")
        for i, (lhs, op, rhs) in enumerate(inequalities):
            print(f"  {i+1}. {lhs} {op} {rhs}")
        
        print()
        print("Variables to eliminate:", variables_to_eliminate)
        print()
        
        # Test direct eliminator first
        print("Testing HierarchicalCaseEliminator directly...")
        eliminator = HierarchicalCaseEliminator()
        
        # Run elimination
        final_cases = eliminator.eliminate_variables_hierarchical(inequalities, variables_to_eliminate)
        
        print()
        print("Checking if elimination_steps were captured...")
        if hasattr(eliminator, 'elimination_steps'):
            print(f"elimination_steps attribute exists: {list(eliminator.elimination_steps.keys())}")
            if 'n_l' in eliminator.elimination_steps:
                print("Found stored data for n_l:")
                steps = eliminator.elimination_steps['n_l']
                for step_name, step_data in steps.items():
                    print(f"  {step_name}: {step_data}")
                    if 'resulting_inequalities' in step_data:
                        print(f"    -> Inequalities: {step_data['resulting_inequalities']}")
            else:
                print("No data stored for n_l")
        else:
            print("elimination_steps attribute not found")
            
        return True
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_elimination()
    print()
    if success:
        print("✅ Test completed")
    else:
        print("❌ Test failed")
