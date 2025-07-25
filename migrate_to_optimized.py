"""
Migration utilities for transitioning from old to new architecture.
"""
import shutil
from pathlib import Path
from typing import List, Dict, Any


def create_legacy_compatibility_layer():
    """Create compatibility layer for old imports."""
    
    # Create compatibility modules that redirect to new architecture
    compatibility_modules = {
        'solver.py': '''"""
Legacy compatibility module for solver.py
This module provides backward compatibility while redirecting to the new architecture.
"""

# Import from new architecture
from rational_inequality_solver.core.solver_engine import SolverEngine
from rational_inequality_solver.core.sign_analyzer import create_optimized_analyzer

# Legacy function name compatibility
def solve_rational_ineq_full(expr, x, op, use_sign_analysis=True):
    """
    Legacy compatibility function for solve_rational_ineq_full.
    
    This function maintains the same interface as the original but uses
    the optimized solver engine internally.
    """
    # Create a temporary solver instance
    solver = SolverEngine(use_sign_analysis=use_sign_analysis)
    
    # Use the optimized internal method
    return solver._solve_rational_inequality(expr, x, op)

# Maintain other legacy exports if needed
__all__ = ['solve_rational_ineq_full']
''',

        'case_processor.py': '''"""
Legacy compatibility module for case_processor.py
"""

from rational_inequality_solver.processors.case_processor import CaseProcessor
from rational_inequality_solver.core.inequality_system import InequalitySystem

def isolate_cases_from_solver(solver_output):
    """Legacy compatibility function."""
    processor = CaseProcessor()
    return processor._parse_solver_output(solver_output)

def generate_case_labeled_bounds(ineq_list, x, solver_func, use_sign_analysis=True):
    """Legacy compatibility function."""
    # Convert to new system format
    system = InequalitySystem([(lhs - rhs, op, 0) for lhs, op, rhs in ineq_list], x)
    
    # Create processor and solve
    processor = CaseProcessor()
    return processor.process_system(system, solver_func)

__all__ = ['isolate_cases_from_solver', 'generate_case_labeled_bounds']
''',

        'input_processor.py': '''"""
Legacy compatibility module for input_processor.py
"""

from rational_inequality_solver.processors.input_processor import InputProcessor as NewInputProcessor
from rational_inequality_solver.utils.validation import ValidationError

# Create global processor instance for compatibility
_processor = NewInputProcessor()

def process_inequalities(ineqs):
    """Legacy compatibility function."""
    return _processor.process_inequalities(ineqs)

def validate_processed_inequalities(processed_ineqs):
    """Legacy compatibility function."""
    return _processor.validate_processed_inequalities(processed_ineqs)

__all__ = ['process_inequalities', 'validate_processed_inequalities']
''',

        'latex_processor.py': '''"""
Legacy compatibility module for latex_processor.py
"""

from rational_inequality_solver.output.latex_formatter import LaTeXFormatter
from rational_inequality_solver.output.console_formatter import ConsoleFormatter

# Create global formatter instances
_latex_formatter = LaTeXFormatter()
_console_formatter = ConsoleFormatter()

def process_and_save_latex(results, base_filename, output_dir="output"):
    """Legacy compatibility function."""
    formatter = LaTeXFormatter(output_directory=output_dir)
    return formatter.format_and_save(results, base_filename)

def generate_summary_report(results, saved_files):
    """Legacy compatibility function."""
    return _latex_formatter.generate_summary_report(results, saved_files)

def clean_case_label(label):
    """Legacy compatibility function."""
    return _latex_formatter._clean_case_label(label)

def format_latex_expression(expr_str, max_line_length=80):
    """Legacy compatibility function."""
    return _latex_formatter._format_latex_expression(expr_str)

def create_latex_document(results, title="Rational Inequality Solutions"):
    """Legacy compatibility function."""
    return _latex_formatter._create_latex_document(results, title)

def clean_latex_result(result):
    """Legacy compatibility function."""
    return _latex_formatter._clean_latex_result(result)

__all__ = [
    'process_and_save_latex',
    'generate_summary_report', 
    'clean_case_label',
    'format_latex_expression',
    'create_latex_document',
    'clean_latex_result'
]
''',

        'sign_analyzer.py': '''"""
Legacy compatibility module for sign_analyzer.py
"""

from rational_inequality_solver.core.sign_analyzer import (
    OptimizedSignAnalyzer as SignAnalyzer,
    create_optimized_analyzer as create_default_analyzer,
    apply_sign_analysis_to_solver_output
)

# Legacy class aliases
class SignCombiner:
    """Legacy compatibility class."""
    
    @staticmethod
    def combine_addition(sign1, sign2):
        # Use the new analyzer's logic
        analyzer = create_default_analyzer()
        # This is a simplified version - the new architecture handles this internally
        if sign1 == 'positive' and sign2 == 'positive':
            return 'positive'
        elif sign1 == 'negative' and sign2 == 'negative':
            return 'negative'
        elif sign1 == 'zero' or sign2 == 'zero':
            return 'zero' if sign1 == sign2 else ('positive' if 'positive' in [sign1, sign2] else 'negative')
        else:
            return 'indeterminate'
    
    @staticmethod
    def combine_multiplication(sign1, sign2):
        if 'zero' in [sign1, sign2]:
            return 'zero'
        elif 'indeterminate' in [sign1, sign2]:
            return 'indeterminate'
        elif sign1 == sign2:
            return 'positive'
        else:
            return 'negative'

__all__ = ['SignAnalyzer', 'SignCombiner', 'create_default_analyzer', 'apply_sign_analysis_to_solver_output']
''',

        'examples.py': '''"""
Legacy compatibility module for examples.py
"""

from rational_inequality_solver.examples import (
    get_example as _get_example,
    list_examples,
    print_example_info,
    get_complex_example,
    get_simple_quadratic_example,
    get_rational_function_example,
    get_polynomial_example,
    get_mixed_parameters_example,
    get_all_examples
)

from rational_inequality_solver.core import SolverEngine
from rational_inequality_solver.processors.input_processor import InputProcessor
from rational_inequality_solver.processors.case_processor import CaseProcessor
from rational_inequality_solver.output.latex_formatter import LaTeXFormatter

def run_example(example_name):
    """Legacy compatibility function with same interface."""
    from sympy import symbols
    
    # Get example data in old format
    examples = get_all_examples()
    
    if example_name not in examples:
        print(f"Unknown example: {example_name}")
        print_example_info()
        return None
    
    x = symbols('x')
    ineqs = examples[example_name]
    
    print(f"Running example: {example_name}")
    print("=" * 50)
    
    try:
        # Use new architecture internally
        from input_processor import process_inequalities, validate_processed_inequalities
        from case_processor import generate_case_labeled_bounds
        from solver import solve_rational_ineq_full
        from latex_processor import process_and_save_latex
        
        processed_ineqs = process_inequalities(ineqs)
        validate_processed_inequalities(processed_ineqs)
        
        print(f"Processing {len(processed_ineqs)} inequalities...")
        
        results = generate_case_labeled_bounds(processed_ineqs, x, solve_rational_ineq_full)
        
        # Process and save LaTeX results
        try:
            saved_files = process_and_save_latex(results, f"example_{example_name}")
            print(f"\\nLaTeX files saved:")
            for file_type, filepath in saved_files.items():
                print(f"  {file_type.capitalize()}: {filepath}")
        except Exception as latex_error:
            print(f"LaTeX processing error: {latex_error}")
        
        # Print simplified results (maintain old format)
        print(f"\\nResults for {example_name}:")
        for i, result in enumerate(results):
            print(f"\\n--- Case {i+1} ---")
            if r'\\wedge' in result and r'\\min' in result:
                # Simplified display logic (same as original)
                parts = result.split(r'\\wedge')
                if len(parts) >= 2:
                    constraint = parts[0].replace(r'\\left\\{', '').replace(r'\\text{', '').replace('}', '').strip()
                    bounds = parts[1].split(r'\\right\\}')[0] if r'\\right\\}' in parts[1] else parts[1]
                    bounds = bounds.replace(r'\\min\\left(', 'min(').replace(r'\\max\\left(', 'max(')
                    
                    if constraint and constraint != '(no additional constraints)':
                        print(f"Constraint: {constraint}")
                    print(f"Bounds: {bounds[:100]}{'...' if len(bounds) > 100 else ''}")
                else:
                    print(result[:100] + "..." if len(result) > 100 else result)
            else:
                print(result[:100] + "..." if len(result) > 100 else result)
        
        return results
        
    except Exception as e:
        print(f"Error running example '{example_name}': {e}")
        return None

__all__ = [
    'get_complex_example',
    'get_simple_quadratic_example', 
    'get_rational_function_example',
    'get_polynomial_example',
    'get_mixed_parameters_example',
    'get_all_examples',
    'list_examples',
    'print_example_info',
    'run_example'
]
'''
    }
    
    return compatibility_modules


