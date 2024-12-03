import os
import sys
from pathlib import Path
import pandas as pd

# Get project root and add src to Python path
current_dir = Path(__file__).parent.parent
src_path = str(current_dir / "src")
os.chdir(current_dir)  # Change to project root
sys.path.append(src_path)  # Add src to Python path

print(f"Project root: {current_dir}")
print(f"Python path: {sys.path}")

try:
    from cloud_cost_optimizer.orchestrator import CloudCostOptimizer

    # Initialize optimizer
    optimizer = CloudCostOptimizer()

    # Load test data
    data_path = current_dir / "data" / "My Billing Account_Cost table, 2024-10-01 — 2024-10-31.csv"
    test_data = pd.read_csv(data_path)

    # Test monitoring
    print("\nTesting monitoring...")
    monitoring_results = optimizer.monitor.process_real_time_data(test_data)
    print(f"Detected {len(monitoring_results['anomalies'])} anomalies")

    # Test recommendations
    print("\nTesting recommendations...")
    recommendations = optimizer.recommender.analyze_resource_usage(test_data)
    print(f"Generated {len(recommendations)} recommendations")

    # Test automation
    print("\nTesting automation...")
    for rec in recommendations[:3]:
        if optimizer.executor.schedule_action(rec):
            print(f"Scheduled action for {rec['service']}")

    results = optimizer.executor.execute_scheduled_actions()
    print(f"Executed {len(results)} actions")

    # Test dashboard update
    dashboard_data = optimizer._update_dashboard(
        monitoring_results,
        recommendations,
        results
    )

    print("\nDashboard Data:")
    for key, value in dashboard_data.items():
        print(f"\n{key.upper()}:")
        print(value)

except Exception as e:
    print(f"\nError: {str(e)}")
    print("\nCurrent directory:", os.getcwd())
    print("\nPython path:", sys.path)
    print("\nContents of src directory:", os.listdir(src_path))