"""
Demonstration script for the LaTeX processor module.
Shows how to use LaTeX processing features independently.
"""
from latex_processor import (
    process_and_save_latex, 
    generate_summary_report,
    clean_case_label,
    format_latex_expression,
    create_latex_document
)
from examples import run_example


def demo_latex_processing():
    """Demonstrate LaTeX processing capabilities."""
    print("LaTeX Processor Demonstration")
    print("=" * 50)
    
    # Example LaTeX results (simplified)
    sample_results = [
        r"\textbf{Case 1: positive condition}\\[1em]\left\{x > 0 \wedge -2 < x < 2\right\}\\[1em]\left\{x > 0 \wedge -2 \le x \le 2\right\}",
        r"\textbf{Case 2: negative condition}\\[1em]\left\{x < 0 \wedge x > -3\right\}\\[1em]\left\{x < 0 \wedge x \ge -3\right\}"
    ]
    
    # Test clean_case_label function
    print("\n1. Testing case label cleaning:")
    verbose_label = "Case 1: Entire expression <= 0 because very long expression with many terms >= 0 and denominator > 0"
    clean_label = clean_case_label(verbose_label)
    print(f"   Original: {verbose_label}")
    print(f"   Cleaned:  {clean_label}")
    
    # Test expression formatting
    print("\n2. Testing expression formatting:")
    long_expr = r"\frac{a + b + c + d + e + f + g + h + i + j + k + l + m + n}{x + y + z + w + v + u + t + s + r + q + p}"
    formatted_expr = format_latex_expression(long_expr, 40)
    print(f"   Original: {long_expr}")
    print(f"   Formatted:\n{formatted_expr}")
    
    # Test document creation
    print("\n3. Creating LaTeX document:")
    latex_doc = create_latex_document(sample_results, "Demo Inequality Solutions")
    print(f"   Document created with {len(latex_doc)} characters")
    
    # Test file saving
    print("\n4. Testing file operations:")
    try:
        saved_files = process_and_save_latex(sample_results, "demo_solutions")
        summary = generate_summary_report(sample_results, saved_files)
        print("   " + "\n   ".join(summary.split("\n")))
    except Exception as e:
        print(f"   Error: {e}")


def demo_with_real_example():
    """Run a real example and show LaTeX processing."""
    print("\n" + "=" * 60)
    print("REAL EXAMPLE WITH LATEX PROCESSING")
    print("=" * 60)
    
    # Run a simple example
    results = run_example('rational')
    
    if results:
        print(f"\nGenerated {len(results)} LaTeX results")
        print("Files saved in 'output/' directory")
    else:
        print("Failed to generate results")


def demo_custom_latex_processing():
    """Show how to use LaTeX processor with custom results."""
    print("\n" + "=" * 60)
    print("CUSTOM LATEX PROCESSING")
    print("=" * 60)
    
    # Create some custom LaTeX results
    custom_results = [
        r"\textbf{Linear Case}\\[1em]\left\{a > 0 \wedge x > \frac{-b}{a}\right\}\\[1em]\left\{a > 0 \wedge x \ge \frac{-b}{a}\right\}",
        r"\textbf{Quadratic Case}\\[1em]\left\{\Delta \ge 0 \wedge r_1 < x < r_2\right\}\\[1em]\left\{\Delta \ge 0 \wedge r_1 \le x \le r_2\right\}"
    ]
    
    try:
        # Process and save
        saved_files = process_and_save_latex(custom_results, "custom_demo", "custom_output")
        
        print("Custom LaTeX processing completed!")
        print(f"Files saved to 'custom_output/' directory:")
        for file_type, path in saved_files.items():
            print(f"  {file_type}: {path}")
            
    except Exception as e:
        print(f"Error in custom processing: {e}")


if __name__ == "__main__":
    # Run all demonstrations
    demo_latex_processing()
    demo_with_real_example() 
    demo_custom_latex_processing()
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("Check the 'output/' and 'custom_output/' directories for generated files.")
