import os
import shutil
from pathlib import Path

def cleanup_and_setup():
    # Get project root
    root = Path.cwd()
    print(f"Project root: {root}")
    
    # Move src from scripts to root
    scripts_src = root / 'scripts' / 'src'
    root_src = root / 'src'
    
    if scripts_src.exists():
        # Remove old src if exists
        if root_src.exists():
            shutil.rmtree(root_src)
            print(f"Removed old src directory: {root_src}")
            
        # Move src from scripts to root
        shutil.move(str(scripts_src), str(root_src))
        print(f"Moved src from {scripts_src} to {root_src}")
    
    # Create other necessary directories
    directories = ['data', 'tests']
    for dir_name in directories:
        dir_path = root / dir_name
        if not dir_path.exists():
            dir_path.mkdir()
            print(f"Created directory: {dir_path}")
    
    print("\nFinal structure:")
    for root_dir, dirs, files in os.walk(root):
        level = root_dir.replace(str(root), '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root_dir)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if not f.startswith('__pycache__'):
                print(f"{subindent}{f}")

if __name__ == "__main__":
    cleanup_and_setup()