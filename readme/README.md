# Rational Inequality Solver

A modular Python package for solving rational inequalities symbolically with LaTeX output formatting.

## Features

- Solve rational inequalities with symbolic parameters
- Handle linear, quadratic, and higher-order polynomials
- Generate case-based solutions with LaTeX formatting
- Modular architecture for easy extension
- Multiple input formats supported
- Comprehensive error handling and validation

## Project Structure

```
├── solver.py           # Core solving logic
├── case_processor.py   # Case processing and LaTeX formatting
├── input_processor.py  # Input parsing and validation
├── main.py            # Main execution script
├── examples.py        # Example configurations and test cases
├── script.py          # Legacy compatibility module
└── requirements.txt   # Dependencies
```

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Running the Main Example

```python
python main.py
```

### Running Specific Examples

```python
from examples import run_example, print_example_info

# See available examples
print_example_info()

# Run a specific example
run_example('quadratic')
```

### Custom Usage

```python
from sympy import symbols
from solver import solve_rational_ineq_full
from case_processor import generate_case_labeled_bounds
from input_processor import process_inequalities

# Define symbols and inequalities
x, a, b = symbols('x a b')
ineqs = [
    (x**2 - 4, ">=", 0),
    (a*x + b, ">", 0)
]

# Process and solve
processed = process_inequalities(ineqs)
results = generate_case_labeled_bounds(processed, x, solve_rational_ineq_full)

# Print results
for i, result in enumerate(results):
    print(f"Case {i+1}: {result}")
```

## Input Formats

The solver accepts inequalities in multiple formats:

1. **Tuple format**: `(expression, operator, rhs)`
   ```python
   (x**2 - 4, ">=", 0)
   ```

2. **Expression-operator format**: `(expression, operator)`
   ```python
   (x**2 - 4, ">=")  # Assumes RHS = 0
   ```

3. **String format**: `"lhs operator rhs"`
   ```python
   "x**2 - 4 >= 0"
   ```

## Supported Operators

- `<=`, `<`: Less than (or equal)
- `>=`, `>`: Greater than (or equal)
- `==`: Equal
- `!=`: Not equal

## Module Descriptions

### `solver.py`
Contains the core rational inequality solving logic:
- Handles rational expressions by analyzing numerator and denominator separately
- Supports linear and quadratic polynomials with symbolic parameters
- Generates detailed case analysis for all solution branches

### `case_processor.py`
Processes solver output and generates formatted results:
- Extracts bound information from solver output
- Combines multiple inequality cases using Cartesian products
- Formats output as LaTeX for mathematical presentation

### `input_processor.py`
Handles input parsing and validation:
- Supports multiple inequality input formats
- Converts strings to SymPy expressions
- Validates operator syntax and expression structure

### `examples.py`
Contains predefined test cases and examples:
- Complex rational inequalities with multiple parameters
- Simple polynomial inequalities
- Mixed parameter systems
- Utilities for running and comparing examples

## Error Handling

The solver includes comprehensive error handling:
- Input format validation
- Expression parsing error recovery
- Operator validation
- Symbolic computation error handling

## LaTeX Output

Results are formatted as LaTeX expressions suitable for mathematical documents:

```latex
\textbf{Case 1: ...}\\[1em]
\left\{ \text{constraints} \wedge \max(...) < x < \min(...) \right\}\\[1em]
\left\{ \text{constraints} \wedge \max(...) \le x \le \min(...) \right\}
```

## Contributing

1. Follow the existing modular structure
2. Add comprehensive docstrings
3. Include error handling
4. Add examples for new features
5. Update this README for significant changes

## Dependencies

- SymPy: Symbolic mathematics library
- Python 3.7+: Core language features

## License

This project is provided as-is for educational and research purposes.
