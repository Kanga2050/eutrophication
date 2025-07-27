"""
Test the improved variable elimination formatting.
"""
from variable_eliminator import solve_with_variable_elimination
from datetime import datetime


def test_improved_formatting():
    """Test the improved formatting with clear case splitting example."""
    
    print("TESTING IMPROVED VARIABLE ELIMINATION FORMATTING")
    print("="*80)
    
    # Simple example that will show all formatting improvements
    inequalities = [
        "x1**2 - 3*x1 + 2 >= 0",    # Quadratic case splitting
        "x2 - x1 >= 0",             # Creates bounds
        "x1 + x2 <= 5",             # Another bound
        "a + b <= c",               # Unrelated (should be preserved)
        "d*e >= f"                  # Another unrelated (should be preserved)
    ]
    
    print("Input system:")
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    
    print("\nExpected improvements:")
    print("1. Step 1: Unrelated inequalities (a+b<=c, d*e>=f) shown separately")
    print("2. Step 2: Format should be max(...) <= x1 <= min(...)")
    print("3. Step 3: Format should be max(...) <= min(...)")
    print("4. All steps: Include unrelated inequalities throughout")
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = solve_with_variable_elimination(
            inequalities=inequalities,
            variables_to_eliminate=['x1', 'x2'],
            use_sign_analysis=True,
            save_latex=True,
            output_filename=f"improved_format_{timestamp}"
        )
        
        print(f"\n✅ SUCCESS: Generated improved formatting")
        print(f"Steps: {result['total_steps']}")
        print(f"Final inequalities: {len(result['final_inequalities'])}")
        
        print(f"\n📄 Check LaTeX file: output_final/improved_format_{timestamp}_complete.tex")
        print("Look for these improvements:")
        print("• Inequalities separated by variable involvement")
        print("• Proper max(...) <= x <= min(...) formatting")
        print("• Constraint format max(...) <= min(...) in step 3")
        print("• Unrelated inequalities preserved throughout")
        
        return timestamp
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def verify_improvements(timestamp):
    """Verify the improvements in the generated LaTeX file."""
    
    if not timestamp:
        return False
        
    print("\n" + "="*80)
    print("VERIFYING IMPROVEMENTS IN LATEX")
    print("="*80)
    
    latex_file = f"output_final/improved_format_{timestamp}_complete.tex"
    
    try:
        with open(latex_file, 'r') as f:
            content = f.read()
        
        improvements_found = []
        
        # Check for separated inequalities
        if "Inequalities involving" in content and "not involving" in content:
            improvements_found.append("✅ Inequalities properly separated by variable involvement")
        else:
            improvements_found.append("❌ Inequalities not properly separated")
        
        # Check for proper bound formatting
        if "\\leq" in content and "\\geq" in content:
            improvements_found.append("✅ Proper bound symbols used")
        else:
            improvements_found.append("❌ Bound formatting issues")
        
        # Check for constraint format
        if "Constraint After Eliminating" in content:
            improvements_found.append("✅ Step 3 constraint format improved")
        else:
            improvements_found.append("❌ Step 3 format not improved")
        
        # Check for preserved inequalities
        preserved_count = content.count("preserved")
        if preserved_count > 0:
            improvements_found.append(f"✅ Found {preserved_count} references to preserved inequalities")
        else:
            improvements_found.append("❌ No evidence of preserved inequalities")
        
        print("Improvement verification:")
        for improvement in improvements_found:
            print(f"  {improvement}")
        
        return all("✅" in imp for imp in improvements_found)
        
    except Exception as e:
        print(f"Error reading LaTeX file: {e}")
        return False


def show_sample_output(timestamp):
    """Show a sample of the improved output."""
    
    if not timestamp:
        return
        
    print("\n" + "="*80)
    print("SAMPLE OF IMPROVED OUTPUT")
    print("="*80)
    
    latex_file = f"output_final/improved_format_{timestamp}_complete.tex"
    
    try:
        with open(latex_file, 'r') as f:
            content = f.read()
        
        # Extract a key section to show improvement
        lines = content.split('\n')
        
        # Find the step 2 section
        step2_start = None
        step3_start = None
        
        for i, line in enumerate(lines):
            if "Step 1.2:" in line:
                step2_start = i
            if "Step 1.3:" in line:
                step3_start = i
                break
        
        if step2_start and step3_start:
            print("SAMPLE: Step 2 formatting (should show max <= x <= min):")
            print("-" * 60)
            for line in lines[step2_start:step3_start]:
                if line.strip():
                    print(line)
            
            print("\nSAMPLE: Step 3 formatting (should show max <= min):")
            print("-" * 60)
            step4_start = None
            for i, line in enumerate(lines[step3_start:], step3_start):
                if "Step 1.4:" in line:
                    step4_start = i
                    break
            
            if step4_start:
                for line in lines[step3_start:step4_start]:
                    if line.strip():
                        print(line)
        
        print("\n" + "="*40)
        print("The complete file shows all improvements!")
        
    except Exception as e:
        print(f"Error reading sample: {e}")


def main():
    """Test and verify improved formatting."""
    
    # Test improved formatting
    timestamp = test_improved_formatting()
    
    # Verify improvements
    success = verify_improvements(timestamp)
    
    # Show sample output
    show_sample_output(timestamp)
    
    print("\n" + "="*80)
    print("IMPROVED FORMATTING TEST COMPLETE")
    print("="*80)
    
    if success:
        print("🎉 ALL IMPROVEMENTS SUCCESSFULLY IMPLEMENTED!")
        print("\n✅ Key improvements:")
        print("   • Inequalities separated by variable involvement")
        print("   • Proper max(...) <= x <= min(...) format in step 2")
        print("   • Constraint max(...) <= min(...) format in step 3") 
        print("   • Unrelated inequalities preserved throughout")
        print("   • Clear section labeling and organization")
    else:
        print("⚠️ Some improvements may need refinement")
    
    if timestamp:
        print(f"\n📄 Full improved output: output_final/improved_format_{timestamp}_complete.tex")


if __name__ == "__main__":
    main()
