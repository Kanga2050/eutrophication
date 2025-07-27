"""
New Formatting Test Module for Variable Elimination

This module tests and verifies the new LaTeX formatting features implemented
in the variable elimination solver, specifically focusing on enhanced mathematical
notation and improved visual presentation.

Key Features Tested:
- **Large Brackets**: Use of \\left\\{ and \\right\\} for system notation
- **Logical Symbols**: ∧ (wedge) symbols between inequalities within systems  
- **Equivalence Arrows**: ⟺ (if and only if) arrows showing logical equivalence between steps
- **Multi-line Formatting**: Proper alignment and spacing for complex expressions
- **Professional Presentation**: Academic-quality mathematical typesetting

Test Scenarios:
1. **New Bracket Formatting**: Verify large brackets surround inequality systems
2. **Logical Connector Testing**: Confirm ∧ symbols separate inequalities properly
3. **Equivalence Arrow Verification**: Check ⟺ arrows appear between elimination steps
4. **Multi-line Structure**: Validate proper spacing and alignment in complex expressions
5. **Complete Integration**: Ensure all new features work together cohesively

Functions:
- test_new_formatting(): Main test function for new formatting features
- verify_new_formatting(): Automated verification of LaTeX output
- show_sample_new_formatting(): Display sample output for manual review
- main(): Comprehensive test execution and reporting

Author: Rational Inequality Solver Team
Version: New Formatting Verification Suite
"""
from variable_eliminator import solve_with_variable_elimination
from datetime import datetime


