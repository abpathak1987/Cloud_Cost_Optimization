import os
import shutil
from pathlib import Path

def setup_project():
    # Get project root
    project_root = Path.cwd()
    print(f"Setting up project in: {project_root}")
    
    # Clear existing structure
    dirs_to_clear = ['src', 'scripts', 'tests', 'data']
    for dir_name in dirs_to_clear:
        dir_path = project_root / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"Cleared {dir_path}")
    
    # Create fresh directory structure
    directories = [
        'src/cloud_cost_optimizer/data/processors',
        'src/cloud_cost_optimizer/services',
        'scripts',
        'tests',
        'data'
    ]
    
    # Create directories and __init__.py files
    for dir_path in directories:
        full_path = project_root / dir_path
        full_path.mkdir(parents=True)
        print(f"Created directory: {full_path}")
        
        # Add __init__.py to Python package directories
        if 'src' in dir_path:
            init_file = full_path / "__init__.py"
            init_file.touch()
            print(f"Created {init_file}")
    
    # Create root __init__.py
    (project_root / 'src' / '__init__.py').touch()
    
    # Create necessary Python files
    files_to_create = {
        'src/cloud_cost_optimizer/data/processors/billing_data_processor.py': '',
        'src/cloud_cost_optimizer/services/cost_optimizer.py': '',
        'scripts/check_structure.py': '',
        'tests/test_analysis.py': '',
        'tests/simple_test.py': ''
    }
    
    for file_path, content in files_to_create.items():
        file_full_path = project_root / file_path
        with open(file_full_path, 'w') as f:
            f.write(content)
        print(f"Created file: {file_path}")
    
    print("\nFinal structure:")
    for root, dirs, files in os.walk(project_root):
        level = root.replace(str(project_root), '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

if __name__ == "__main__":
    setup_project()