# Hierarchical Variable Elimination System

## Overview

This system implements a complete hierarchical variable elimination process for systems of linear inequalities. The key features include:

1. **Hierarchical Case Management**: Cases are organized with descriptive naming (Case 1, Subcase 1.1, Subsubcase 1.1.2, etc.)
2. **4-Step Elimination Process**: Each variable is eliminated using a rigorous 4-step process
3. **Individual Subcase Solving**: Each subcase is solved individually and documented
4. **Complete LaTeX Documentation**: Full mathematical documentation with proper case hierarchy

## 4-Step Variable Elimination Process

For each variable to be eliminated, the system follows these steps:

### Step 1: Isolate Variable
- Identify all inequalities containing the target variable
- Solve each inequality to isolate the variable on one side
- Separate into lower bounds (variable ≥ expression) and upper bounds (variable ≤ expression)

### Step 2: Combine to Min/Max Form
- Combine multiple lower bounds: `variable ≥ max(lower_bounds)`
- Combine multiple upper bounds: `variable ≤ min(upper_bounds)`
- Form: `max(lower_bounds) ≤ variable ≤ min(upper_bounds)`

### Step 3: Remove Variable
- Create elimination constraints of the form: `max(lower_bounds) ≤ min(upper_bounds)`
- These constraints must be satisfied for the system to have a solution

### Step 4: Expand Cases
- For each min/max combination, create individual inequalities
- Generate hierarchical subcases for each combination
- Handle tightness cases when multiple bounds exist

## Hierarchical Case Structure

### Case Naming System
- **Case 1, Case 2, ...**: Top-level cases (root level)
- **Subcase 1.1, Subcase 1.2, ...**: First-level subcases
- **Subsubcase 1.1.1, Subsubcase 1.1.2, ...**: Second-level subcases
- **SubSubSubcase 1.1.1.1, ...**: Third-level subcases (and so on)

### Case Management
Each case in the hierarchy contains:
- **Name**: Descriptive hierarchical name
- **Case ID**: Unique identifier for tracking
- **Inequalities**: Set of constraints for this case
- **Parent**: Reference to parent case
- **Level**: Depth in the hierarchy
- **Subcases**: List of child cases
- **Elimination Steps**: Record of variable elimination steps
- **Solution Status**: Whether the case has been solved

## Implementation Components

### Core Classes

#### `CaseNamingSystem`
Manages the hierarchical naming convention:
- Tracks case counters at each level
- Generates descriptive case names
- Maintains parent-child relationships

#### `HierarchicalCase`
Represents individual cases in the hierarchy:
- Stores case information and constraints
- Manages subcases and elimination steps
- Handles individual case solving

#### `HierarchicalCaseEliminator`
Main elimination engine:
- Implements the 4-step elimination process
- Manages case hierarchy during elimination
- Coordinates the overall elimination process

#### `HierarchicalLatexGenerator`
Generates comprehensive LaTeX documentation:
- Creates hierarchical document structure
- Documents each elimination step
- Formats mathematical expressions properly

### Key Methods

#### `eliminate_variables_hierarchical()`
Main elimination function that:
1. Initializes the root case with all inequalities
2. For each variable to eliminate:
   - Processes each current case
   - Applies 4-step elimination
   - Generates subcases
   - Solves each subcase individually
3. Returns final solution cases

#### `eliminate_variable_4_step_hierarchical()`
Implements the complete 4-step process for a single case:
1. Isolate the variable in relevant inequalities
2. Combine to max/min form
3. Remove the variable
4. Expand into hierarchical subcases

## Input Format

The system accepts inequalities in the following formats:

### Variables
- Must be named with pattern: `x1`, `x2`, `x3`, `x4`, ...
- Variables are eliminated in the order specified

### Constants
- Can be named with any valid symbols: `a`, `b`, `c`, `d`, `e`, ...
- Support arbitrary parameter names

### Inequality Strings
Examples:
```
"x1 + 2*x2 + a >= b"
"x1 - x2 + c >= 0"
"2*x1 + d <= x2 + e"
"x2 <= f"
"g*x3 + x1 >= h"
```

## Output Format

### Console Output
- Step-by-step elimination process
- Case generation with hierarchical naming
- Final solution summary
- Case analysis with statistics

### LaTeX Documentation
Complete mathematical document including:
- Introduction and methodology
- Original system presentation
- Detailed elimination steps for each case
- Hierarchical case documentation
- Final solution summary

### Generated Files
Files are saved in `output_final/` directory:
- `hierarchical_main_TIMESTAMP_complete.tex`: Complete LaTeX document
- Timestamp format: `YYYYMMDD_HHMMSS`

## Example Usage

### Basic Usage
```python
from main import demonstrate_enhanced_variable_elimination

# Use default example system
demonstrate_enhanced_variable_elimination()
```

### Custom System
```python
# Define custom inequalities
inequalities = [
    "x1 + x2 >= a",
    "x1 - x2 <= b",
    "2*x1 + c >= d",
    "x2 + e <= f"
]

# Specify elimination order
variables_to_eliminate = ["x1", "x2"]

# Run elimination
demonstrate_enhanced_variable_elimination(
    inequalities=inequalities,
    variables_to_eliminate=variables_to_eliminate
)
```

## Mathematical Properties

### Correctness
- Each elimination step preserves solution equivalence
- Case expansion ensures complete coverage of solution space
- Hierarchical structure maintains logical relationships

### Completeness
- All possible cases are generated through systematic expansion
- No solution cases are lost during elimination
- Final constraints represent complete solution characterization

### Efficiency
- Hierarchical organization reduces redundant computation
- Individual case solving optimizes memory usage
- Structured documentation enables easy verification

## Error Handling

The system includes robust error handling for:
- Malformed inequality expressions
- Invalid variable names
- Unsolvable constraint systems
- Complex coefficient scenarios
- File I/O operations

## Dependencies

Required Python packages:
- `sympy`: Symbolic mathematics and expression manipulation
- `datetime`: Timestamp generation for output files
- `os`: File system operations
- `collections.defaultdict`: Hierarchical counter management

## Testing

The system includes comprehensive testing:
- Unit tests for individual components
- Integration tests for complete elimination
- Custom system validation
- Multi-variable system testing

See `test_hierarchical.py` for example test cases.
