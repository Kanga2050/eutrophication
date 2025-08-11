"""
Progressive Complexity Test Suite for Rational Inequality Solver

This module creates increasingly complex test cases to stress-test the system
and measure performance scaling. We progressively increase:
- Number of constants (a, b, c, ...)
- Number of variables (x1, x2, x3, ...)  
- Number of inequalities/equations
- Complexity of expressions (linear -> polynomial -> rational)

Target: Work up to 8 constants, 10 variables, 7 equations

Author: Test Suite Team
Version: 1.0.0 - Progressive Complexity Testing
"""

import time
import traceback
from datetime import datetime
import os
from collections import defaultdict

from eliminator import HierarchicalCaseEliminator
from latex_generator import HierarchicalLatexGenerator
from demo import demonstrate_enhanced_variable_elimination


class ComplexityTester:
    """Manages progressive complexity testing with timing and verification"""
    
    def __init__(self):
        self.results = []
        self.output_dir = "/workspaces/codespaces-blank/output_final"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def run_timed_test(self, test_case):
        """Run a single test case with timing and result capture"""
        print(f"\n{'='*80}")
        print(f"TEST: {test_case['name']}")
        print(f"{'='*80}")
        print(f"Constants: {test_case['constants']}")
        print(f"Variables: {test_case['variables']} (to eliminate: {test_case['variables_to_eliminate']})")
        print(f"Equations: {len(test_case['inequalities'])}")
        print(f"Complexity: {test_case['complexity']}")
        print()
        
        for i, ineq in enumerate(test_case['inequalities'], 1):
            print(f"  {i}. {ineq}")
        
        print(f"\nStarting elimination of variables: {test_case['variables_to_eliminate']}")
        print("-" * 80)
        
        start_time = time.time()
        
        try:
            # Run the test
            success = demonstrate_enhanced_variable_elimination(
                inequalities=test_case['inequalities'],
                variables_to_eliminate=test_case['variables_to_eliminate']
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Record results
            result = {
                'name': test_case['name'],
                'constants': test_case['constants'],
                'variables': len(test_case['variables']),
                'variables_to_eliminate': len(test_case['variables_to_eliminate']),
                'equations': len(test_case['inequalities']),
                'complexity': test_case['complexity'],
                'duration': duration,
                'success': success,
                'timestamp': datetime.now()
            }
            
            self.results.append(result)
            
            print(f"\n{'='*80}")
            print(f"TEST COMPLETED: {test_case['name']}")
            print(f"{'='*80}")
            print(f"✅ Success: {'Yes' if success else 'No'}")
            print(f"⏱️  Duration: {duration:.3f} seconds")
            print(f"📊 Performance: {test_case['complexity']} complexity")
            
            if duration > 60:
                print(f"⚠️  WARNING: Test took over 1 minute ({duration/60:.1f} minutes)")
            elif duration > 10:
                print(f"⚠️  NOTICE: Test took over 10 seconds")
            
            return success, duration
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"\n{'='*80}")
            print(f"TEST FAILED: {test_case['name']}")
            print(f"{'='*80}")
            print(f"❌ Error: {e}")
            print(f"⏱️  Duration before failure: {duration:.3f} seconds")
            print(f"📊 Details:")
            traceback.print_exc()
            
            # Record failure
            result = {
                'name': test_case['name'],
                'constants': test_case['constants'],
                'variables': len(test_case['variables']),
                'variables_to_eliminate': len(test_case['variables_to_eliminate']),
                'equations': len(test_case['inequalities']),
                'complexity': test_case['complexity'],
                'duration': duration,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now()
            }
            
            self.results.append(result)
            
            return False, duration
    
    def print_summary(self):
        """Print comprehensive test summary"""
        print(f"\n{'='*100}")
        print(f"PROGRESSIVE COMPLEXITY TEST SUITE SUMMARY")
        print(f"{'='*100}")
        
        if not self.results:
            print("No test results to display.")
            return
        
        print(f"{'Test Name':<25} {'Vars':<4} {'Eqs':<4} {'Complexity':<12} {'Time':<8} {'Status':<8}")
        print("-" * 100)
        
        total_time = 0
        successful = 0
        
        for result in self.results:
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            time_str = f"{result['duration']:.3f}s"
            
            print(f"{result['name']:<25} {result['variables_to_eliminate']:<4} {result['equations']:<4} "
                  f"{result['complexity']:<12} {time_str:<8} {status}")
            
            total_time += result['duration']
            if result['success']:
                successful += 1
        
        print("-" * 100)
        print(f"Total tests: {len(self.results)}")
        print(f"Successful: {successful}/{len(self.results)} ({100*successful/len(self.results):.1f}%)")
        print(f"Total time: {total_time:.3f} seconds ({total_time/60:.1f} minutes)")
        print(f"Average time per test: {total_time/len(self.results):.3f} seconds")
        
        # Performance analysis
        if successful > 0:
            successful_results = [r for r in self.results if r['success']]
            fastest = min(successful_results, key=lambda x: x['duration'])
            slowest = max(successful_results, key=lambda x: x['duration'])
            
            print(f"\nPerformance Analysis:")
            print(f"Fastest test: {fastest['name']} ({fastest['duration']:.3f}s)")
            print(f"Slowest test: {slowest['name']} ({slowest['duration']:.3f}s)")
            print(f"Speed ratio: {slowest['duration']/fastest['duration']:.1f}x")
        
        print(f"\n{'='*100}")


