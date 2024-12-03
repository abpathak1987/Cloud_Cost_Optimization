import os
import shutil
from pathlib import Path

def setup_data_files():
    project_root = Path.cwd()
    data_dir = project_root / 'data'
    
    # Create data directory if it doesn't exist
    data_dir.mkdir(exist_ok=True)
    
    # Expected file names
    expected_files = [
        'My Billing Account_Cost table, 2024-10-01 — 2024-10-31.csv',
        'My Billing Account_Cost Breakdown, 2024-10-01 – 2024-10-31.csv',
        'My Billing Account_Reports, 2024-11-01 — 2024-11-18.csv'
    ]
    
    print("Checking data files...")
    for filename in expected_files:
        data_file = data_dir / filename
        if not data_file.exists():
            print(f"Missing: {filename}")
        else:
            print(f"Found: {filename}")
            
    print("\nTo continue, please copy your CSV files to:")
    print(data_dir)
    
    # List all files in data directory
    print("\nCurrent files in data directory:")
    for file in data_dir.glob('*'):
        print(f"  {file.name}")

if __name__ == "__main__":
    setup_data_files()