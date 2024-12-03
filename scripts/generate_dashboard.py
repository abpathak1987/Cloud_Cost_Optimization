import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

class CostVisualizer:
    def __init__(self):
        # Use a built-in style that's clean and professional
        plt.style.use('ggplot')
        self.colors = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c', '#34495e', '#f1c40f']
    
    def plot_service_costs(self, cost_table: pd.DataFrame, title="Cost Distribution by Service"):
        """Create a pie chart of costs by service"""
        plt.figure(figsize=(10, 6))
        
        # Calculate service costs
        service_costs = cost_table.groupby('Service description')['Cost ($)'].sum()
        
        # Create pie chart
        plt.pie(service_costs.values, 
                labels=service_costs.index,
                autopct='%1.1f%%',
                colors=self.colors)
        
        plt.title(title, pad=20, fontsize=12, fontweight='bold')
        plt.axis('equal')
        return plt.gcf()
    
    def plot_cost_trends(self, daily_costs: pd.DataFrame):
        """Create a line plot of daily costs with anomalies highlighted"""
        plt.figure(figsize=(15, 6))
        
        # Plot normal costs
        normal_costs = daily_costs[~daily_costs['is_anomaly']]
        anomaly_costs = daily_costs[daily_costs['is_anomaly']]
        
        plt.plot(daily_costs['date'], daily_costs['Cost ($)'], 
                label='Daily Cost', color='#3498db', alpha=0.6)
        
        # Plot moving average
        plt.plot(daily_costs['date'], daily_costs['MA7_cost'],
                label='7-day Moving Average', color='#2ecc71', linestyle='--')
        
        # Highlight anomalies
        if len(anomaly_costs) > 0:
            plt.scatter(anomaly_costs['date'], anomaly_costs['Cost ($)'],
                       color='#e74c3c', label='Cost Anomalies', s=100)
        
        plt.title('Daily Cost Trends with Anomaly Detection', fontsize=12, fontweight='bold')
        plt.xlabel('Date', fontsize=10)
        plt.ylabel('Cost ($)', fontsize=10)
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        return plt.gcf()
    
    def plot_cost_by_project(self, cost_table: pd.DataFrame):
        """Create a bar chart of costs by project"""
        plt.figure(figsize=(12, 6))
        
        project_costs = cost_table.groupby('Project name')['Cost ($)'].sum()
        plt.bar(range(len(project_costs)), project_costs.values, color=self.colors)
        plt.xticks(range(len(project_costs)), project_costs.index, rotation=45, ha='right')
        
        plt.title('Total Cost by Project', fontsize=12, fontweight='bold')
        plt.xlabel('Project', fontsize=10)
        plt.ylabel('Cost ($)', fontsize=10)
        
        # Add value labels on top of bars
        for i, v in enumerate(project_costs.values):
            plt.text(i, v, f'${v:,.0f}', ha='center', va='bottom')
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        return plt.gcf()
    
    def plot_optimization_potential(self, cost_table: pd.DataFrame, recommendations: list):
        """Create a visualization of potential cost savings"""
        plt.figure(figsize=(10, 6))
        
        services = []
        current_costs = []
        potential_savings = []
        
        for rec in recommendations:
            service = rec['service']
            current_cost = cost_table[cost_table['Service description'] == service]['Cost ($)'].sum()
            saving_pct = float(rec['potential_savings'].rstrip('%')) / 100
            
            services.append(service)
            current_costs.append(current_cost * (1 - saving_pct))
            potential_savings.append(current_cost * saving_pct)
        
        # Create stacked bar chart
        x = range(len(services))
        plt.bar(x, current_costs, label='Projected Cost After Optimization',
                color='#2ecc71', alpha=0.6)
        plt.bar(x, potential_savings, bottom=current_costs,
                label='Potential Savings', color='#e74c3c', alpha=0.6)
        
        plt.title('Cost Optimization Potential by Service', fontsize=12, fontweight='bold')
        plt.xlabel('Service', fontsize=10)
        plt.ylabel('Cost ($)', fontsize=10)
        plt.xticks(x, services, rotation=45, ha='right')
        plt.legend()
        
        # Add value labels
        for i in range(len(services)):
            total = current_costs[i] + potential_savings[i]
            savings_pct = (potential_savings[i] / total) * 100
            plt.text(i, total, f'${total:,.0f}\n({savings_pct:.1f}% savings)', 
                    ha='center', va='bottom')
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        return plt.gcf()
    
    def plot_usage_patterns(self, cost_table: pd.DataFrame):
        """Create a heatmap of usage patterns"""
        plt.figure(figsize=(12, 6))
        
        # Create usage matrix by hour and day
        cost_table['hour'] = cost_table['Usage start date'].dt.hour
        cost_table['day'] = cost_table['Usage start date'].dt.day_name()
        
        usage_matrix = cost_table.pivot_table(
            values='Usage amount',
            index='hour',
            columns='day',
            aggfunc='mean'
        )
        
        # Create heatmap
        plt.imshow(usage_matrix, cmap='YlOrRd', aspect='auto')
        plt.colorbar(label='Average Usage')
        
        # Set labels
        plt.title('Usage Patterns by Hour and Day', fontsize=12, fontweight='bold')
        plt.xlabel('Day of Week', fontsize=10)
        plt.ylabel('Hour of Day', fontsize=10)
        
        # Set ticks
        plt.xticks(range(len(usage_matrix.columns)), usage_matrix.columns, rotation=45)
        plt.yticks(range(len(usage_matrix.index)), usage_matrix.index)
        
        plt.tight_layout()
        return plt.gcf()

