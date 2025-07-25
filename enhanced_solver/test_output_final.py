"""
Demonstration of the output_final folder functionality.

This script shows how the enhanced solver now saves complete LaTeX reports
to both the standard output folder and the new output_final folder.
"""
import os
from enhanced_solver import solve_with_elimination


def test_output_final():
    """Test the output_final folder functionality."""
    
    print("Testing output_final folder functionality")
    print("=" * 50)
    
    # Simple test system
    inequalities = [
        "x1 + x2 >= 0",
        "x1**2 - 4 <= 0", 
        "x2 - 1 >= 0",
        "a + b <= c"
    ]
    
    variables = ['x1', 'x2']
    
    print("Test system:")
    for ineq in inequalities:
        print(f"  {ineq}")
    
    print(f"\nVariables to eliminate: {variables}")
    print("\nRunning solver with output_final functionality...")
    
    # Run solver with custom filename
    result = solve_with_elimination(
        inequalities, 
        variables,
        output_filename="output_final_test"
    )
    
    print("\nChecking generated files...")
    
    # Check standard output folder
    output_dir = "output"
    standard_tex = os.path.join(output_dir, "output_final_test.tex")
    summary_txt = os.path.join(output_dir, "output_final_test_summary.txt")
    
    # Check output_final folder
    final_dir = "output_final"
    complete_tex = os.path.join(final_dir, "output_final_test_complete.tex")
    
    print(f"\nFiles generated:")
    print(f"Standard LaTeX: {standard_tex} - {'✓' if os.path.exists(standard_tex) else '✗'}")
    print(f"Text summary:   {summary_txt} - {'✓' if os.path.exists(summary_txt) else '✗'}")
    print(f"Complete LaTeX: {complete_tex} - {'✓' if os.path.exists(complete_tex) else '✗'}")
    
    if os.path.exists(complete_tex):
        print(f"\nComplete LaTeX file size: {os.path.getsize(complete_tex)} bytes")
        
        # Show a preview of the complete LaTeX
        with open(complete_tex, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            print(f"Complete LaTeX preview (first 10 lines):")
            for i, line in enumerate(lines[:10]):
                print(f"  {i+1}: {line}")
    
    print(f"\nSolver results:")
    print(f"  Total steps: {result['total_steps']}")
    print(f"  Final inequalities: {len(result['final_inequalities'])}")
    
    print(f"\nBenefits of output_final folder:")
    print(f"  • Contains complete step-by-step documentation")
    print(f"  • Shows all 4 steps for each variable elimination")
    print(f"  • Professional LaTeX formatting ready for compilation")
    print(f"  • Separate from summary outputs for organization")


if __name__ == "__main__":
    test_output_final()
