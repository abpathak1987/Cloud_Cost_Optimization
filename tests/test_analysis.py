import os
import sys
from pathlib import Path

# Add src to Python path and set correct working directory
def setup_environment():
    # Get project root (parent of tests directory)
    project_root = Path(__file__).parent.parent
    
    # Change to project root directory
    os.chdir(project_root)
    
    # Add src to Python path
    src_path = project_root / 'src'
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    print(f"Working directory: {os.getcwd()}")
    print(f"Python path: {src_path}")

def main():
    setup_environment()
    
    from cloud_cost_optimizer.services.cost_optimizer import CostOptimizer
    
    # Initialize optimizer
    optimizer = CostOptimizer()
    
    # Load and process data
    print("\nLoading data...")
    optimizer.initialize_monitoring(
        cost_table_path="data/My Billing Account_Cost table, 2024-10-01 — 2024-10-31.csv",
        cost_breakdown_path="data/My Billing Account_Cost Breakdown, 2024-10-01 – 2024-10-31.csv",
        reports_path="data/My Billing Account_Reports, 2024-11-01 — 2024-11-18.csv"
    )
    
    # Get current status
    print("\nCurrent Status:")
    status = optimizer.get_current_status()
    print(f"Total Cost: ${status['total_cost']:,.2f}")
    print("\nCosts by Service:")
    for service, cost in status['by_service'].items():
        print(f"{service}: ${cost:,.2f}")
    
    # Get recommendations
    print("\nRecommendations:")
    recommendations = optimizer.get_recommendations()
    for rec in recommendations:
        print(f"\n- {rec['service']}: {rec['message']}")
        print(f"  Potential savings: {rec['potential_savings']}")
    
    # Get optimization summary
    print("\nOptimization Summary:")
    summary = optimizer.get_optimization_summary()
    print(f"Total Potential Savings: ${summary['total_potential_savings']:,.2f}")
    print(f"Number of Optimizations: {summary['optimization_count']}")
    print(f"Services to Optimize: {', '.join(summary['services_to_optimize'])}")

if __name__ == "__main__":
    main()