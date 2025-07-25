"""
Enhanced LaTeX formatter with better organization and performance.
"""
import os
import re
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path

from sympy.printing.latex import latex

from ..utils.validation import ProcessingError


class LaTeXFormatter:
    """Enhanced LaTeX formatter with better performance and organization."""
    
    def __init__(self, 
                 output_directory: str = "output",
                 line_length: int = 80,
                 auto_create_dirs: bool = True):
        """
        Initialize LaTeX formatter.
        
        Args:
            output_directory: Directory for output files
            line_length: Maximum line length for formatting
            auto_create_dirs: Automatically create output directories
        """
        self.output_directory = Path(output_directory)
        self.line_length = line_length
        self.auto_create_dirs = auto_create_dirs
        
        if auto_create_dirs:
            self.output_directory.mkdir(parents=True, exist_ok=True)
    
    def format_and_save(self, 
                       results: List[str], 
                       base_filename: str,
                       title: Optional[str] = None) -> Dict[str, str]:
        """
        Format LaTeX results and save to files.
        
        Args:
            results: List of LaTeX result strings
            base_filename: Base filename for output files
            title: Document title (optional)
            
        Returns:
            Dictionary mapping format types to file paths
        """
        if not results:
            raise ProcessingError("No results to format")
        
        saved_files = {}
        
        try:
            # Save raw LaTeX expressions
            raw_file = self._save_raw_latex(results, base_filename)
            saved_files['raw'] = str(raw_file)
            
            # Save formatted LaTeX document
            formatted_file = self._save_formatted_document(results, base_filename, title)
            saved_files['formatted'] = str(formatted_file)
            
            # Save simple text version
            simple_file = self._save_simple_text(results, base_filename)
            saved_files['simple'] = str(simple_file)
            
            return saved_files
            
        except Exception as e:
            raise ProcessingError(f"Failed to save LaTeX files: {e}")
    
    def _save_raw_latex(self, results: List[str], base_filename: str) -> Path:
        """Save raw LaTeX expressions to text file."""
        raw_file = self.output_directory / f"{base_filename}_raw.txt"
        
        with open(raw_file, 'w', encoding='utf-8') as f:
            f.write(f"Raw LaTeX Results - Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
            f.write("=" * 80 + "\\n\\n")
            
            for i, result in enumerate(results):
                f.write(f"Case {i+1}:\\n")
                f.write("-" * 40 + "\\n")
                f.write(result + "\\n\\n")
        
        return raw_file
    
    def _save_formatted_document(self, 
                                results: List[str], 
                                base_filename: str,
                                title: Optional[str]) -> Path:
        """Save complete LaTeX document."""
        tex_file = self.output_directory / f"{base_filename}.tex"
        
        # Generate document
        if title is None:
            title = f"Rational Inequality Solutions - {base_filename}"
        
        document = self._create_latex_document(results, title)
        
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(document)
        
        return tex_file
    
    def _save_simple_text(self, results: List[str], base_filename: str) -> Path:
        """Save simplified text version for easy reading."""
        simple_file = self.output_directory / f"{base_filename}_simple.txt"
        
        with open(simple_file, 'w', encoding='utf-8') as f:
            f.write(f"Simplified Results - Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
            f.write("=" * 80 + "\\n\\n")
            
            for i, result in enumerate(results):
                f.write(f"Case {i+1}:\\n")
                f.write("-" * 40 + "\\n")
                
                # Simplify for text display
                simplified = self._simplify_for_text(result)
                f.write(simplified + "\\n\\n")
        
        return simple_file
    
    def _create_latex_document(self, results: List[str], title: str) -> str:
        """Create complete LaTeX document."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Document header
        doc = r"""\\documentclass{article}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{geometry}
\\geometry{margin=1in}

\\title{""" + title + r"""}
\\author{Rational Inequality Solver v2.0}
\\date{Generated on """ + timestamp + r"""}

\\begin{document}
\\maketitle

\\section{Solution Cases}

"""
        
        # Process each result
        for i, result in enumerate(results):
            doc += f"\\subsection{{Case {i+1}}}\\n\\n"
            
            # Clean and format the result
            cleaned = self._clean_latex_result(result)
            
            doc += "\\begin{align}\\n"
            doc += cleaned
            doc += "\\n\\end{align}\\n\\n"
        
        # Document footer
        doc += r"""
\\section{Notes}

These solutions represent the case-wise analysis of the given rational inequality system. Each case corresponds to different sign combinations of the numerator and denominator expressions.

The solutions are presented in the form:
\\begin{itemize}
\\item Strict inequalities: $\\max(\\text{lower bounds}) < x < \\min(\\text{upper bounds})$
\\item Non-strict inequalities: $\\max(\\text{lower bounds}) \\le x \\le \\min(\\text{upper bounds})$
\\end{itemize}

\\end{document}
"""
        
        return doc
    
    def _clean_latex_result(self, result: str) -> str:
        """Clean and format LaTeX result for document inclusion."""
        # Extract main components
        parts = result.split(r'\\\\[1em]')
        
        if len(parts) < 3:
            return result
        
        # Clean case header
        case_header = parts[0]
        case_header = self._clean_case_label(case_header)
        
        # Clean conditions
        conditions = []
        for part in parts[1:]:
            cleaned_part = self._format_latex_expression(part)
            conditions.append(cleaned_part)
        
        # Reconstruct
        return case_header + " \\\\\\\\[0.5em] " + " \\\\\\\\[0.5em] ".join(conditions)
    
    def _clean_case_label(self, label: str) -> str:
        """Clean verbose case labels."""
        # Remove excessive detail from case labels
        if "Case" in label:
            case_match = re.search(r'Case (\\d+)', label)
            if case_match:
                case_num = case_match.group(1)
                
                if "positive" in label.lower() or "> 0" in label:
                    return f"\\\\textbf{{Case {case_num}: Positive Condition}}"
                elif "negative" in label.lower() or "< 0" in label:
                    return f"\\\\textbf{{Case {case_num}: Negative Condition}}"
                else:
                    return f"\\\\textbf{{Case {case_num}}}"
        
        return label
    
    def _format_latex_expression(self, expr_str: str) -> str:
        """Format long LaTeX expressions with line breaks."""
        if len(expr_str) <= self.line_length:
            return expr_str
        
        # Find good break points
        break_points = ['+', '-', ',', r'\\wedge', r'\\min', r'\\max']
        
        # Split on natural break points
        parts = re.split(r'(\\+|\\-|,|\\\\wedge|\\\\min|\\\\max)', expr_str)
        
        formatted_lines = []
        current_line = ""
        
        for part in parts:
            if len(current_line + part) <= self.line_length:
                current_line += part
            else:
                if current_line:
                    formatted_lines.append(current_line.strip())
                current_line = part
        
        if current_line:
            formatted_lines.append(current_line.strip())
        
        # Join with LaTeX line breaks
        return " \\\\\\\\\\n    & ".join(formatted_lines)
    
    def _simplify_for_text(self, latex_result: str) -> str:
        """Simplify LaTeX for plain text display."""
        # Remove LaTeX commands
        text = latex_result
        
        # Replace LaTeX commands with text equivalents
        replacements = {
            r'\\textbf{': '',
            r'}': '',
            r'\\\\': ' | ',
            r'\\left\\{': '{',
            r'\\right\\}': '}',
            r'\\wedge': ' AND ',
            r'\\le': ' <= ',
            r'\\ge': ' >= ',
            r'\\min\\left(': 'min(',
            r'\\max\\left(': 'max(',
            r'\\left(': '(',
            r'\\right)': ')',
            r'[1em]': '',
            r'\\text{': '',
        }
        
        for latex_cmd, text_replacement in replacements.items():
            text = text.replace(latex_cmd, text_replacement)
        
        # Clean up multiple spaces
        text = re.sub(r'\\s+', ' ', text)
        text = text.strip()
        
        # Format for readability
        if ' AND ' in text and ('min(' in text or 'max(' in text):
            parts = text.split(' AND ')
            if len(parts) >= 2:
                constraint = parts[0].strip()
                bounds = ' AND '.join(parts[1:]).strip()
                
                if constraint and constraint != '(no additional constraints)':
                    return f"Constraints: {constraint}\\nBounds: {bounds}"
                else:
                    return f"Bounds: {bounds}"
        
        return text[:200] + "..." if len(text) > 200 else text
    
    def generate_summary_report(self, 
                              results: List[str], 
                              saved_files: Dict[str, str]) -> str:
        """Generate a summary report of the processing results."""
        report = []
        report.append("LaTeX Processing Summary")
        report.append("=" * 50)
        report.append(f"Total cases processed: {len(results)}")
        report.append(f"Output directory: {self.output_directory}")
        report.append("")
        
        report.append("Generated files:")
        for file_type, filepath in saved_files.items():
            report.append(f"  {file_type.capitalize()}: {filepath}")
        
        report.append("")
        report.append("File descriptions:")
        report.append("  Raw: Contains unprocessed LaTeX expressions")
        report.append("  Formatted: Complete LaTeX document ready for compilation")
        report.append("  Simple: Plain text version for easy reading")
        
        return "\\n".join(report)
