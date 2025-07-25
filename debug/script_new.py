import sys
import os
# Add parent directory to path to import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
Legacy script.py - now refactored into separate modules.
This file imports from the new modular structure for backward compatibility.
"""
from solver import solve_rational_ineq_full

# Re-export the main function for backward compatibility
__all__ = ['solve_rational_ineq_full']
