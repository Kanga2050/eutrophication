"""
Configuration management for the rational inequality solver.
"""
import os
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from pathlib import Path


@dataclass
class SolverConfig:
    """Configuration settings for the solver engine."""
    use_sign_analysis: bool = True
    max_recursion_depth: int = 10
    simplification_level: int = 2  # 0=none, 1=basic, 2=aggressive
    timeout_seconds: Optional[float] = None
    cache_results: bool = True
    

@dataclass  
class OutputConfig:
    """Configuration settings for output formatting."""
    output_directory: str = "output"
    latex_enabled: bool = True
    console_enabled: bool = True
    save_raw_latex: bool = True
    save_formatted_latex: bool = True
    latex_line_length: int = 80
    console_line_length: int = 100
    

@dataclass
class ProcessingConfig:
    """Configuration settings for input/case processing."""
    validate_inputs: bool = True
    auto_convert_strings: bool = True
    strict_operator_validation: bool = True
    case_combination_limit: int = 1000
    

@dataclass
class ApplicationConfig:
    """Main application configuration combining all sub-configs."""
    solver: SolverConfig = field(default_factory=SolverConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    
    def __post_init__(self):
        """Create output directory if it doesn't exist."""
        Path(self.output.output_directory).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ApplicationConfig':
        """Create config from dictionary."""
        solver_config = SolverConfig(**config_dict.get('solver', {}))
        output_config = OutputConfig(**config_dict.get('output', {}))
        processing_config = ProcessingConfig(**config_dict.get('processing', {}))
        
        return cls(
            solver=solver_config,
            output=output_config, 
            processing=processing_config
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'solver': {
                'use_sign_analysis': self.solver.use_sign_analysis,
                'max_recursion_depth': self.solver.max_recursion_depth,
                'simplification_level': self.solver.simplification_level,
                'timeout_seconds': self.solver.timeout_seconds,
                'cache_results': self.solver.cache_results,
            },
            'output': {
                'output_directory': self.output.output_directory,
                'latex_enabled': self.output.latex_enabled,
                'console_enabled': self.output.console_enabled,
                'save_raw_latex': self.output.save_raw_latex,
                'save_formatted_latex': self.output.save_formatted_latex,
                'latex_line_length': self.output.latex_line_length,
                'console_line_length': self.output.console_line_length,
            },
            'processing': {
                'validate_inputs': self.processing.validate_inputs,
                'auto_convert_strings': self.processing.auto_convert_strings,
                'strict_operator_validation': self.processing.strict_operator_validation,
                'case_combination_limit': self.processing.case_combination_limit,
            }
        }


# Global default configuration
DEFAULT_CONFIG = ApplicationConfig()


def load_config_from_file(config_path: str) -> ApplicationConfig:
    """
    Load configuration from a JSON or YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        ApplicationConfig instance
    """
    import json
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        if config_path.endswith('.json'):
            config_dict = json.load(f)
        elif config_path.endswith(('.yml', '.yaml')):
            try:
                import yaml
                config_dict = yaml.safe_load(f)
            except ImportError:
                raise ImportError("PyYAML required for YAML config files")
        else:
            raise ValueError("Config file must be .json, .yml, or .yaml")
    
    return ApplicationConfig.from_dict(config_dict)


def save_config_to_file(config: ApplicationConfig, config_path: str):
    """
    Save configuration to a JSON file.
    
    Args:
        config: Configuration to save
        config_path: Path where to save the configuration
    """
    import json
    
    with open(config_path, 'w') as f:
        json.dump(config.to_dict(), f, indent=2)
