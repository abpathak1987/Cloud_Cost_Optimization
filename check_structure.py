import os
from pathlib import Path

def check_project_structure():
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Check src directory
    src_dir = current_dir / "src"
    print(f"\nChecking src directory: {src_dir}")
    print(f"Exists: {src_dir.exists()}")
    
    # Check package directory
    package_dir = src_dir / "cloud_cost_optimizer"
    print(f"\nChecking package directory: {package_dir}")
    print(f"Exists: {package_dir.exists()}")
    
    # List all files in the project
    print("\nProject structure:")
    for root, dirs, files in os.walk(current_dir):
        level = root.replace(str(current_dir), '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

if __name__ == "__main__":
    check_project_structure()