# Unified Rational Inequality Solver

A comprehensive solver for rational inequalities with both traditional solving and advanced variable elimination capabilities.

## Features

### Original Solver
- Solves rational inequalities for a single variable
- Generates min/max expressions with case analysis
- Produces detailed LaTeX documentation
- Handles complex multi-parameter systems

### Variable Elimination (NEW)
- Sequential elimination of multiple variables
- 4-step process for each elimination:
  1. Original inequalities
  2. Min/max expressions with variable
  3. Min/max expressions without variable  
  4. Final split inequalities
- Complete LaTeX documentation with step-by-step process
- Preserves parameter constraints

## Quick Start

### Basic Usage

```python
# Original solver (single variable analysis)
from solver import solve_rational_ineq_full
from case_processor import generate_case_labeled_bounds

# Variable elimination (multi-variable systems)
from variable_eliminator import solve_with_variable_elimination

# Eliminate variables x1, x2, x3 from a system
result = solve_with_variable_elimination(
    inequalities=["x1 + x2 >= 0", "x2 - x3 <= 1"],
    variables_to_eliminate=['x1', 'x2', 'x3']
)
```

### Unified Demonstration

```bash
python unified_main.py
```

This runs both the original solver and variable elimination on example systems, showing the capabilities of each approach.

## File Structure

### Core Components
- `solver.py` - Original rational inequality solver
- `case_processor.py` - Case analysis and bound generation
- `input_processor.py` - Input validation and processing
- `latex_processor.py` - LaTeX output generation
- `variable_eliminator.py` - **NEW** Variable elimination solver
- `unified_main.py` - **NEW** Unified demonstration script

### Examples and Demos
- `main.py` - Original solver examples
- `examples.py` - Test case definitions
- `demo_optimized.py` - Optimized solver demonstration

### Configuration and Utilities
- `config/settings.py` - Configuration settings
- `sign_analyzer.py` - Sign analysis utilities
- `requirements.txt` - Python dependencies

### Output Directories
- `output/` - Original solver LaTeX and summaries
- `output_final/` - **NEW** Complete variable elimination documentation

## Key Improvements

### Unified Architecture
- Eliminated redundancy between enhanced_solver and main codebase
- Single integrated system with complementary approaches
- Clear separation of concerns between solving strategies

### Enhanced Documentation
- Complete LaTeX generation for both approaches
- Step-by-step elimination process documentation
- Professional mathematical formatting

### Comprehensive Testing
- Original solver test cases preserved
- Variable elimination test coverage
- Unified demonstration examples

## Usage Examples

### Example 1: Original Solver
```python
from main import main
main()  # Runs original solver on complex examples
```

### Example 2: Variable Elimination
```python
from variable_eliminator import solve_with_variable_elimination

# Multi-variable system
inequalities = [
    "x1**2 + x2 - 4 >= 0",
    "x1 + 2*x2 + x3 >= 1", 
    "x2 - x3 <= 2"
]

result = solve_with_variable_elimination(
    inequalities=inequalities,
    variables_to_eliminate=['x1', 'x2', 'x3'],
    save_latex=True
)
```

### Example 3: Comparison
```python
from unified_main import main
main()  # Shows both approaches on test systems
```

## Dependencies

```
sympy>=1.12
itertools (built-in)
datetime (built-in)
os (built-in)
```

Install with:
```bash
pip install -r requirements.txt
```

## When to Use Each Approach

### Original Solver
- When you need min/max expressions for a single variable
- For analysis of solution structure in terms of parameters
- When working with complex rational expressions

### Variable Elimination  
- When you want to systematically remove multiple variables
- For dimensional reduction of constraint systems
- When you need complete step-by-step elimination documentation
- For optimization problems requiring constraint simplification

## Output Files

### Original Solver Output
- `output/main_example_solutions.tex` - Complete LaTeX solutions
- `output/main_example_solutions_simple.txt` - Text summaries
- `output/main_example_solutions_raw.txt` - Raw solver output

### Variable Elimination Output
- `output_final/variable_elimination_TIMESTAMP.tex` - Complete elimination steps
- `output_final/variable_elimination_TIMESTAMP_summary.txt` - Process summary

## Advanced Features

- **Sign Analysis**: Automatic sign determination for expressions
- **Case Generation**: Comprehensive case analysis for all scenarios  
- **LaTeX Integration**: Professional mathematical documentation
- **Parameter Preservation**: Maintains non-target variable constraints
- **Error Handling**: Robust validation and error reporting

## Architecture Benefits

1. **Unified Codebase**: Single repository with complementary solving approaches
2. **Code Reuse**: Shared utilities between original and elimination solvers
3. **Clear Interfaces**: Well-defined APIs for both solving strategies
4. **Comprehensive Testing**: Full coverage of both approaches
5. **Professional Output**: LaTeX documentation for all results

This unified solver provides both traditional rational inequality solving and advanced multi-variable elimination in a single, well-integrated system.