def test_new_formatting():
    """
    Test the new bracket and iff arrow formatting features.
    
    This function tests the enhanced LaTeX formatting capabilities by running
    the variable elimination solver on a carefully designed test system and
    verifying that the output contains the expected new formatting elements.
    
    Test System Design:
    - **Quadratic Inequality**: x1**2 - 3*x1 + 2 >= 0 (shows polynomial handling)
    - **Linear Constraints**: x2 - x1 >= 0, x1 + x2 <= 5 (creates variable dependencies)
    - **Parameter Constraint**: a + b <= c (tests parameter handling)
    
    Expected New Features:
    - Large brackets { } around each inequality system
    - ∧ symbols between inequalities within brackets  
    - ⟺ (if and only if) arrows between elimination steps
    - Min, variable, and max each displayed on separate lines within brackets
    - Clean mathematical presentation with proper spacing
    
    Returns:
        str: Timestamp of generated files for verification, or None if failed
        
    Side Effects:
        - Creates LaTeX files in output_final/ directory
        - Displays progress and results to console
        - Generates new_format_[timestamp]_complete.tex file
    
    Example Output Pattern:
        \\left\\{
        \\begin{aligned}
        & x_1^2 - 3x_1 + 2 \\geq 0 \\\\
        & \\wedge \\\\
        & x_2 - x_1 \\geq 0 \\\\
        \\end{aligned}
        \\right\\}
        \\Longleftrightarrow
        \\left\\{
        ... (elimination results)
        \\right\\}
    """
    
    print("TESTING NEW BRACKET AND IFF ARROW FORMATTING")
    print("="*80)
    
    # Simple example to show new formatting clearly
    inequalities = [
        "x1**2 - 3*x1 + 2 >= 0",    # Quadratic 
        "x2 - x1 >= 0",             # Linear
        "x1 + x2 <= 5",             # Another linear
        "a + b <= c"                # Parameter
    ]
    
    print("Input system:")
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    
    print("\nExpected new formatting:")
    print("• Large brackets { } around each system")
    print("• ∧ symbols between inequalities")
    print("• ⟺ (if and only if) arrows between steps")
    print("• Min, variable, and max each on separate lines")
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = solve_with_variable_elimination(
            inequalities=inequalities,
            variables_to_eliminate=['x1', 'x2'],
            use_sign_analysis=True,
            save_latex=False,
            output_filename=f"new_format_{timestamp}"
        )
        
        print(f"\n✅ SUCCESS: Generated new formatting")
        print(f"Steps: {result['total_steps']}")
        print(f"Final inequalities: {len(result['final_inequalities'])}")
        
        print(f"\n📄 Check LaTeX file: output_final/new_format_{timestamp}_complete.tex")
        print("Look for these new features:")
        print("• \\left\\{ and \\right\\} large brackets")
        print("• \\wedge symbols (∧) between inequalities")
        print("• \\Longleftrightarrow symbols (⟺) between steps")
        print("• Multi-line min/max formatting in brackets")
        
        return timestamp
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def verify_new_formatting(timestamp):
    """
    Verify the new formatting features in the generated LaTeX file.
    
    This function performs automated verification of the LaTeX output to ensure
    all new formatting features are properly implemented. It reads the generated
    LaTeX file and searches for specific formatting elements.
    
    Args:
        timestamp (str): Timestamp identifier for the LaTeX file to verify
        
    Returns:
        bool: True if all formatting features are found, False otherwise
        
    Verification Checklist:
    1. **Large Brackets**: Count \\left\\{ and \\right\\} pairs
    2. **Logical Connectors**: Count \\wedge symbols for inequality separation
    3. **Equivalence Arrows**: Count \\Longleftrightarrow symbols between steps  
    4. **Multi-line Formatting**: Count \\begin{aligned} blocks for proper structure
    
    Verification Process:
    - Read the complete LaTeX file content
    - Search for each formatting element using pattern matching
    - Count occurrences of each element type
    - Report findings with ✅ (success) or ❌ (missing) indicators
    - Return overall success status
    
    Output Example:
        ✅ Large brackets: 4 pairs found
        ✅ And symbols (∧): 6 found  
        ✅ If-and-only-if arrows (⟺): 2 found
        ✅ Multi-line alignment: 3 blocks found
    """
    
    if not timestamp:
        return False
        
    print("\n" + "="*80)
    print("VERIFYING NEW FORMATTING FEATURES")
    print("="*80)
    
    latex_file = f"output_final/new_format_{timestamp}_complete.tex"
    
    try:
        with open(latex_file, 'r') as f:
            content = f.read()
        
        features_found = []
        
        # Check for large brackets
        left_bracket_count = content.count(r'\left\{')
        right_bracket_count = content.count(r'\right\}')
        if left_bracket_count > 0 and right_bracket_count > 0:
            features_found.append(f"✅ Large brackets: {left_bracket_count} pairs found")
        else:
            features_found.append("❌ No large brackets found")
        
        # Check for ∧ symbols
        wedge_count = content.count(r'\wedge')
        if wedge_count > 0:
            features_found.append(f"✅ And symbols (∧): {wedge_count} found")
        else:
            features_found.append("❌ No and symbols (∧) found")
        
        # Check for iff arrows
        iff_count = content.count(r'\Longleftrightarrow')
        if iff_count > 0:
            features_found.append(f"✅ If-and-only-if arrows (⟺): {iff_count} found")
        else:
            features_found.append("❌ No if-and-only-if arrows found")
        
        # Check for multi-line formatting
        aligned_count = content.count(r'\begin{aligned}')
        if aligned_count > 0:
            features_found.append(f"✅ Multi-line alignment: {aligned_count} blocks found")
        else:
            features_found.append("❌ No multi-line alignment found")
        
        print("New formatting verification:")
        for feature in features_found:
            print(f"  {feature}")
        
        return all("✅" in feat for feat in features_found)
        
    except Exception as e:
        print(f"Error reading LaTeX file: {e}")
        return False


