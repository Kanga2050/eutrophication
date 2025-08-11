"""
Case Management System for Hierarchical Variable Elimination

This module provides the core case management infrastructure for the rational
inequality solver system. It handles hierarchical case naming and case data
structures with support for nested subcases and elimination tracking.

Classes:
- CaseNamingSystem: Manages hierarchical case naming (Case 1 → Subcase 1.1 → etc.)
- HierarchicalCase: Represents a case with inequalities and hierarchical structure

Author: Simplified Rational Inequality Solver Team
Version: Pure Inequality System - No Constraint/Inequality Separation
"""
from collections import defaultdict


class CaseNamingSystem:
    """Manages hierarchical case naming (case 1, subcase 1.1, subsubcase 1.1.2, etc.)"""
    
    def __init__(self):
        self.case_counters = defaultdict(int)
        self.parent_cases = {}
    
    def get_case_name(self, parent_case=None, level=0, force_single_case=False):
        """Generate hierarchical case name"""
        if parent_case is None:
            # Top-level case
            self.case_counters[0] += 1
            case_name = f"Case {self.case_counters[0]}"
            case_id = str(self.case_counters[0])
        else:
            # Sub-case
            parent_id = self.parent_cases.get(parent_case, "1")
            
            # If this is a forced single case, don't increment level
            if force_single_case:
                # Use the parent's naming and just increment at the same level
                case_name = parent_case
                case_id = parent_id
            else:
                key = f"{parent_id}_{level}"
                self.case_counters[key] += 1
                
                if level == 1:
                    case_name = f"Subcase {parent_id}.{self.case_counters[key]}"
                    case_id = f"{parent_id}.{self.case_counters[key]}"
                elif level == 2:
                    case_name = f"Subsubcase {parent_id}.{self.case_counters[key]}"
                    case_id = f"{parent_id}.{self.case_counters[key]}"
                else:
                    # Deep nesting
                    prefix = "Sub" * level + "case"
                    case_name = f"{prefix} {parent_id}.{self.case_counters[key]}"
                    case_id = f"{parent_id}.{self.case_counters[key]}"
        
        self.parent_cases[case_name] = case_id
        return case_name, case_id
    
    def reset_level(self, level):
        """Reset counters for a specific level and all deeper levels"""
        keys_to_remove = [k for k in self.case_counters.keys() if isinstance(k, str) and len(k.split('_')) > level]
        for key in keys_to_remove:
            del self.case_counters[key]


class HierarchicalCase:
    """Represents a case in the hierarchical structure with only inequalities"""
    
    def __init__(self, name, case_id, inequalities, parent=None, level=0):
        self.name = name
        self.case_id = case_id
        self.inequalities = inequalities
        self.parent = parent
        self.level = level
        self.subcases = []
        self.elimination_steps = []
        self.is_solved = False
    
    def add_subcase(self, subcase):
        """Add a subcase to this case"""
        self.subcases.append(subcase)
    
    def add_elimination_step(self, step):
        """Add an elimination step to this case"""
        self.elimination_steps.append(step)
    
    def get_path(self):
        """Get the hierarchical path from root to this case"""
        path = []
        current = self
        while current:
            path.insert(0, current.name)
            current = current.parent
        return path
    
    def is_final_case(self):
        """Check if this is a final case (no more variables to eliminate)"""
        return len(self.subcases) == 0 and self.is_solved
    
    def solve_case(self, solver_func=None):
        """Mark this case as solved and optionally apply a solver function"""
        self.is_solved = True
        if solver_func:
            return solver_func(self.inequalities)
        return self.inequalities
    
    def get_all_inequalities(self):
        """Get all inequalities including those from elimination steps"""
        all_inequalities = list(self.inequalities)
        for step in self.elimination_steps:
            if 'resulting_inequalities' in step:
                all_inequalities.extend(step['resulting_inequalities'])
        return all_inequalities
    
    def __repr__(self):
        return f"HierarchicalCase(name='{self.name}', level={self.level}, inequalities={len(self.inequalities)})"
