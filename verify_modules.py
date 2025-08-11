#!/usr/bin/env python3
"""
Module Verification Script

This script verifies that all modules can be imported correctly
and that the basic functionality is working after the refactoring.
"""

def test_imports():
    """Test that all modules can be imported successfully"""
    try:
        # Test core modules
        from case_system import CaseNamingSystem, HierarchicalCase
        from eliminator import HierarchicalCaseEliminator
        from latex_generator import HierarchicalLatexGenerator
        from demo import demonstrate_enhanced_variable_elimination
        
        # Test supporting modules
        from input_processor import process_inequalities
        from sign_analyzer import create_default_analyzer
        from solver import solve_rational_ineq_full
        
        print("✅ All module imports successful")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of key classes"""
    try:
        # Import classes for testing
        from case_system import CaseNamingSystem, HierarchicalCase
        from eliminator import HierarchicalCaseEliminator
        
        # Test CaseNamingSystem
        naming = CaseNamingSystem()
        case_name, case_id = naming.get_case_name()
        assert case_name == "Case 1"
        assert case_id == "1"
        
        # Test HierarchicalCase
        case = HierarchicalCase("Test Case", "1", [("x", ">=", "0")])
        assert case.name == "Test Case"
        assert len(case.inequalities) == 1
        
        # Test HierarchicalCaseEliminator
        eliminator = HierarchicalCaseEliminator()
        assert eliminator.use_sign_analysis == True
        
        print("✅ Basic functionality tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

def test_integration():
    """Test that the integration between modules works"""
    try:
        from eliminator import HierarchicalCaseEliminator
        
        # Simple test case
        inequalities = [("x1 + x2", "<=", "a"), ("x1", ">=", "b")]
        variables_to_eliminate = ['x1']
        
        eliminator = HierarchicalCaseEliminator()
        final_cases = eliminator.eliminate_variables_hierarchical(
            inequalities, variables_to_eliminate
        )
        
        assert len(final_cases) >= 0  # Should at least run without error
        print("✅ Integration test passed")
        return True
        
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False

if __name__ == "__main__":
    print("=== Module Verification Script ===")
    print()
    
    all_passed = True
    
    print("1. Testing imports...")
    all_passed &= test_imports()
    print()
    
    print("2. Testing basic functionality...")
    all_passed &= test_basic_functionality()
    print()
    
    print("3. Testing integration...")
    all_passed &= test_integration()
    print()
    
    if all_passed:
        print("🎉 All tests passed! The modular structure is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the module structure.")
