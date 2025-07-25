# Enhanced Variable Elimination Solver for Rational Inequalities

## Overview

This enhanced solver implements a sequential variable elimination approach for solving systems of rational inequalities. Unlike traditional approaches that solve for a single variable, this solver eliminates variables **x₁, x₂, ..., xₙ** one by one, creating a systematic reduction process that transforms complex multi-variable systems into simpler constraint systems.

## Key Features

### 🔄 Sequential Variable Elimination
- Eliminates variables in a specified order: x₁, then x₂, then x₃, etc.
- Each elimination step creates min/max expressions that are then expanded
- Preserves non-variable constraints throughout the process

### 📊 Four-Step Process for Each Variable
For each variable elimination, the solver shows:
1. **Original inequalities** involving the variable
2. **Min/Max expressions** after variable isolation  
3. **Min/Max expressions** after variable removal
4. **Final expanded inequalities** from min/max combinations

### 📄 Comprehensive Documentation
- Complete LaTeX reports with step-by-step derivations
- Text summaries for quick analysis
- Case-by-case breakdown of the elimination process

### ⚡ Advanced Features
- Sign analysis optimization from the base solver
- Support for rational, polynomial, and linear inequalities
- Robust error handling and input validation
- Modular architecture for easy extension

## Installation

The enhanced solver builds on the existing rational inequality solver. Ensure you have the base system installed:

```bash
# Install dependencies
pip install sympy

# The enhanced solver is ready to use
cd enhanced_solver
python demo.py  # Run demonstrations
```

## Quick Start

### Basic Usage

```python
from enhanced_solver import solve_with_elimination

# Define your system of inequalities
inequalities = [
    "x1**2 + x2 - 4 >= 0",    # Quadratic inequality
    "x1 + 2*x2 <= 1",         # Linear constraint  
    "x2 - x3 > 0",            # Variable relationship
    "a + b <= c"              # Parameter constraint (preserved)
]

# Specify variables to eliminate in order
variables = ['x1', 'x2', 'x3']

# Solve with full documentation
result = solve_with_elimination(inequalities, variables)

# Results include:
# - Step-by-step elimination process
# - Final inequality system
# - LaTeX report with full derivations
```

### Supported Input Formats

```python
# String format
"x**2 - 4 >= 0"

# Tuple format
("x + y", "<=", "1")
("2*x - y", ">=")  # Assumes RHS = 0

# Mixed formats in same system
inequalities = [
    "x1 + x2 >= 0",           # String
    ("x1 - x2", "<=", "1"),   # Tuple  
    ("y**2 - 4", ">=")        # Tuple with implicit 0
]
```

## How It Works

### The Elimination Process

Consider eliminating variable **x₁** from the system:
```
x₁² - 4 ≥ 0
x₁ + x₂ ≤ 1  
x₂ + a ≥ b
```

**Step 1: Isolate x₁**
- From x₁² - 4 ≥ 0: x₁ ≤ -2 or x₁ ≥ 2
- From x₁ + x₂ ≤ 1: x₁ ≤ 1 - x₂

**Step 2: Create Min/Max**
- Upper bounds: min(1 - x₂, -2, +∞) 
- Lower bounds: max(2, -∞)

**Step 3: Remove Variable**  
- Upper: min(1 - x₂, -2)
- Lower: 2

**Step 4: Expand Combinations**
- 2 ≤ min(1 - x₂, -2)
- Expands to: 2 ≤ 1 - x₂ AND 2 ≤ -2
- Plus preserved constraint: x₂ + a ≥ b

### Why This Approach?

**Advantages:**
- ✅ Systematically reduces problem dimensionality
- ✅ Handles complex rational inequalities robustly
- ✅ Preserves all constraint relationships
- ✅ Provides complete mathematical documentation
- ✅ Useful for optimization and feasibility analysis

**Trade-offs:**
- ⚠️ Can generate many inequalities (combinatorial explosion)
- ⚠️ Computational complexity grows with system size
- ⚠️ May create redundant constraints that need simplification

## Examples

### Example 1: Linear System
```python
inequalities = [
    "x1 + x2 >= 0",
    "x1 - x2 <= 1", 
    "2*x1 + x2 >= -1"
]
variables = ['x1', 'x2']

result = solve_with_elimination(inequalities, variables)
# Result: Simplified constraint system without x1, x2
```

### Example 2: Mixed System with Parameters
```python
inequalities = [
    "x**2 - 4 >= 0",      # Quadratic in x
    "x + y <= a",         # Linear with parameter
    "y >= b",             # Parameter bound
    "c + d <= e"          # Pure parameter constraint
]
variables = ['x', 'y']

result = solve_with_elimination(inequalities, variables)
# Result: Constraints only involving a, b, c, d, e
```