def backup_original_files():
    """Backup original files before migration."""
    backup_dir = Path("backup_original")
    backup_dir.mkdir(exist_ok=True)
    
    files_to_backup = [
        'main.py',
        'solver.py', 
        'case_processor.py',
        'input_processor.py',
        'latex_processor.py',
        'sign_analyzer.py',
        'examples.py'
    ]
    
    backed_up = []
    for filename in files_to_backup:
        source = Path(filename)
        if source.exists():
            destination = backup_dir / filename
            shutil.copy2(source, destination)
            backed_up.append(filename)
    
    return backed_up


def create_migration_report(backed_up_files: List[str]) -> str:
    """Create a migration report."""
    report = []
    report.append("MIGRATION REPORT")
    report.append("=" * 60)
    report.append("")
    
    report.append("WHAT WAS DONE:")
    report.append("-" * 30)
    report.append("1. Created new optimized package structure:")
    report.append("   rational_inequality_solver/")
    report.append("   ├── core/              # Core solver components")
    report.append("   ├── processors/        # Input and case processors")
    report.append("   ├── output/            # Output formatters")
    report.append("   ├── utils/             # Utility functions")
    report.append("   └── examples/          # Example library")
    report.append("")
    
    report.append("2. Backed up original files:")
    for filename in backed_up_files:
        report.append(f"   backup_original/{filename}")
    report.append("")
    
    report.append("3. Created compatibility layer for legacy imports")
    report.append("4. Added comprehensive test suite")
    report.append("5. Implemented configuration system")
    report.append("6. Added performance optimizations:")
    report.append("   - LRU caching for solver operations")
    report.append("   - Optimized sign analysis")
    report.append("   - Better input validation")
    report.append("   - Modular architecture")
    report.append("")
    
    report.append("BENEFITS OF NEW ARCHITECTURE:")
    report.append("-" * 40)
    report.append("• Better performance through caching and optimizations")
    report.append("• Improved error handling and validation")
    report.append("• Modular design for easier extension")
    report.append("• Comprehensive test coverage")
    report.append("• Configurable behavior")
    report.append("• Better code organization and maintainability")
    report.append("• Enhanced LaTeX and console output formatting")
    report.append("")
    
    report.append("HOW TO USE:")
    report.append("-" * 20)
    report.append("# New optimized API:")
    report.append("from rational_inequality_solver import solve_inequality_system")
    report.append("results = solve_inequality_system(inequalities)")
    report.append("")
    report.append("# Legacy compatibility (existing code should still work):")
    report.append("from solver import solve_rational_ineq_full")
    report.append("from examples import run_example")
    report.append("")
    report.append("# Run optimized main script:")
    report.append("python main_optimized.py")
    report.append("")
    report.append("# Run tests:")
    report.append("python tests/test_optimized_solver.py")
    report.append("")
    
    report.append("FILES TO EXPLORE:")
    report.append("-" * 25)
    report.append("• main_optimized.py - New main script with demonstrations")
    report.append("• tests/test_optimized_solver.py - Comprehensive test suite")
    report.append("• config/settings.py - Configuration system")
    report.append("• rational_inequality_solver/ - New package structure")
    
    return "\\n".join(report)


