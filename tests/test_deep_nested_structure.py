#!/usr/bin/env python3

"""
Test for Deeper Nested Case Structure

This tests examples that should create multiple levels of nesting 
to verify the complete nested case tree structure.
"""

import sys
sys.path.append('/workspaces/codespaces-blank')

from nested_case_latex_generator import NestedCaseLatexGenerator
from datetime import datetime
import os

def test_deep_nested_structure():
    """
    Test cases that should create deeper nested structures.
    """
    print("=" * 80)
    print("TESTING DEEP NESTED CASE STRUCTURES")
    print("=" * 80)
    
    generator = NestedCaseLatexGenerator()
    
    # Test case that should create multiple levels
    print("TEST: Three Variables - Deep Nesting Expected")
    print("-" * 50)
    
    # System that should create cases at each elimination step
    system = [
        "x + y >= 1", 
        "x - y >= -1",    # Multiple bounds for x
        "y + z >= 2", 
        "y - z >= 0",     # Multiple bounds for y  
        "z >= 1",
        "z <= 3"          # Bounds for z
    ]
    variables = ['x', 'y', 'z']
    
    print(f"System: {system}")
    print(f"Variables to eliminate: {variables}")
    print()
    
    print("EXPECTED STRUCTURE:")
    print("Section: Eliminating Variable x")
    print("  Subsection: Case 1 (when x >= 1-y is tightest)")
    print("    Analysis: Eliminating y from Case 1")
    print("    Subsubsection: Case 1.1 (when y >= 2-z is tightest)")
    print("      Analysis: Eliminating z from Case 1.1")
    print("      Paragraph: Case 1.1.1 (final constraint on z)")
    print("      Paragraph: Case 1.1.2 (final constraint on z)")
    print("    Subsubsection: Case 1.2 (when y >= z is tightest)")
    print("      Final constraints for Case 1.2")
    print("  Subsection: Case 2 (when x >= y+1 is tightest)")
    print("    Similar nested structure...")
    print()
    
    # Generate the LaTeX
    latex_content = generator.generate_nested_case_latex(system, variables)
    
    # Save to file
    output_dir = "/workspaces/codespaces-blank/output_deep_test"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/deep_nested_test_{timestamp}.tex"
    
    with open(filename, 'w') as f:
        f.write(latex_content)
    
    print(f"✅ Generated deep nested LaTeX file: {filename}")
    
    # Test another case with guaranteed multiple cases at each level
    print("\n" + "=" * 60)
    print("TEST: Designed for Maximum Nesting")
    print("-" * 50)
    
    # System carefully designed to create cases at each step
    system2 = [
        "x + 2*y >= 1",
        "x - y >= 0",      # Two lower bounds for x
        "2*y + z >= 3", 
        "y - z >= -1",     # Mixed bounds for y
        "z >= 0"
    ]
    variables2 = ['x', 'y']  # Just two variables for clarity
    
    print(f"System: {system2}")
    print(f"Variables to eliminate: {variables2}")
    print()
    
    # Generate the LaTeX
    latex_content2 = generator.generate_nested_case_latex(system2, variables2)
    
    filename2 = f"{output_dir}/max_nested_test_{timestamp}.tex"
    
    with open(filename2, 'w') as f:
        f.write(latex_content2)
    
    print(f"✅ Generated max nested LaTeX file: {filename2}")
    
    return filename, filename2


def analyze_generated_latex(filename):
    """
    Analyze the generated LaTeX structure.
    """
    print(f"\n{'='*60}")
    print(f"ANALYZING GENERATED LATEX: {filename}")
    print(f"{'='*60}")
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Count nesting levels
    sections = content.count('\\section{')
    subsections = content.count('\\subsection{')
    subsubsections = content.count('\\subsubsection{')
    paragraphs = content.count('\\paragraph{')
    
    print(f"LaTeX Structure Analysis:")
    print(f"  Sections (\\section): {sections}")
    print(f"  Subsections (\\subsection): {subsections}")
    print(f"  Subsubsections (\\subsubsection): {subsubsections}")
    print(f"  Paragraphs (\\paragraph): {paragraphs}")
    print()
    
    # Find case analysis patterns
    case_analysis_count = content.count('Multiple lower bounds require case analysis')
    bound_analysis_count = content.count('Lower bounds for')
    final_results_count = content.count('Final Result for Case')
    
    print(f"Content Analysis:")
    print(f"  Case analysis sections: {case_analysis_count}")
    print(f"  Bound analysis sections: {bound_analysis_count}")
    print(f"  Final result sections: {final_results_count}")
    print()
    
    # Show structure preview
    print("Structure Preview:")
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if ('\\section{' in line or '\\subsection{' in line or 
            '\\subsubsection{' in line or '\\paragraph{' in line):
            indent = '  ' * (line.count('sub') + line.count('paragraph'))
            print(f"{indent}{line.strip()}")
    
    return {
        'sections': sections,
        'subsections': subsections, 
        'subsubsections': subsubsections,
        'paragraphs': paragraphs,
        'case_analysis': case_analysis_count,
        'bound_analysis': bound_analysis_count,
        'final_results': final_results_count
    }


if __name__ == "__main__":
    # Run the deep nesting tests
    filename1, filename2 = test_deep_nested_structure()
    
    # Analyze the results
    print("\n" * 2)
    stats1 = analyze_generated_latex(filename1)
    stats2 = analyze_generated_latex(filename2)
    
    print(f"\n{'='*80}")
    print("FINAL EVALUATION")
    print(f"{'='*80}")
    
    print(f"Deep nesting test statistics: {stats1}")
    print(f"Max nesting test statistics: {stats2}")
    
    print("\nStructure Quality Assessment:")
    if stats1['subsubsections'] > 0 or stats2['subsubsections'] > 0:
        print("✅ SUCCESS: Generated proper nested structure with subsubsections")
    else:
        print("⚠️  WARNING: Limited nesting depth - may need adjustment")
    
    if stats1['case_analysis'] > 1 or stats2['case_analysis'] > 1:
        print("✅ SUCCESS: Multiple case analysis sections generated")
    else:
        print("⚠️  WARNING: Limited case analysis - may need more complex examples")
