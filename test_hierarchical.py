#!/usr/bin/env python3
"""
Test script for hierarchical variable elimination
"""

from main import demonstrate_enhanced_variable_elimination

def test_custom_system():
    """Test with a custom inequality system"""
    print("Testing with custom inequality system...")
    
    # Define a custom system
    custom_inequalities = [
        "x1 + x2 >= a",
        "x1 - x2 <= b", 
        "2*x1 + c >= d",
        "x2 + e <= f"
    ]
    
    custom_variables = ["x1", "x2"]
    
    print("Custom system:")
    for i, ineq in enumerate(custom_inequalities, 1):
        print(f"  {i}. {ineq}")
    
    print(f"Variables to eliminate: {custom_variables}")
    print()
    
    # Run elimination
    success = demonstrate_enhanced_variable_elimination(
        inequalities=custom_inequalities,
        variables_to_eliminate=custom_variables
    )
    
    return success

def test_three_variable_system():
    """Test with a more complex three-variable system"""
    print("\nTesting with three-variable system...")
    
    # Define a three-variable system
    three_var_inequalities = [
        "x1 + x2 + x3 >= a",
        "x1 - x2 + b >= 0",
        "x2 + c*x3 <= d",
        "x1 + e <= x3 + f"
    ]
    
    three_variables = ["x1", "x2", "x3"]
    
    print("Three-variable system:")
    for i, ineq in enumerate(three_var_inequalities, 1):
        print(f"  {i}. {ineq}")
    
    print(f"Variables to eliminate: {three_variables}")
    print()
    
    # Run elimination
    success = demonstrate_enhanced_variable_elimination(
        inequalities=three_var_inequalities,
        variables_to_eliminate=three_variables
    )
    
    return success

if __name__ == "__main__":
    print("HIERARCHICAL VARIABLE ELIMINATION TESTING")
    print("=" * 60)
    
    # Test 1: Custom two-variable system
    success1 = test_custom_system()
    
    # Test 2: Three-variable system
    success2 = test_three_variable_system()
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)
    
    if success1 and success2:
        print("✅ All tests passed successfully!")
        print("Check output_final/ directory for generated LaTeX files")
    else:
        print("❌ Some tests failed")
        print(f"Test 1 (custom system): {'✅' if success1 else '❌'}")
        print(f"Test 2 (three variables): {'✅' if success2 else '❌'}")
