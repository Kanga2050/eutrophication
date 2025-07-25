"""
LaTeX processor module for formatting and saving mathematical expressions.
Handles LaTeX output generation, formatting, and file writing.
"""
import os
import re
from datetime import datetime
from sympy.printing.latex import latex


def clean_case_label(label):
    """
    Clean up verbose case labels to make them more concise.
    
    Args:
        label: Original case label string
        
    Returns:
        Cleaned, concise label
    """
    # Extract just the case number and basic description
    if "Case" in label:
        # Extract case number
        case_match = re.search(r'Case (\d+)', label)
        if case_match:
            case_num = case_match.group(1)
            
            # Determine if it's about numerator or denominator conditions
            if "because" in label:
                if ">= 0" in label or "> 0" in label:
                    condition = "positive"
                elif "<= 0" in label or "< 0" in label:
                    condition = "negative"
                else:
                    condition = "constrained"
                    
                return f"Case {case_num}: {condition}"
            else:
                return f"Case {case_num}"
    
    return label


def format_latex_expression(expr_str, max_line_length=80):
    """
    Format long LaTeX expressions with proper line breaks.
    
    Args:
        expr_str: LaTeX expression string
        max_line_length: Maximum characters per line
        
    Returns:
        Formatted LaTeX string with line breaks
    """
    if len(expr_str) <= max_line_length:
        return expr_str
    
    # Find good break points (after commas, operators, etc.)
    break_points = ['+', '-', ',', r'\wedge', r'\min', r'\max']
    
    formatted_lines = []
    current_line = ""
    
    # Split on natural break points
    parts = re.split(r'(\+|\-|,|\\wedge|\\min|\\max)', expr_str)
    
    for i, part in enumerate(parts):
        if len(current_line + part) <= max_line_length:
            current_line += part
        else:
            if current_line:
                formatted_lines.append(current_line.strip())
            current_line = part
    
    if current_line:
        formatted_lines.append(current_line.strip())
    
    # Join with proper LaTeX line breaks
    return " \\\\\n    & ".join(formatted_lines)


def create_latex_document(results, title="Rational Inequality Solutions"):
    """
    Create a complete LaTeX document from results.
    
    Args:
        results: List of LaTeX formatted result strings
        title: Document title
        
    Returns:
        Complete LaTeX document string
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Document header
    latex_doc = r"""\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{geometry}
\geometry{margin=1in}

\title{""" + title + r"""}
\author{Rational Inequality Solver}
\date{Generated on """ + timestamp + r"""}

\begin{document}
\maketitle

\section{Solution Cases}

"""
    
    # Process each result
    for i, result in enumerate(results):
        latex_doc += f"\\subsection{{Case {i+1}}}\n\n"
        
        # Clean up the result formatting
        cleaned_result = clean_latex_result(result)
        
        latex_doc += "\\begin{align}\n"
        latex_doc += cleaned_result
        latex_doc += "\n\\end{align}\n\n"
    
    # Document footer
    latex_doc += r"""
\section{Notes}

These solutions represent the case-wise analysis of the given rational inequality system. Each case corresponds to different sign combinations of the numerator and denominator expressions.

