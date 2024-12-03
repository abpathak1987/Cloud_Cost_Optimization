import os
import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
src_path = str(project_root / 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

print(f"Project root: {project_root}")
print(f"Source path: {src_path}")
print(f"Python path: {sys.path}")

try:
    from cloud_cost_optimizer.services.cost_optimizer import CostOptimizer
    print("Successfully imported CostOptimizer!")
except ImportError as e:
    print(f"Import failed: {str(e)}")
    
    # Check if files exist
    files_to_check = [
        'src/cloud_cost_optimizer/services/cost_optimizer.py',
        'src/cloud_cost_optimizer/data/processors/billing_data_processor.py'
    ]
    
    print("\nChecking files:")
    for file_path in files_to_check:
        full_path = project_root / file_path
        print(f"{file_path}: {'Exists' if full_path.exists() else 'Missing'}")