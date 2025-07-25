"""
Console formatter for readable output display.
"""
import re
from typing import List, Optional


class ConsoleFormatter:
    """Formatter for console output display."""
    
    def __init__(self, line_length: int = 100):
        """
        Initialize console formatter.
        
        Args:
            line_length: Maximum line length for console output
        """
        self.line_length = line_length
    
    def format_results(self, results: List[str], show_details: bool = True) -> str:
        """
        Format LaTeX results for console display.
        
        Args:
            results: List of LaTeX result strings
            show_details: Whether to show detailed case information
            
        Returns:
            Formatted string for console display
        """
        if not results:
            return "No results to display."
        
        output = []
        output.append("INEQUALITY SOLVER RESULTS")
        output.append("=" * min(self.line_length, 80))
        output.append("")
        
        for i, result in enumerate(results):
            output.append(f"--- Case {i+1} ---")
            
            if show_details:
                formatted = self._format_single_result(result)
                output.append(formatted)
            else:
                summary = self._summarize_result(result)
                output.append(summary)
            
            output.append("")
        
        return "\\n".join(output)
    
    def _format_single_result(self, latex_result: str) -> str:
        """Format a single LaTeX result for console."""
        # Extract case information
        parts = latex_result.split(r'\\\\[1em]')
        
        if len(parts) < 2:
            return self._simplify_latex_for_console(latex_result)
        
        # Get case header
        case_header = parts[0]
        case_header = self._clean_case_header(case_header)
        
        # Extract constraints and bounds
        if len(parts) > 1:
            bounds_info = self._extract_bounds_info(parts[1:])
            return f"{case_header}\\n{bounds_info}"
        
        return case_header
    
    def _summarize_result(self, latex_result: str) -> str:
        """Create a brief summary of the result."""
        # Extract just the essential information
        if 'min(' in latex_result or 'max(' in latex_result:
            return "Solution involves bound expressions"
        elif 'x <' in latex_result or 'x >' in latex_result:
            return "Direct variable bounds found"
        elif 'no additional constraints' in latex_result:
            return "Constraint-only case"
        else:
            return "Complex case analysis"
    
    def _clean_case_header(self, header: str) -> str:
        """Clean case header for console display."""
        # Remove LaTeX formatting
        cleaned = header.replace(r'\\textbf{', '').replace('}', '')
        cleaned = cleaned.replace(r' \\\\ ', ' | ')
        
        # Simplify verbose descriptions
        if "Entire expression" in cleaned and "because" in cleaned:
            # Extract case number
            case_match = re.search(r'Case (\\d+)', cleaned)
            if case_match:
                case_num = case_match.group(1)
                
                if "> 0" in cleaned or "positive" in cleaned.lower():
                    return f"Case {case_num}: Positive condition"
                elif "< 0" in cleaned or "negative" in cleaned.lower():
                    return f"Case {case_num}: Negative condition"
                else:
                    return f"Case {case_num}: Mixed condition"
        
        return cleaned
    
    def _extract_bounds_info(self, bounds_parts: List[str]) -> str:
        """Extract and format bounds information."""
        result_lines = []
        
        for part in bounds_parts:
            # Clean LaTeX formatting
            cleaned = self._simplify_latex_for_console(part)
            
            # Extract constraint and bound information
            if r'\\wedge' in part:
                constraint_part, bound_part = part.split(r'\\wedge', 1)
                
                constraint = self._clean_constraint(constraint_part)
                bound = self._clean_bound(bound_part)
                
                if constraint and constraint != "(no additional constraints)":
                    result_lines.append(f"  Constraints: {constraint}")
                
                if bound:
                    # Limit bound length for readability
                    if len(bound) > self.line_length - 15:
                        bound = bound[:self.line_length - 18] + "..."
                    result_lines.append(f"  Bounds: {bound}")
            else:
                cleaned_part = cleaned[:self.line_length - 5] + "..." if len(cleaned) > self.line_length else cleaned
                result_lines.append(f"  {cleaned_part}")
        
        return "\\n".join(result_lines) if result_lines else "  No specific bounds"
    
    def _clean_constraint(self, constraint_part: str) -> str:
        """Clean constraint part for console display."""
        cleaned = constraint_part.replace(r'\\left\\{', '').replace(r'\\text{', '').replace('}', '').strip()
        return cleaned
    
    def _clean_bound(self, bound_part: str) -> str:
        """Clean bound part for console display."""
        cleaned = bound_part.replace(r'\\right\\}', '').replace(r'\\left(', '').replace(r'\\right)', '').strip()
        cleaned = cleaned.replace(r'\\le', '<=').replace(r'\\ge', '>=')
        cleaned = cleaned.replace(r'\\min\\left(', 'min(').replace(r'\\max\\left(', 'max(')
        return cleaned
    
    def _simplify_latex_for_console(self, latex_str: str) -> str:
        """Simplify LaTeX string for console display."""
        # Replace LaTeX commands with console-friendly equivalents
        replacements = {
            r'\\textbf{': '',
            r'}': '',
            r'\\\\': ' | ',
            r'\\left\\{': '{',
            r'\\right\\}': '}',
            r'\\left(': '(',
            r'\\right)': ')',
            r'\\wedge': ' AND ',
            r'\\le': ' <= ',
            r'\\ge': ' >= ',
            r'\\min\\left(': 'min(',
            r'\\max\\left(': 'max(',
            r'\\text{': '',
            r'[1em]': '',
            r'\\infty': 'infinity',
            r'\\': '',
        }
        
        result = latex_str
        for latex_cmd, replacement in replacements.items():
            result = result.replace(latex_cmd, replacement)
        
        # Clean up multiple spaces
        result = re.sub(r'\\s+', ' ', result)
        return result.strip()
    
    def format_summary(self, 
                      num_cases: int, 
                      num_variables: int, 
                      num_constraints: int,
                      processing_time: Optional[float] = None) -> str:
        """
        Format a summary of the solving process.
        
        Args:
            num_cases: Number of cases generated
            num_variables: Number of variable terms
            num_constraints: Number of constraint terms
            processing_time: Time taken to process (optional)
            
        Returns:
            Formatted summary string
        """
        summary = []
        summary.append("SOLVING SUMMARY")
        summary.append("-" * 30)
        summary.append(f"Cases generated: {num_cases}")
        summary.append(f"Variable terms: {num_variables}")
        summary.append(f"Constraint terms: {num_constraints}")
        
        if processing_time is not None:
            summary.append(f"Processing time: {processing_time:.3f} seconds")
        
        return "\\n".join(summary)
