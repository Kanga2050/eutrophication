#!/usr/bin/env python3
"""
Simple verification script to test the enhanced case numbering system.
This script tests a simple case to ensure single subcases don't create
unnecessary nesting levels.
"""

from main import demonstrate_enhanced_variable_elimination

def test_simple_case():
    """Test a simple case with predictable single subcases"""
    print("Testing simple case with single subcases...")
    
    # Simple system that should produce single subcases at each step
    inequalities = [
        "x1 >= a",  # Simple lower bound
        "x2 <= b"   # Simple upper bound  
    ]
    variables = ["x1", "x2"]
    
    print(f"System: {inequalities}")
    print(f"Variables to eliminate: {variables}")
    print()
    
    success = demonstrate_enhanced_variable_elimination(
        inequalities=inequalities,
        variables_to_eliminate=variables
    )
    
    if success:
        print("✅ Simple case test completed successfully")
        print("Expected behavior:")
        print("• Case structure should be flat (Case 1 → Case 1)")
        print("• No unnecessary subcases like Subcase 1.1 should be created")
        print("• LaTeX should show logical case progression")
    else:
        print("❌ Simple case test failed")
    
    return success

if __name__ == "__main__":
    test_simple_case()
