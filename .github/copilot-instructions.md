# Rational Inequality Solver - AI Coding Agent Instructions

## Project Overview
This is a **dual-approach symbolic mathematics system** for solving rational inequalities using SymPy. The architecture provides two complementary solving strategies:

1. **Traditional Solver** (`solver.py`): Analyzes single variables with comprehensive case-by-case breakdown
2. **Variable Elimination Engine** (`main.py`): Sequential multi-variable elimination using a **simplified 4-step hierarchical process**

## Core Principle
**KEY INSIGHT**: The system recently underwent major simplification. Everything is now treated as **inequalities within cases** - no artificial separation between "constraints" and "inequalities". The principle: *"At the end, we can just say all the inequalities in one of the cases needs to be true."*

## Essential Architecture

### 4-Step Variable Elimination Process (Primary Engine)
The `HierarchicalCaseEliminator` in `main.py` implements the core algorithm:

1. **ISOLATE VARIABLE**: Transform inequalities to `x ≥ expr` or `x ≤ expr` using `solve_rational_ineq_full()`
2. **COMBINE TO MIN/MAX**: Collect bounds into `max(lower_bounds) ≤ variable ≤ min(upper_bounds)`  
3. **REMOVE VARIABLE**: Create elimination constraints `max(lower) ≤ min(upper)`
4. **EXPAND CASES**: Generate hierarchical subcases for min/max combinations

### Input Processing Pipeline
```python
# Standard input format: List of (lhs, op, rhs) tuples
inequalities = [("x1 + x2", "<=", "a"), ("x1", ">=", "b")]
variables_to_eliminate = ['x1', 'x2']

# Entry point
eliminator = HierarchicalCaseEliminator()
final_cases = eliminator.eliminate_variables_hierarchical(inequalities, variables_to_eliminate)
```

### Case Hierarchy System
- **HierarchicalCase**: Tracks inequalities, elimination steps, and hierarchical path
- **CaseNamingSystem**: Manages naming (Case 1 → Subcase 1.1 → Subsubcase 1.1.1)
- **HierarchicalLatexGenerator**: Creates comprehensive LaTeX documentation

## Critical Development Patterns

### Unified Terminology
**Always use "inequality" terminology**, never "constraint":
- `_filter_inequalities()` not `_filter_constraints()`
- `case.inequalities` not `case.constraints` 
- Method names should reflect this unified approach

### Error Handling Strategy
```python
# Pattern: Always provide intelligent fallbacks
try:
    bounds = self._solve_inequality_for_variable(expr, op, rhs, variable)
except Exception as e:
    print(f"Error solving: {e}")
    # Intelligent fallback based on operator
    if op in ['>=', '>']:
        return [('lower', 0, op)]
    else:
        return [('upper', 0, op)]
```

### LaTeX Generation Pattern
All LaTeX output follows this structure:
- **Overview**: Explains the simplified approach (no constraint/inequality separation)
- **4-Step Documentation**: Complete process for each variable
- **Hierarchical Cases**: Shows path from root to final cases
- **Final Summary**: All inequalities in parameter space only

## Key Integration Points

### Solver Engine Integration
The variable eliminator calls `solve_rational_ineq_full()` from `solver.py`:
```python
case_outputs = solve_rational_ineq_full(ineq_expr, var_symbol, op, self.use_sign_analysis)
bounds = self._extract_bounds_from_single_case(case_output, variable, op, case_num)
```

### Input Validation Chain
1. `input_processor.process_inequalities()` - Standardizes input formats
2. `HierarchicalCaseEliminator._filter_inequalities()` - Validates and filters
3. Sign analysis via `sign_analyzer.py` (optional optimization)

### Output Generation
- **Terminal**: Detailed step-by-step elimination process with debugging info
- **LaTeX**: Professional mathematical documentation in `output_final/`
- **File naming**: `simplified_elimination_YYYYMMDD_HHMMSS.tex`

## Critical Files and Their Roles

### Core Engine Files
- `main.py`: Primary elimination engine with `HierarchicalCaseEliminator`
- `solver.py`: Symbolic inequality solver using case-based analysis
- `input_processor.py`: Input validation and standardization
- `latex_processor.py`: Professional LaTeX document generation

### Support Systems  
- `sign_analyzer.py`: Optional performance optimization for impossible case elimination
- `config/settings.py`: Configuration management for solver behavior
- `SIMPLIFICATION_SUMMARY.md`: Documents the recent constraint/inequality unification

## Testing and Debugging

### Running the System
```bash
python main.py  # Runs comprehensive test suite with 3 complex examples
```

### Key Test Cases
1. **Simple Linear**: 2 variables, basic bounds
2. **Three Variable**: Complex multi-variable with hierarchical cases
3. **Mixed Bounds**: Multiple lower/upper bounds requiring case expansion

### Debug Output Interpretation
- **Step-by-step elimination**: Shows 4-step process for each variable
- **Case generation**: Tracks hierarchical subcase creation
- **Bound extraction**: Shows how solver results become variable bounds
- **Impossible case detection**: Filters contradictory inequalities

## Development Guidelines

### When Adding New Features
1. **Maintain the 4-step structure** - all variable elimination should follow this pattern
2. **Use inequality terminology consistently** - avoid "constraint" language
3. **Preserve hierarchical case tracking** - ensure proper naming and path tracking
4. **Add LaTeX documentation** - all new features need mathematical documentation

### Common Pitfalls
- **Don't mix constraint/inequality terminology** - system was recently unified
- **Don't bypass the 4-step process** - it ensures mathematical completeness
- **Don't ignore case hierarchy** - proper naming is crucial for output clarity
- **Don't skip input validation** - malformed inputs can cascade through the system

### Performance Considerations
- **Sign analysis**: Use `use_sign_analysis=True` to eliminate impossible cases early
- **Case explosion**: Monitor hierarchical case counts - exponential growth possible
- **SymPy overhead**: Complex symbolic operations can be expensive

## Integration with External Tools
- **SymPy dependency**: Version ≥1.12 required for symbolic mathematics
- **LaTeX compilation**: Generated `.tex` files compile with standard LaTeX distributions
- **File I/O**: All outputs go to `output_final/` directory with timestamped names

This system represents a sophisticated mathematical engine where understanding the 4-step elimination process and unified inequality treatment is essential for effective development.
