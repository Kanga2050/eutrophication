import sys
import os
# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#!/usr/bin/env python3
"""
Demonstration script showing the benefits of sign analysis for case reduction.
"""
from sympy import symbols, pi, exp, log, parse_expr
from solver import solve_rational_ineq_full
from case_processor import generate_case_labeled_bounds
from latex_processor import process_and_save_latex

def demo_sign_analysis_benefits():
    """Demonstrate the case reduction benefits of sign analysis."""
    x = symbols('x')
    
    print("=== SIGN ANALYSIS DEMONSTRATION ===")
    print("Showing how sign analysis reduces case complexity\n")
    
    # Example 1: Expression with always positive denominator
    print("Example 1: (x - 2) / (x² + 1) ≤ 0")
    print("Analysis: x² + 1 is always positive, so we only need one case")
    print("-" * 60)
    
    expr1_cases = [(parse_expr('x - 2'), '<=', parse_expr('x**2 + 1'))]
    
    # With sign analysis
    results_with = generate_case_labeled_bounds(expr1_cases, x, solve_rational_ineq_full, use_sign_analysis=True)
    print(f"WITH sign analysis: {len(results_with)} case(s)")
    
    # Without sign analysis  
    results_without = generate_case_labeled_bounds(expr1_cases, x, solve_rational_ineq_full, use_sign_analysis=False)
    print(f"WITHOUT sign analysis: {len(results_without)} case(s)")
    
    reduction1 = ((len(results_without) - len(results_with)) / len(results_without)) * 100 if len(results_without) > 0 else 0
    print(f"Case reduction: {reduction1:.1f}%\n")
    
    # Save LaTeX output for this example
    process_and_save_latex(
        results_with, 
        "demo_with_sign_analysis",
        "output"
    )
    
    process_and_save_latex(
        results_without,
        "demo_without_sign_analysis",
        "output"
    )
    
    # Example 2: Expression with mathematical constants
    print("Example 2: (x - π) / eˣ ≥ 0")
    print("Analysis: eˣ is always positive, so denominator sign is known")
    print("-" * 60)
    
    expr2_cases = [(parse_expr('x - pi'), '>=', parse_expr('exp(x)'))]
    
    # With sign analysis
    results2_with = generate_case_labeled_bounds(expr2_cases, x, solve_rational_ineq_full, use_sign_analysis=True)
    print(f"WITH sign analysis: {len(results2_with)} case(s)")
    
    # Without sign analysis
    results2_without = generate_case_labeled_bounds(expr2_cases, x, solve_rational_ineq_full, use_sign_analysis=False)  
    print(f"WITHOUT sign analysis: {len(results2_without)} case(s)")
    
    reduction2 = ((len(results2_without) - len(results2_with)) / len(results2_without)) * 100 if len(results2_without) > 0 else 0
    print(f"Case reduction: {reduction2:.1f}%\n")
    
    # Example 3: Always negative over always positive
    print("Example 3: -5 / (x² + 3) < 0")
    print("Analysis: Numerator always negative, denominator always positive")
    print("-" * 60)
    
    expr3_cases = [(parse_expr('-5'), '<', parse_expr('x**2 + 3'))]
    
    # With sign analysis
    results3_with = generate_case_labeled_bounds(expr3_cases, x, solve_rational_ineq_full, use_sign_analysis=True)
    print(f"WITH sign analysis: {len(results3_with)} case(s)")
    
    # Without sign analysis
    results3_without = generate_case_labeled_bounds(expr3_cases, x, solve_rational_ineq_full, use_sign_analysis=False)
    print(f"WITHOUT sign analysis: {len(results3_without)} case(s)")
    
    reduction3 = ((len(results3_without) - len(results3_with)) / len(results3_without)) * 100 if len(results3_without) > 0 else 0
    print(f"Case reduction: {reduction3:.1f}%\n")
    
    # Summary
    total_with = len(results_with) + len(results2_with) + len(results3_with)
    total_without = len(results_without) + len(results2_without) + len(results3_without)
    overall_reduction = ((total_without - total_with) / total_without) * 100 if total_without > 0 else 0
    
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total cases WITH sign analysis: {total_with}")
    print(f"Total cases WITHOUT sign analysis: {total_without}")
    print(f"Overall case reduction: {overall_reduction:.1f}%")
    print(f"Cases eliminated: {total_without - total_with}")
    
    print("\nFiles generated:")
    print("  demo_with_sign_analysis_raw.txt - Copy-paste ready LaTeX (with optimization)")
    print("  demo_without_sign_analysis_raw.txt - Copy-paste ready LaTeX (without optimization)")

if __name__ == "__main__":
    demo_sign_analysis_benefits()