### Example 3: Rational Inequalities
```python
inequalities = [
    "(x + 1)/(x - 1) >= 0",
    "x + y <= 3",
    "y**2 - 4 <= 0"
]
variables = ['x', 'y']

result = solve_with_elimination(inequalities, variables)
# Result: Handles rational inequality cases automatically
```

## Output Structure

### Result Dictionary
```python
{
    'steps': [
        {
            'step_number': 0,
            'description': 'Initial Inequality System',
            'input_inequalities': [...],
            'variable_eliminated': None,
            # ...
        },
        {
            'step_number': 1,
            'description': 'Eliminate Variable x1',
            'variable_eliminated': 'x1',
            'input_inequalities': [...],
            'min_max_expressions': {...},
            'eliminated_expressions': {...},
            'output_inequalities': [...]
        },
        # ... more steps
    ],
    'final_inequalities': [...],
    'total_steps': 3
}
```

### LaTeX Report
Automatically generated comprehensive report with:
- Complete mathematical derivations
- Step-by-step variable elimination
- Min/max expression development  
- Final constraint system
- Professional mathematical formatting
- **Saved to both `output/` and `output_final/` folders**

### Text Summary
Human-readable summary including:
- System progression through each step
- Bound counting and analysis
- Final inequality enumeration
- Performance metrics

## Advanced Usage

### Custom Configuration
```python
# Disable sign analysis for debugging
result = solve_with_elimination(
    inequalities, variables,
    use_sign_analysis=False
)

# Custom output filename
result = solve_with_elimination(
    inequalities, variables,
    output_filename="my_analysis_2024"
)

# Skip LaTeX generation for speed
result = solve_with_elimination(
    inequalities, variables,
    save_latex=False
)
```

### Programmatic Access
```python
from enhanced_solver.core import VariableEliminationSolver

# Direct solver access
solver = VariableEliminationSolver(use_sign_analysis=True)
result = solver.solve_with_variable_elimination(inequalities, variables)

# Generate custom LaTeX
latex_content = solver.generate_latex_report()
```

## Testing

Run the comprehensive test suite:

```bash
cd enhanced_solver
python tests/test_enhanced_solver.py
```

Run demonstrations:

```bash
python demo.py
```

## File Structure

```
enhanced_solver/
├── __init__.py                    # Package interface
├── enhanced_solver.py             # Main solving interface  
├── demo.py                       # Demonstration examples
├── simple_example.py             # Clear 4-step breakdown
├── main.py                       # Integration script
├── core/
│   ├── __init__.py
│   └── variable_eliminator.py    # Core elimination logic
├── tests/
│   └── test_enhanced_solver.py   # Comprehensive tests
├── output/                       # Standard output folder
│   ├── *.tex                     # LaTeX documents
│   └── *_summary.txt             # Text summaries
└── output_final/                 # Complete LaTeX reports
    └── *_complete.tex            # Full step-by-step documentation
```

## Performance Considerations

- **Linear systems**: Generally produce fewer final inequalities
- **Quadratic systems**: Can generate many constraints due to case analysis  
- **Rational systems**: Complex case splitting, but handled robustly
- **Large systems**: Computational time grows significantly with variables

**Optimization tips:**
- Enable sign analysis for better performance
- Eliminate variables in order of increasing complexity
- Consider partial elimination for very large systems

## Integration with Base Solver

The enhanced solver builds on and integrates seamlessly with the existing rational inequality solver:

- Uses the same `solve_rational_ineq_full` function for individual variable isolation
- Inherits sign analysis optimization capabilities
- Compatible with existing input processing and case handling
- Extends LaTeX formatting for multi-step documentation

## Contributing

To extend the enhanced solver:

1. **New elimination strategies**: Modify `_expand_minmax_combinations`
2. **Output formats**: Extend LaTeX generation methods
3. **Optimization**: Add caching or parallel processing
4. **Integration**: Connect with optimization solvers

## Dependencies

- **SymPy**: Symbolic mathematics and expression handling
- **Base solver**: Existing rational inequality solver modules
- **Python 3.7+**: Core language features

## License

This enhanced solver extends the existing rational inequality solver and is provided for educational and research purposes.

---

**Note**: This enhanced solver transforms inequality systems by eliminating variables sequentially. While powerful for systematic analysis, users should be aware that the number of resulting inequalities can grow significantly with system complexity. The approach is particularly valuable for parameter analysis, constraint simplification, and multi-stage optimization problems.