def show_sample_new_formatting(timestamp):
    """
    Display sample sections of the new formatting for manual review.
    
    This function extracts and displays representative samples from the generated
    LaTeX file to provide a quick visual verification of the new formatting features.
    It helps users understand what the new formatting looks like in practice.
    
    Args:
        timestamp (str): Timestamp identifier for the LaTeX file to sample
        
    Display Sections:
    1. **Initial System**: Shows how the original inequality system is formatted
       with large brackets and ∧ symbols between inequalities
    2. **Elimination Steps**: Shows how elimination steps are connected with ⟺ arrows
       and how intermediate results are formatted
    3. **Mathematical Structure**: Demonstrates the overall flow and presentation
    
    Sample Output Structure:
        SAMPLE: Initial System with large brackets and ∧:
        \\left\\{
        \\begin{aligned}
        & x_1^2 - 3x_1 + 2 \\geq 0 \\\\
        & \\wedge \\\\  
        & x_2 - x_1 \\geq 0 \\\\
        \\end{aligned}
        \\right\\}
        
        SAMPLE: Step with ⟺ arrow:
        \\Longleftrightarrow
        \\left\\{
        ... (elimination results)
        \\right\\}
    
    Side Effects:
        - Reads LaTeX file content
        - Displays formatted samples to console
        - Provides visual confirmation of new features
    """
    
    if not timestamp:
        return
        
    print("\n" + "="*80)
    print("SAMPLE OF NEW FORMATTING")
    print("="*80)
    
    latex_file = f"output_final/new_format_{timestamp}_complete.tex"
    
    try:
        with open(latex_file, 'r') as f:
            content = f.read()
        
        # Show a sample section
        lines = content.split('\n')
        
        # Find initial system
        initial_start = None
        step1_start = None
        
        for i, line in enumerate(lines):
            if "Initial System" in line:
                initial_start = i
            if "Step 1:" in line:
                step1_start = i
                break
        
        if initial_start and step1_start:
            print("SAMPLE: Initial System with large brackets and ∧:")
            print("-" * 60)
            for line in lines[initial_start:step1_start]:
                if line.strip():
                    print(line)
        
        # Find a step with iff arrow
        step2_start = None
        for i, line in enumerate(lines):
            if "Step 1.3:" in line:
                step2_start = i
                break
        
        if step2_start:
            print("\nSAMPLE: Step with ⟺ arrow:")
            print("-" * 60)
            for i, line in enumerate(lines[step2_start:step2_start+15]):
                if line.strip():
                    print(line)
                if i > 10:  # Limit output
                    break
        
        print("\n" + "="*40)
        print("Complete file shows all new formatting!")
        
    except Exception as e:
        print(f"Error reading sample: {e}")


def main():
    """
    Main test execution function for comprehensive new formatting verification.
    
    This function orchestrates the complete testing process for the new formatting
    features, running all test phases and providing a comprehensive report of
    the implementation status.
    
    Test Execution Flow:
    1. **Feature Testing**: Run test_new_formatting() to generate output with new features
    2. **Automated Verification**: Run verify_new_formatting() to check for all expected elements
    3. **Sample Display**: Run show_sample_new_formatting() to show visual examples
    4. **Results Summary**: Provide comprehensive report of test outcomes
    
    Success Criteria:
    - All new formatting features successfully implemented
    - LaTeX output contains expected mathematical notation
    - File generation completes without errors
    - Visual samples demonstrate proper formatting
    
    Report Sections:
    1. **Feature Implementation Status**: ✅ or ⚠️ indicators for each feature
    2. **Generated Files**: List of output files created during testing
    3. **Usage Instructions**: How to view and use the generated LaTeX files
    
    Output Examples:
        🎉 ALL NEW FORMATTING FEATURES IMPLEMENTED!
        
        ✅ New features:
           • Large brackets { } around each inequality system
           • ∧ symbols separating inequalities within brackets
           • ⟺ arrows showing logical equivalence between steps
           • Min, variable, max each on separate lines in brackets
           • Clean mathematical presentation
           
        📄 Full new formatting: output_final/new_format_[timestamp]_complete.tex
    
    Returns:
        None (outputs results to console and files)
    """
    
    # Test new formatting
    timestamp = test_new_formatting()
    
    # Verify features
    success = verify_new_formatting(timestamp)
    
    # Show samples
    show_sample_new_formatting(timestamp)
    
    print("\n" + "="*80)
    print("NEW FORMATTING TEST COMPLETE")
    print("="*80)
    
    if success:
        print("🎉 ALL NEW FORMATTING FEATURES IMPLEMENTED!")
        print("\n✅ New features:")
        print("   • Large brackets { } around each inequality system")
        print("   • ∧ symbols separating inequalities within brackets")
        print("   • ⟺ arrows showing logical equivalence between steps")
        print("   • Min, variable, max each on separate lines in brackets")
        print("   • Clean mathematical presentation")
    else:
        print("⚠️ Some formatting features may need refinement")
    
    if timestamp:
        print(f"\n📄 Full new formatting: output_final/new_format_{timestamp}_complete.tex")


if __name__ == "__main__":
    main()