def create_progressive_test_cases():
    """Create test cases with progressively increasing complexity"""
    
    test_cases = []
    
    # Level 1: Simple 2-variable, 2-constant system (Baseline)
    test_cases.append({
        'name': 'Level_1_Basic',
        'constants': 2,
        'variables': ['x1', 'x2'],
        'variables_to_eliminate': ['x1', 'x2'],
        'complexity': 'Linear-Basic',
        'inequalities': [
            'x1 + x2 <= a',
            'x1 >= b'
        ]
    })
    
    # Level 2: Add one more variable and constant
    test_cases.append({
        'name': 'Level_2_Extended',
        'constants': 3,
        'variables': ['x1', 'x2', 'x3'],
        'variables_to_eliminate': ['x1', 'x2', 'x3'],
        'complexity': 'Linear-Extended',
        'inequalities': [
            'x1 + x2 <= a',
            'x2 + x3 <= b',
            'x1 >= c'
        ]
    })
    
    # Level 3: More complex expressions
    test_cases.append({
        'name': 'Level_3_Polynomial',
        'constants': 4,
        'variables': ['x1', 'x2', 'x3', 'x4'],
        'variables_to_eliminate': ['x1', 'x2', 'x3', 'x4'],
        'complexity': 'Polynomial',
        'inequalities': [
            'x1 + 2*x2 + x3 <= a',
            'x1**2 + x2 >= b',
            'x3 + x4 <= c',
            'x4 >= d'
        ]
    })
    
    # Level 4: Rational expressions (moderate complexity)
    test_cases.append({
        'name': 'Level_4_Rational',
        'constants': 4,
        'variables': ['x1', 'x2', 'x3', 'x4'],
        'variables_to_eliminate': ['x1', 'x2', 'x3', 'x4'],
        'complexity': 'Rational-Moderate',
        'inequalities': [
            'x1/(x2 + 1) <= a',
            'x1 + x2 + x3 >= b', 
            'x3**2 + x4 <= c',
            'x4 >= d'
        ]
    })
    
    # Level 5: Five variables, five constants
    test_cases.append({
        'name': 'Level_5_Five_Vars',
        'constants': 5,
        'variables': ['x1', 'x2', 'x3', 'x4', 'x5'],
        'variables_to_eliminate': ['x1', 'x2', 'x3', 'x4', 'x5'],
        'complexity': 'Multi-Variable',
        'inequalities': [
            'x1 + x2 + x3 <= a',
            'x2 + x4 + x5 <= b',
            'x1 + x5 >= c',
            'x3 + x4 >= d',
            'x5 <= e'
        ]
    })
    
    # Level 6: Six variables, mixed complexity
    test_cases.append({
        'name': 'Level_6_Mixed_Complex',
        'constants': 6,
        'variables': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6'],
        'variables_to_eliminate': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6'],
        'complexity': 'Mixed-Complex',
        'inequalities': [
            '2*x1 + x2/(x3 + 1) <= a',
            'x1**2 + x4 + x5 >= b',
            'x2 + x3 + x6 <= c',
            'x4 + x5**2 >= d',
            'x5 + x6 <= e',
            'x6 >= f'
        ]
    })
    
    # Level 7: Seven variables, six equations, more constants
    test_cases.append({
        'name': 'Level_7_Seven_Vars',
        'constants': 7,
        'variables': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7'],
        'variables_to_eliminate': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7'],
        'complexity': 'High-Complexity',
        'inequalities': [
            'x1 + x2 + x3 + x4 <= a',
            'x2**2 + x5 + x6 <= b',
            'x1 + x7/(x3 + 2) >= c',
            'x4 + x5 + x6 + x7 <= d',
            'x3 + x5 >= e',
            'x6 + x7 <= f',
            'x7 >= g'
        ]
    })
    
    # Level 8: Eight variables, advanced expressions
    test_cases.append({
        'name': 'Level_8_Eight_Vars',
        'constants': 8,
        'variables': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8'],
        'variables_to_eliminate': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8'],
        'complexity': 'Very-High',
        'inequalities': [
            'x1 + x2 + x3 + x4 + x5 <= a',
            'x2/(x6 + 1) + x7 + x8 <= b',
            'x1**2 + x3 + x5 >= c',
            'x4 + x6**2 + x7 <= d',
            'x2 + x8/(x1 + 3) >= e',
            'x5 + x6 + x7 + x8 <= f',
            'x7 + x8 >= g',
            'x8 <= h'
        ]
    })
    
    # Level 9: Nine variables, complex rational expressions
    test_cases.append({
        'name': 'Level_9_Nine_Vars',
        'constants': 8,
        'variables': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9'],
        'variables_to_eliminate': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9'],
        'complexity': 'Extreme',
        'inequalities': [
            'x1 + x2 + x3 + x4 + x5 + x6 <= a',
            'x2/(x7 + 1) + x8 + x9 <= b',
            'x1**2 + x3 + x5 + x7 >= c',
            'x4 + x6**2 + x8 + x9 <= d',
            'x1 + x7/(x2 + 2) + x9 >= e',
            'x5 + x6 + x8 <= f',
            'x7 + x8 + x9 >= g',
            'x9 <= h'
        ]
    })
    
    # Level 10: TARGET - Ten variables, seven equations, eight constants
    test_cases.append({
        'name': 'Level_10_TARGET',
        'constants': 8,
        'variables': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10'],
        'variables_to_eliminate': ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10'],
        'complexity': 'MAXIMUM',
        'inequalities': [
            'x1 + x2 + x3 + x4 + x5 + x6 + x7 <= a',           # 7 variables in one constraint
            'x2/(x8 + 1) + x9 + x10 <= b',                      # Rational with 3 variables
            'x1**2 + x3 + x5 + x7 + x9 >= c',                  # Polynomial with 5 variables  
            'x4 + x6**2 + x8 + x10 <= d',                      # Mixed polynomial, 4 variables
            'x1 + x7/(x2 + 2) + x9 + x10 >= e',               # Rational with 4 variables
            'x5 + x6 + x8 + x9 <= f',                          # Linear, 4 variables
            'x3 + x7 + x8 + x10 >= g'                          # Linear, 4 variables
        ]
    })
    
    return test_cases


