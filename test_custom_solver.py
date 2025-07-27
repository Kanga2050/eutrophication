#!/usr/bin/env python3
"""
Custom test to verify all solver.py functionality is working correctly
"""

from main import demonstrate_enhanced_variable_elimination
import traceback

def test_complex_solver_functionality():
    """Test various complex inequality types that use different parts of solver.py"""
    
    test_cases = [
        {
            'name': 'Pure Quadratic Test',
            'description': 'Test quadratic inequality handling',
            'inequalities': [
                "x1**2 - 4*x1 + 3 >= 0",  # (x-1)(x-3) >= 0
                "x1 + x2 <= a"
            ],
            'variables': ['x1', 'x2']
        },
        {
            'name': 'Mixed Rational and Quadratic',
            'description': 'Test both rational and quadratic in same system',
            'inequalities': [
                "x1**2 - 1 >= 0",  # x1 >= 1 or x1 <= -1
                "(x1 + 2)/(x1 - 3) <= 0",  # Rational inequality
                "x2 >= b"
            ],
            'variables': ['x1', 'x2']
        },
        {
            'name': 'Complex Rational System',
            'description': 'Complex rational inequality',
            'inequalities': [
                "(x1**2 - 1)/(x1 + 4) >= 0",  # Quadratic numerator, linear denominator
                "x1 - x2 <= c",
                "x2 + d >= e"
            ],
            'variables': ['x1', 'x2']
        },
        {
            'name': 'High Degree Test',
            'description': 'Test higher degree polynomial',
            'inequalities': [
                "x1**3 - x1 >= 0",  # x1(x1-1)(x1+1) >= 0
                "x1 + x2 <= f"
            ],
            'variables': ['x1', 'x2']
        }
    ]
    
    print("=" * 80)
    print("CUSTOM SOLVER FUNCTIONALITY TESTS")
    print("=" * 80)
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nCUSTOM TEST {i}: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print(f"Inequalities: {test_case['inequalities']}")
        print("-" * 60)
        
        try:
            success = demonstrate_enhanced_variable_elimination(
                inequalities=test_case['inequalities'],
                variables_to_eliminate=test_case['variables']
            )
            
            results.append({
                'test_case': test_case['name'],
                'success': success,
                'error': None
            })
            
            if success:
                print(f"✅ Custom test {i} completed successfully")
            else:
                print(f"❌ Custom test {i} failed")
                
        except Exception as e:
            print(f"❌ Custom test {i} failed with error: {e}")
            traceback.print_exc()
            results.append({
                'test_case': test_case['name'],
                'success': False,
                'error': str(e)
            })
        
        print("-" * 60)
    
    # Summary
    print("\n" + "=" * 80)
    print("CUSTOM TEST SUMMARY")
    print("=" * 80)
    
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"Total custom tests: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print()
    
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{status}: {result['test_case']}")
        if result['error']:
            print(f"    Error: {result['error']}")
    
    return results

if __name__ == "__main__":
    test_complex_solver_functionality()
