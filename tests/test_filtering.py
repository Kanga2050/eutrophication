"""
Test the condition filtering function
"""

from variable_eliminator import VariableEliminationSolver

def test_filtering():
    """Test the condition filtering logic."""
    
    solver = VariableEliminationSolver()
    
    print("Testing condition filtering:")
    
    # Test cases
    test_conditions = [
        [(1, '<', 0)],  # Always false
        [(1, '>', 0)],  # Always true  
        [(1, '==', 1)], # Always true
        [(0, '>', 1)],  # Always false
        [('x2 + 2', '>', 0)],  # Keep this
        [(1, '<', 0), ('x2', '>', 0)],  # Mix: false + keep
        [(1, '>', 0), ('x2', '<', 5)],  # Mix: true + keep
    ]
    
    for i, conditions in enumerate(test_conditions):
        print(f"\nTest {i+1}: {conditions}")
        result = solver._filter_trivial_conditions(conditions)
        print(f"  Result: {result}")

if __name__ == "__main__":
    test_filtering()
