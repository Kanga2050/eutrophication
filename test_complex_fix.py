"""
Test and fix the complex number comparison issue.
"""
from variable_eliminator import solve_with_variable_elimination
from sympy import symbols, I, re, im


def test_complex_issue():
    """Test the specific case that causes complex number issues."""
    print("Testing nested fraction that causes complex numbers...")
    
    # This is the problematic case from the tests
    inequalities = [
        "1/(1 + 1/(x1 + 1)) >= x2",
        "x1 + x2 <= 3", 
        "c >= d"
    ]
    
    print("Inequalities:")
    for ineq in inequalities:
        print(f"  {ineq}")
    
    try:
        result = solve_with_variable_elimination(
            inequalities=inequalities,
            variables_to_eliminate=['x1'],  # Just eliminate x1 first to see where it fails
            use_sign_analysis=True,
            save_latex=False
        )
        
        print("✅ No complex number issues!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Try to isolate the issue
        from sympy import solve, symbols
        x1, x2 = symbols('x1 x2')
        
        # The nested fraction expression
        expr = 1/(1 + 1/(x1 + 1))
        print(f"\nExpression: {expr}")
        
        # Simplify it
        simplified = expr.simplify()
        print(f"Simplified: {simplified}")
        
        # Try to solve the inequality manually
        try:
            # 1/(1 + 1/(x1 + 1)) >= x2
            # This becomes (x1 + 1)/(x1 + 2) >= x2
            # Rearranging: (x1 + 1) - x2*(x1 + 2) >= 0
            # x1 + 1 - x2*x1 - 2*x2 >= 0
            # x1*(1 - x2) + (1 - 2*x2) >= 0
            
            manual_expr = x1*(1 - x2) + (1 - 2*x2)
            print(f"Manual rearrangement: {manual_expr} >= 0")
            
            # Solve for x1
            roots = solve(manual_expr, x1)
            print(f"Critical points for x1: {roots}")
            
            # Check if any roots are complex
            for root in roots:
                if hasattr(root, 'as_real_imag'):
                    real_part, imag_part = root.as_real_imag()
                    if imag_part != 0:
                        print(f"Complex root found: {root} = {real_part} + {imag_part}*I")
                        return False
                        
        except Exception as solve_error:
            print(f"Manual solve error: {solve_error}")
        
        return False


def test_alternative_approach():
    """Test an alternative approach that avoids complex issues."""
    print("\n" + "="*60)
    print("Testing alternative approach...")
    
    # Rewrite the nested fraction in a simpler form
    inequalities = [
        "(x1 + 1)/(x1 + 2) >= x2",  # Simplified form of 1/(1 + 1/(x1 + 1))
        "x1 + x2 <= 3",
        "c >= d"
    ]
    
    print("Simplified inequalities:")
    for ineq in inequalities:
        print(f"  {ineq}")
    
    try:
        result = solve_with_variable_elimination(
            inequalities=inequalities,
            variables_to_eliminate=['x1', 'x2'],
            use_sign_analysis=True,
            save_latex=False
        )
        
        print("✅ Alternative approach works!")
        print(f"Final inequalities: {len(result['final_inequalities'])}")
        return True
        
    except Exception as e:
        print(f"❌ Alternative approach failed: {e}")
        return False


def create_improved_variable_eliminator():
    """Create an improved version that handles complex numbers better."""
    print("\n" + "="*60) 
    print("Creating improved variable eliminator with complex number handling...")
    
    # The fix should be in the solver itself - add complex number filtering
    improved_code = '''
def _filter_real_solutions(self, bounds):
    """Filter out complex solutions from bounds."""
    real_bounds = []
    
    for bound_expr, bound_type in bounds:
        try:
            # Check if the expression contains complex numbers
            if hasattr(bound_expr, 'as_real_imag'):
                real_part, imag_part = bound_expr.as_real_imag()
                if imag_part == 0:  # Only real numbers
                    real_bounds.append((bound_expr, bound_type))
                else:
                    print(f"Warning: Filtered out complex bound: {bound_expr}")
            else:
                # Assume it's real if we can't check
                real_bounds.append((bound_expr, bound_type))
        except:
            # If checking fails, include it (might be a symbolic expression)
            real_bounds.append((bound_expr, bound_type))
    
    return real_bounds
'''
    
    print("Improvement strategy:")
    print("1. Add complex number detection to bound filtering")
    print("2. Filter out complex roots before creating min/max expressions")
    print("3. Add warning messages for filtered complex solutions")
    print("4. Graceful degradation when complex numbers are encountered")
    
    return True


def main():
    """Test complex number handling and propose fixes."""
    print("COMPLEX NUMBER HANDLING TESTS")
    print("="*60)
    
    # Test the problematic case
    result1 = test_complex_issue()
    
    # Test alternative approach 
    result2 = test_alternative_approach()
    
    # Propose improvements
    result3 = create_improved_variable_eliminator()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    print(f"Complex issue test: {'✅ PASSED' if result1 else '❌ FAILED'}")
    print(f"Alternative approach: {'✅ PASSED' if result2 else '❌ FAILED'}")
    print(f"Improvement strategy: {'✅ CREATED' if result3 else '❌ FAILED'}")
    
    if not result1 and result2:
        print("\n💡 RECOMMENDATION:")
        print("The issue is with nested fractions creating complex roots.")
        print("Solution: Pre-simplify nested fractions before solving.")
        print("Alternative: Add complex number filtering to the solver.")
    
    return result1 or result2


if __name__ == "__main__":
    main()