\end{document}
"""
    
    return latex_doc


def clean_latex_result(result):
    """
    Clean and format a single LaTeX result for better readability.
    
    Args:
        result: Raw LaTeX result string
        
    Returns:
        Cleaned LaTeX string
    """
    # Extract the main components
    parts = result.split(r'\\[1em]')
    
    if len(parts) < 3:
        return result
    
    # Clean case header
    case_header = parts[0]
    case_header = re.sub(r'\\textbf\{([^}]+)\}', r'\\text{\1}', case_header)
    
    # Simplify long case descriptions
    if len(case_header) > 100:
        # Extract case numbers and simplify
        case_matches = re.findall(r'Case \d+', case_header)
        if case_matches:
            simplified_header = f"\\text{{{', '.join(case_matches)}}}"
        else:
            simplified_header = r"\text{Combined Cases}"
    else:
        simplified_header = case_header
    
    # Format the bounds
    strict_bounds = parts[1] if len(parts) > 1 else ""
    non_strict_bounds = parts[2] if len(parts) > 2 else ""
    
    # Clean up bound expressions
    strict_bounds = clean_bound_expression(strict_bounds)
    non_strict_bounds = clean_bound_expression(non_strict_bounds)
    
    # Combine with proper formatting
    cleaned = f"{simplified_header} \\\\\n"
    cleaned += f"& {strict_bounds} \\\\\n"
    cleaned += f"& {non_strict_bounds}"
    
    return cleaned


def clean_bound_expression(bound_expr):
    """
    Clean and format bound expressions for better readability.
    
    Args:
        bound_expr: Bound expression string
        
    Returns:
        Cleaned bound expression
    """
    if not bound_expr:
        return ""
    
    # Remove redundant braces and simplify
    bound_expr = re.sub(r'\\left\\{([^}]+)\\right\\}', r'\{\1\}', bound_expr)
    
    # Break long expressions
    if len(bound_expr) > 120:
        # Find the main components (constraint and bound)
        wedge_split = bound_expr.split(r'\wedge')
        if len(wedge_split) == 2:
            constraint = wedge_split[0].strip().rstrip('{').strip()
            bound = wedge_split[1].strip().rstrip('}').strip()
            
            # Format constraint
            if constraint and constraint != r'\text{(no additional constraints)}':
                constraint_formatted = constraint.replace('{', '').replace('}', '')
            else:
                constraint_formatted = ""
            
            # Format bound with line breaks if needed
            if len(bound) > 80:
                bound_formatted = format_latex_expression(bound, 60)
            else:
                bound_formatted = bound
            
            if constraint_formatted:
                return f"\\{{{constraint_formatted} \\wedge {bound_formatted}\\}}"
            else:
                return f"\\{{{bound_formatted}\\}}"
    
    return bound_expr


def save_latex_to_file(latex_content, filename="inequality_solutions.tex", output_dir="output"):
    """
    Save LaTeX content to a file.
    
    Args:
        latex_content: LaTeX content string
        filename: Output filename
        output_dir: Output directory
        
    Returns:
        Full path to saved file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Full file path
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        return filepath
    except Exception as e:
        raise IOError(f"Failed to save LaTeX file: {e}")


