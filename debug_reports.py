import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

def check_environment():
    # Get current directory and project root
    current_dir = Path.cwd()
    print(f"Current working directory: {current_dir}")
    
    # Check reports directory
    reports_dir = current_dir / "reports"
    if not reports_dir.exists():
        print(f"Creating reports directory: {reports_dir}")
        reports_dir.mkdir(exist_ok=True)
    else:
        print(f"Reports directory exists: {reports_dir}")
    
    # Check data files
    data_dir = current_dir / "data"
    data_files = [
        "My Billing Account_Cost table, 2024-10-01 — 2024-10-31.csv",
        "My Billing Account_Cost Breakdown, 2024-10-01 – 2024-10-31.csv",
        "My Billing Account_Reports, 2024-11-01 — 2024-11-18.csv"
    ]
    
    print("\nChecking data files:")
    for file in data_files:
        file_path = data_dir / file
        if file_path.exists():
            print(f"✓ Found: {file}")
            # Print first few lines to verify content
            df = pd.read_csv(file_path)
            print(f"  - Rows: {len(df)}")
            print(f"  - Columns: {df.columns.tolist()}\n")
        else:
            print(f"✗ Missing: {file}")

    # Test matplotlib
    print("\nTesting matplotlib:")
    try:
        plt.figure()
        plt.plot([1, 2, 3], [1, 2, 3])
        test_plot_path = reports_dir / "test_plot.png"
        plt.savefig(test_plot_path)
        plt.close()
        print(f"✓ Successfully saved test plot to: {test_plot_path}")
        if test_plot_path.exists():
            print(f"✓ Test plot file exists: {test_plot_path}")
            print(f"  - File size: {test_plot_path.stat().st_size} bytes")
    except Exception as e:
        print(f"✗ Error saving test plot: {str(e)}")

    # List contents of reports directory
    print("\nContents of reports directory:")
    if reports_dir.exists():
        for item in reports_dir.iterdir():
            print(f"- {item.name}")
    else:
        print("Reports directory does not exist!")

if __name__ == "__main__":
    check_environment()