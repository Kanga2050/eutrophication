"""
Performance Configuration for Rational Inequality Solver

This module provides configuration options for optimizing performance
and controlling debug output in the solver system.
"""
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class PerformanceConfig:
    """Configuration for performance optimization settings"""
    
    # Debug and logging settings
    debug_mode: bool = False
    verbose_elimination: bool = True
    show_step_details: bool = True
    
    # Performance optimizations
    use_sign_analysis: bool = True
    cache_symbolic_operations: bool = True
    early_termination: bool = True
    
    # Memory management
    max_case_depth: int = 10
    max_cases_per_level: int = 100
    
    # LaTeX generation settings
    generate_latex: bool = True
    latex_include_debug_info: bool = False
    
    @classmethod
    def create_fast_mode(cls) -> 'PerformanceConfig':
        """Create configuration optimized for speed"""
        return cls(
            debug_mode=False,
            verbose_elimination=False,
            show_step_details=False,
            use_sign_analysis=True,
            cache_symbolic_operations=True,
            early_termination=True,
            generate_latex=False,
            latex_include_debug_info=False
        )
    
    @classmethod  
    def create_debug_mode(cls) -> 'PerformanceConfig':
        """Create configuration optimized for debugging"""
        return cls(
            debug_mode=True,
            verbose_elimination=True,
            show_step_details=True,
            use_sign_analysis=False,  # Disable for easier debugging
            cache_symbolic_operations=False,
            early_termination=False,
            generate_latex=True,
            latex_include_debug_info=True
        )
    
    @classmethod
    def create_production_mode(cls) -> 'PerformanceConfig':
        """Create configuration optimized for production use"""
        return cls(
            debug_mode=False,
            verbose_elimination=False,
            show_step_details=False,
            use_sign_analysis=True,
            cache_symbolic_operations=True,
            early_termination=True,
            generate_latex=True,
            latex_include_debug_info=False
        )

# Global default configuration
DEFAULT_CONFIG = PerformanceConfig()

def get_config() -> PerformanceConfig:
    """Get the current global configuration"""
    return DEFAULT_CONFIG

def set_config(config: PerformanceConfig):
    """Set the global configuration"""
    global DEFAULT_CONFIG
    DEFAULT_CONFIG = config

def set_fast_mode():
    """Switch to fast mode configuration"""
    set_config(PerformanceConfig.create_fast_mode())

def set_debug_mode():
    """Switch to debug mode configuration"""
    set_config(PerformanceConfig.create_debug_mode())

def set_production_mode():
    """Switch to production mode configuration"""
    set_config(PerformanceConfig.create_production_mode())
