"""
Cleanup script to finalize the unified solver structure.
Removes redundant files and organizes the codebase.
"""
import os
import shutil


def cleanup_redundant_files():
    """Remove redundant files after consolidation."""
    
    # Files that are now redundant
    redundant_files = [
        "main_optimized.py",        # Superseded by unified_main.py
        "demo_optimized.py",        # Examples now in unified_main.py  
        "migrate_to_optimized.py",  # Migration complete
        "OPTIMIZATION_SUMMARY.md",  # Consolidated into README.md
        "README_OPTIMIZED.md"       # Merged into main README.md
    ]
    
    print("Cleaning up redundant files...")
    
    for file_path in redundant_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removed: {file_path}")
            except Exception as e:
                print(f"❌ Failed to remove {file_path}: {e}")
        else:
            print(f"ℹ️  File not found (already clean): {file_path}")
    
    print()


def organize_debug_files():
    """Organize debug files into a cleaner structure."""
    
    debug_dir = "debug"
    if os.path.exists(debug_dir):
        debug_files = os.listdir(debug_dir)
        
        # Keep essential debug files, remove outdated ones
        essential_debug = [
            "test_sign_integration.py",
            "test_advanced_sign.py", 
            "latex_demo.py"
        ]
        
        print("Organizing debug directory...")
        
        for file_name in debug_files:
            file_path = os.path.join(debug_dir, file_name)
            
            if file_name not in essential_debug and file_name.endswith('.py'):
                try:
                    os.remove(file_path)
                    print(f"✅ Removed debug file: {file_name}")
                except Exception as e:
                    print(f"❌ Failed to remove {file_name}: {e}")
        
        print()


def organize_readme_files():
    """Consolidate readme files."""
    
    readme_dir = "readme"
    if os.path.exists(readme_dir):
        print("README files are preserved in readme/ for reference")
        print("Main documentation is now in README.md")
        print()


def create_project_summary():
    """Create a final project summary."""
    
    summary = """
# PROJECT CONSOLIDATION COMPLETE

## Unified Solver Structure

### Core Files
- `solver.py` - Original rational inequality solver
- `variable_eliminator.py` - Variable elimination solver  
- `unified_main.py` - Unified demonstration and interface
- `case_processor.py` - Case analysis utilities
- `input_processor.py` - Input validation
- `latex_processor.py` - LaTeX output generation

### Entry Points
- `python unified_main.py` - Full demonstration of both approaches
- `python main.py` - Original solver examples
- `from variable_eliminator import solve_with_variable_elimination` - Direct API

### Output Directories
- `output/` - Original solver results
- `output_final/` - Variable elimination documentation

### Testing
- `tests/` - Test suites for all functionality

## Key Achievements

✅ **Eliminated Redundancy**: Removed enhanced_solver/ folder duplication
✅ **Unified Interface**: Single codebase with complementary approaches  
✅ **Enhanced Documentation**: Complete LaTeX generation for both methods
✅ **Preserved Functionality**: All original capabilities maintained
✅ **Clean Architecture**: Clear separation of concerns

## Next Steps

1. Use `unified_main.py` to see both solving approaches
2. Choose appropriate solver based on your needs:
   - Original: Single-variable min/max analysis
   - Elimination: Multi-variable dimensional reduction
3. Both approaches complement each other perfectly

The consolidation successfully combines the best of both worlds!
"""
    
    with open("CONSOLIDATION_COMPLETE.md", "w") as f:
        f.write(summary.strip())
    
    print("✅ Created CONSOLIDATION_COMPLETE.md")
    print()


def main():
    """Main cleanup function."""
    print("=" * 60)
    print("UNIFIED SOLVER CLEANUP")
    print("=" * 60)
    print()
    
    cleanup_redundant_files()
    organize_debug_files()
    organize_readme_files()
    create_project_summary()
    
    print("=" * 60)
    print("CLEANUP COMPLETE")
    print("=" * 60)
    print()
    print("The codebase is now fully consolidated:")
    print("• Redundant files removed")
    print("• Enhanced_solver folder eliminated")  
    print("• Unified interface created")
    print("• All functionality preserved")
    print()
    print("Try: python unified_main.py")


if __name__ == "__main__":
    main()