def save_plain_latex_results(results, filename="latex_results.txt", output_dir="output"):
    """
    Save clean, copy-pasteable LaTeX results to a plain text file.
    
    Args:
        results: List of LaTeX result strings
        filename: Output filename
        output_dir: Output directory
        
    Returns:
        Full path to saved file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Full file path
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            # Write clean LaTeX that can be copy-pasted
            f.write("% Rational Inequality Solver Results\n")
            f.write(f"% Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("% Copy-paste ready LaTeX\n\n")
            
            # Add minimal document wrapper for standalone rendering
            f.write("\\documentclass{article}\n")
            f.write("\\usepackage{amsmath}\n")
            f.write("\\usepackage{amssymb}\n")
            f.write("\\begin{document}\n\n")
            
            for i, result in enumerate(results):
                f.write(f"% Case {i+1}\n")
                
                # Clean up the result for proper LaTeX
                cleaned_result = _clean_for_copy_paste(result)
                
                f.write("\\begin{align}\n")
                f.write(f"\\text{{Case {i+1}:}} \\quad\n")
                f.write(cleaned_result)
                f.write("\n\\end{align}\n\n")
                f.write("\\vspace{1em}\n\n")
            
            f.write("\\end{document}\n")
        
        return filepath
    except Exception as e:
        raise IOError(f"Failed to save LaTeX results file: {e}")


def _clean_for_copy_paste(latex_result):
    """
    Clean LaTeX result for proper copy-paste rendering.
    
    Args:
        latex_result: Raw LaTeX result string
        
    Returns:
        Clean LaTeX string ready for rendering
    """
    # Split the result into components
    parts = latex_result.split(r'\\[1em]')
    
    if len(parts) < 3:
        return latex_result
    
    # Extract and clean case header
    case_header = parts[0]
    case_header = re.sub(r'\\textbf\{([^}]+)\}', r'', case_header)  # Remove textbf
    case_header = re.sub(r'Case \d+: [^:]*:', '', case_header)  # Remove verbose descriptions
    
    # Extract the two bound expressions
    strict_bounds = parts[1] if len(parts) > 1 else ""
    inclusive_bounds = parts[2] if len(parts) > 2 else ""
    
    # Clean each bound expression
    strict_clean = _clean_bound_for_copy_paste(strict_bounds, strict=True)
    inclusive_clean = _clean_bound_for_copy_paste(inclusive_bounds, strict=False)
    
    # Format as clean mathematical expressions
    result_lines = []
    
    if strict_clean:
        result_lines.append(f"& {strict_clean} \\\\")
    
    if inclusive_clean:
        result_lines.append(f"& {inclusive_clean}")
    
    return "\n".join(result_lines)


def _clean_bound_for_copy_paste(bound_expr, strict=True):
    """
    Clean a single bound expression for copy-paste.
    
    Args:
        bound_expr: Bound expression string
        strict: Whether this is strict inequality (< or >) vs inclusive (≤ or ≥)
        
    Returns:
        Clean bound expression
    """
    if not bound_expr:
        return ""
    
    # Remove LaTeX formatting cruft
    bound_expr = re.sub(r'\\left\\{', r'\{', bound_expr)
    bound_expr = re.sub(r'\\right\\}', r'\}', bound_expr)
    bound_expr = re.sub(r'\\left\(', r'(', bound_expr)
    bound_expr = re.sub(r'\\right\)', r')', bound_expr)
    
    # Extract constraint and bounds using wedge
    if r'\wedge' in bound_expr:
        parts = bound_expr.split(r'\wedge', 1)
        constraint_part = parts[0].strip().replace('{', '').replace('}', '')
        bound_part = parts[1].strip().replace('{', '').replace('}', '') if len(parts) > 1 else ""
        
        # Clean constraint
        constraint_clean = _format_constraint(constraint_part)
        
        # Clean bounds  
        bound_clean = _format_bounds(bound_part, strict)
        
        # Combine properly
        if constraint_clean and constraint_clean != "\\text{(no additional constraints)}":
            return f"{constraint_clean} \\text{{ and }} {bound_clean}"
        else:
            return bound_clean
    
    return bound_expr


def _format_constraint(constraint_str):
    """Format constraint part of the expression."""
    if not constraint_str or constraint_str.strip() == "":
        return ""
    
    # Remove text wrapper and clean
    constraint_str = re.sub(r'\\text\{([^}]*)\}', r'\1', constraint_str)
    
    if "no additional constraints" in constraint_str.lower():
        return ""
    
    # Format as math expression
    if any(op in constraint_str for op in ['<=', '>=', '<', '>', '=']):
        return constraint_str.strip()
    
    return constraint_str.strip()


def _format_bounds(bound_str, strict=True):
    """Format bounds part of the expression."""
    if not bound_str:
        return ""
    
    # Clean up the bound string
    bound_str = bound_str.strip()
    
    # Handle infinity symbols
    bound_str = bound_str.replace('-\\infty', '-\\infty')
    bound_str = bound_str.replace('+\\infty', '+\\infty')
    bound_str = bound_str.replace('\\infty', '\\infty')
    
    # Choose appropriate inequality symbols
    if strict:
        lt_symbol = "<"
        le_symbol = "<"
    else:
        lt_symbol = "\\leq"
        le_symbol = "\\leq"
    
    # Replace inequality symbols consistently
    if " < x < " in bound_str:
        if not strict:
            bound_str = bound_str.replace(" < x < ", f" {le_symbol} x {le_symbol} ")
    elif " ≤ x ≤ " in bound_str or " <= x <= " in bound_str:
        bound_str = re.sub(r' (≤|<=) x (≤|<=) ', f' {le_symbol} x {le_symbol} ', bound_str)
    
    return bound_str


def save_simple_latex_results(results, filename="latex_simple.txt", output_dir="output"):
    """
    Save simplified, mathematical LaTeX results that focus on the core inequalities.
    
    Args:
        results: List of LaTeX result strings
        filename: Output filename
        output_dir: Output directory
        
    Returns:
        Full path to saved file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Full file path
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("% Simplified LaTeX for Copy-Paste\n")
            f.write("% Just the mathematical content\n\n")
            
            for i, result in enumerate(results):
                f.write(f"% Case {i+1}\n")
                
                # Extract just the mathematical inequalities
                simplified = _extract_mathematical_content(result)
                
                if simplified:
                    f.write("\\[\n")
                    f.write(simplified)
                    f.write("\n\\]\n\n")
                else:
                    f.write("% (No clear mathematical content extracted)\n\n")
        
        return filepath
    except Exception as e:
        raise IOError(f"Failed to save simplified LaTeX file: {e}")