def run_progressive_complexity_tests():
    """Run the complete progressive complexity test suite"""
    print("=" * 100)
    print("PROGRESSIVE COMPLEXITY TEST SUITE")
    print("Building up to: 8 constants, 10 variables, 7 equations")
    print("=" * 100)
    
    tester = ComplexityTester()
    test_cases = create_progressive_test_cases()
    
    print(f"\nCreated {len(test_cases)} test cases ranging from basic to maximum complexity")
    print(f"Target: Level 10 with 8 constants, 10 variables, 7 equations")
    print()
    
    successful_tests = 0
    total_time = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Running Test {i}/{len(test_cases)}: {test_case['name']}")
        print(f"   Progression: {test_case['constants']} constants, {len(test_case['variables'])} variables, {len(test_case['inequalities'])} equations")
        
        success, duration = tester.run_timed_test(test_case)
        total_time += duration
        
        if success:
            successful_tests += 1
            print(f"✅ Test {i} completed successfully in {duration:.3f}s")
        else:
            print(f"❌ Test {i} failed after {duration:.3f}s")
            
            # Ask user if they want to continue after failure
            print(f"\n⚠️  Test failed. Continue with remaining tests? (y/n): ", end="")
            response = input().strip().lower()
            if response != 'y' and response != 'yes':
                print("Stopping test suite at user request.")
                break
    
    # Print comprehensive summary
    tester.print_summary()
    
    # Final analysis
    print(f"\n🎯 FINAL RESULTS:")
    print(f"   Successfully completed: {successful_tests}/{len(test_cases)} tests")
    print(f"   Total execution time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    
    if successful_tests == len(test_cases):
        print(f"🏆 COMPLETE SUCCESS: All complexity levels handled!")
        print(f"   System successfully scaled to maximum target complexity:")
        print(f"   • 8 constants (a, b, c, d, e, f, g, h)")
        print(f"   • 10 variables (x1, x2, x3, x4, x5, x6, x7, x8, x9, x10)")  
        print(f"   • 7 complex equations with rational and polynomial expressions")
    else:
        highest_success = successful_tests
        print(f"🎯 MAXIMUM LEVEL REACHED: Level {highest_success}")
        print(f"   System handled complexity up to test {highest_success}")
        
        if highest_success >= 7:
            print(f"   🌟 Excellent performance - handled high complexity!")
        elif highest_success >= 5:
            print(f"   ✅ Good performance - handled moderate complexity")
        else:
            print(f"   ⚠️  Limited complexity handling - may need optimization")
    
    return successful_tests, total_time


if __name__ == "__main__":
    # Run the progressive complexity test suite
    successful, total_time = run_progressive_complexity_tests()
    
    print(f"\n" + "="*100)
    print(f"PROGRESSIVE COMPLEXITY TESTING COMPLETE")
    print(f"="*100)
    print(f"Result: {successful} successful tests, {total_time:.1f}s total time")
    print(f"Check output_final/ directory for generated LaTeX files")
    print(f"="*100)
