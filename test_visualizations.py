import os
from pathlib import Path
import matplotlib.pyplot as plt
from cloud_cost_optimizer.services.cost_optimizer import CostOptimizer
from cloud_cost_optimizer.visualizations.cost_visualizer import CostVisualizer, create_executive_dashboard

def test_visualizations():
    # Get project root and ensure we're in the right directory
    project_root = Path.cwd()
    reports_dir = project_root / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    print(f"Project root: {project_root}")
    print(f"Reports directory: {reports_dir}")
    
    # Initialize optimizer
    optimizer = CostOptimizer()
    
    # Load data
    print("\nLoading data...")
    optimizer.initialize_monitoring(
        cost_table_path="data/My Billing Account_Cost table, 2024-10-01 — 2024-10-31.csv",
        cost_breakdown_path="data/My Billing Account_Cost Breakdown, 2024-10-01 – 2024-10-31.csv",
        reports_path="data/My Billing Account_Reports, 2024-11-01 — 2024-11-18.csv"
    )
    
    # Create visualizer
    visualizer = CostVisualizer()
    
    print("\nGenerating visualizations...")
    
    # Test each visualization individually
    try:
        # 1. Service Costs
        print("\n1. Creating service costs plot...")
        fig = visualizer.plot_service_costs(optimizer.cost_table)
        fig.savefig(reports_dir / "service_costs.png", dpi=300, bbox_inches='tight')
        plt.close(fig)
        print("✓ Saved service_costs.png")
        
        # 2. Cost Trends
        print("\n2. Creating cost trends plot...")
        fig = visualizer.plot_cost_trends(optimizer.daily_costs)
        fig.savefig(reports_dir / "cost_trends.png", dpi=300, bbox_inches='tight')
        plt.close(fig)
        print("✓ Saved cost_trends.png")
        
        # 3. Project Costs
        print("\n3. Creating project costs plot...")
        fig = visualizer.plot_cost_by_project(optimizer.cost_table)
        fig.savefig(reports_dir / "project_costs.png", dpi=300, bbox_inches='tight')
        plt.close(fig)
        print("✓ Saved project_costs.png")
        
        # 4. Optimization Potential
        print("\n4. Creating optimization potential plot...")
        recommendations = optimizer.get_recommendations()
        fig = visualizer.plot_optimization_potential(optimizer.cost_table, recommendations)
        fig.savefig(reports_dir / "optimization.png", dpi=300, bbox_inches='tight')
        plt.close(fig)
        print("✓ Saved optimization.png")
        
        # 5. Usage Patterns
        print("\n5. Creating usage patterns plot...")
        fig = visualizer.plot_usage_patterns(optimizer.cost_table)
        fig.savefig(reports_dir / "usage_patterns.png", dpi=300, bbox_inches='tight')
        plt.close(fig)
        print("✓ Saved usage_patterns.png")
        
    except Exception as e:
        print(f"Error generating visualizations: {str(e)}")
        raise
    
    # Verify files were created
    print("\nVerifying generated files:")
    expected_files = [
        "service_costs.png",
        "cost_trends.png",
        "project_costs.png",
        "optimization.png",
        "usage_patterns.png"
    ]
    
    for filename in expected_files:
        file_path = reports_dir / filename
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✓ {filename} (Size: {size:,} bytes)")
        else:
            print(f"✗ {filename} not found!")

if __name__ == "__main__":
    test_visualizations()