def create_executive_dashboard(cost_optimizer, output_dir="reports"):
    """Create a comprehensive executive dashboard"""
    import os
    from datetime import datetime
    
    # Create visualizer
    visualizer = CostVisualizer()
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get data
    daily_costs = cost_optimizer.daily_costs
    cost_table = cost_optimizer.cost_table
    recommendations = cost_optimizer.get_recommendations()
    
    # Create visualizations
    figs = {
        'service_costs': visualizer.plot_service_costs(cost_table),
        'cost_trends': visualizer.plot_cost_trends(daily_costs),
        'project_costs': visualizer.plot_cost_by_project(cost_table),
        'optimization': visualizer.plot_optimization_potential(cost_table, recommendations),
        'usage_patterns': visualizer.plot_usage_patterns(cost_table)
    }
    
    # Save all figures
    print("\nSaving visualizations:")
    for name, fig in figs.items():
        filepath = f"{output_dir}/{name}.png"
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"✓ {name}.png")
    
    # Create summary report
    summary = cost_optimizer.get_optimization_summary()
    report_path = f"{output_dir}/summary_report.txt"
    
    with open(report_path, 'w') as f:
        f.write("Cloud Cost Optimization Summary\n")
        f.write("=" * 30 + "\n\n")
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("1. Overall Costs\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total Cost: ${cost_table['Cost ($)'].sum():,.2f}\n")
        f.write(f"Potential Savings: ${summary['total_potential_savings']:,.2f}\n")
        f.write(f"Number of Optimization Opportunities: {summary['optimization_count']}\n\n")
        
        f.write("2. Service-wise Recommendations\n")
        f.write("-" * 20 + "\n")
        for rec in recommendations:
            f.write(f"\n• {rec['service']}:\n")
            f.write(f"  - {rec['message']}\n")
            f.write(f"  - Potential Savings: {rec['potential_savings']}\n")
        
        f.write("\n3. Key Metrics\n")
        f.write("-" * 20 + "\n")
        service_costs = cost_table.groupby('Service description')['Cost ($)'].sum()
        f.write("\nTop Cost Centers:\n")
        for service, cost in service_costs.nlargest(3).items():
            f.write(f"• {service}: ${cost:,.2f}\n")
    
    print(f"✓ summary_report.txt")