def _extract_mathematical_content(latex_result):
    """
    Extract just the core mathematical inequalities from a LaTeX result.
    
    Args:
        latex_result: Full LaTeX result string
        
    Returns:
        Simplified mathematical expression
    """
    # Split by the standard separators
    parts = latex_result.split(r'\\[1em]')
    
    if len(parts) < 2:
        return ""
    
    # Look for the bounds in parts[1] and parts[2]
    mathematical_parts = []
    
    for i in range(1, min(3, len(parts))):
        bound_part = parts[i]
        
        # Extract the mathematical content
        if r'\wedge' in bound_part:
            # Split on wedge to get constraint and bound
            wedge_parts = bound_part.split(r'\wedge', 1)
            if len(wedge_parts) >= 2:
                constraint = wedge_parts[0].strip()
                bound = wedge_parts[1].strip()
                
                # Clean both parts
                constraint_clean = _clean_mathematical_expr(constraint)
                bound_clean = _clean_mathematical_expr(bound)
                
                # Combine if we have both
                if constraint_clean and bound_clean:
                    mathematical_parts.append(f"{constraint_clean} \\text{{ and }} {bound_clean}")
                elif bound_clean:
                    mathematical_parts.append(bound_clean)
        else:
            # Just clean the whole expression
            cleaned = _clean_mathematical_expr(bound_part)
            if cleaned:
                mathematical_parts.append(cleaned)
    
    # Return the first meaningful mathematical expression
    if mathematical_parts:
        return mathematical_parts[0]
    
    return ""


def _clean_mathematical_expr(expr):
    """
    Clean a mathematical expression by removing LaTeX formatting cruft.
    
    Args:
        expr: Mathematical expression string
        
    Returns:
        Cleaned mathematical expression
    """
    if not expr:
        return ""
    
    # Remove outer braces and LaTeX cruft
    expr = re.sub(r'\\left\\{', '{', expr)
    expr = re.sub(r'\\right\\}', '}', expr)
    expr = re.sub(r'^\\{', '', expr)
    expr = re.sub(r'\\}$', '', expr)
    expr = re.sub(r'^{', '', expr)
    expr = re.sub(r'}$', '', expr)
    
    # Remove text wrappers for constraints we don't want
    expr = re.sub(r'\\text\{[^}]*no additional constraints[^}]*\}', '', expr, flags=re.IGNORECASE)
    
    # Clean up spacing
    expr = re.sub(r'\s+', ' ', expr).strip()
    
    # Return empty string if it's just whitespace or constraint-less
    if not expr or expr.isspace():
        return ""
    
    # Skip if it's just a constraint with no math
    if "no additional constraints" in expr.lower():
        return ""
    
    return expr


def process_and_save_latex(results, base_filename="inequality_solutions", output_dir="output"):
    """
    Process LaTeX results and save both formatted document and clean copy-paste versions.
    
    Args:
        results: List of LaTeX result strings
        base_filename: Base filename (without extension)
        output_dir: Output directory
        
    Returns:
        Dictionary with paths to saved files
    """
    saved_files = {}
    
    try:
        # Save clean copy-paste LaTeX results
        clean_file = save_plain_latex_results(
            results, 
            f"{base_filename}_raw.txt", 
            output_dir
        )
        saved_files['clean'] = clean_file
        
        # Save simplified mathematical LaTeX
        simple_file = save_simple_latex_results(
            results,
            f"{base_filename}_simple.txt",
            output_dir
        )
        saved_files['simple'] = simple_file
        
        # Create and save formatted LaTeX document
        latex_doc = create_latex_document(results)
        doc_file = save_latex_to_file(
            latex_doc, 
            f"{base_filename}.tex", 
            output_dir
        )
        saved_files['document'] = doc_file
        
        return saved_files
        
    except Exception as e:
        raise IOError(f"Failed to process and save LaTeX: {e}")


def generate_summary_report(results, saved_files):
    """
    Generate a summary report of the LaTeX processing.
    
    Args:
        results: List of LaTeX result strings
        saved_files: Dictionary of saved file paths
        
    Returns:
        Summary report string
    """
    report = []
    report.append("LaTeX Processing Summary")
    report.append("=" * 50)
    report.append(f"Number of cases processed: {len(results)}")
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    report.append("Saved Files:")
    for file_type, filepath in saved_files.items():
        report.append(f"  {file_type.capitalize()}: {filepath}")
    
    report.append("")
    report.append("File Descriptions:")
    report.append("  Clean: Copy-paste ready LaTeX with document structure")
    report.append("  Simple: Mathematical content only, minimal formatting") 
    report.append("  Document: Complete LaTeX document ready for compilation")
    
    return "\n".join(report)