def perform_migration():
    """Perform the complete migration."""
    print("PERFORMING MIGRATION TO OPTIMIZED ARCHITECTURE")
    print("=" * 60)
    
    # Step 1: Backup original files
    print("Step 1: Backing up original files...")
    backed_up_files = backup_original_files()
    print(f"Backed up {len(backed_up_files)} files to backup_original/")
    
    # Step 2: Create compatibility layer
    print("\\nStep 2: Creating compatibility layer...")
    compatibility_modules = create_legacy_compatibility_layer()
    
    for filename, content in compatibility_modules.items():
        with open(filename, 'w') as f:
            f.write(content)
    
    print(f"Created {len(compatibility_modules)} compatibility modules")
    
    # Step 3: Update requirements if needed
    print("\\nStep 3: Checking requirements...")
    requirements_path = Path("requirements.txt")
    if requirements_path.exists():
        with open(requirements_path, 'r') as f:
            current_reqs = f.read()
        
        # Add any new requirements if needed
        if "dataclasses" not in current_reqs:
            with open(requirements_path, 'a') as f:
                f.write("\\n# Added for optimized architecture\\n")
                # dataclasses is built-in for Python 3.7+, but keeping for older versions
    
    # Step 4: Create default configuration
    print("\\nStep 4: Creating default configuration...")
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    default_config = {
        "solver": {
            "use_sign_analysis": True,
            "max_recursion_depth": 10,
            "simplification_level": 2,
            "cache_results": True
        },
        "output": {
            "output_directory": "output",
            "latex_enabled": True,
            "console_enabled": True,
            "save_raw_latex": True,
            "save_formatted_latex": True,
            "latex_line_length": 80,
            "console_line_length": 100
        },
        "processing": {
            "validate_inputs": True,
            "auto_convert_strings": True,
            "strict_operator_validation": True,
            "case_combination_limit": 1000
        }
    }
    
    import json
    with open(config_dir / "default_config.json", 'w') as f:
        json.dump(default_config, f, indent=2)
    
    # Step 5: Generate migration report
    print("\\nStep 5: Generating migration report...")
    report = create_migration_report(backed_up_files)
    
    with open("MIGRATION_REPORT.md", 'w') as f:
        f.write(report)
    
    print("\\nMIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 40)
    print("Please read MIGRATION_REPORT.md for details.")
    print("Your original files are backed up in backup_original/")
    print("\\nTo test the new architecture:")
    print("  python main_optimized.py")
    print("  python tests/test_optimized_solver.py")
    
    return True


if __name__ == "__main__":
    perform_migration()
