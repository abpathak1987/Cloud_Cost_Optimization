import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import os

class CostVisualizer:
    def __init__(self):
        plt.style.use('classic')
        self.colors = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c', '#34495e', '#f1c40f']
        
    def plot_optimization_potential(self, cost_table: pd.DataFrame, recommendations: list):
        """Create a visualization of potential cost savings with numbers on the bars"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
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
        
        x = range(len(services))
        bars1 = ax.bar(x, current_costs, label='Projected Cost',
               color='#2ecc71', alpha=0.6)
        bars2 = ax.bar(x, potential_savings, bottom=current_costs,
               label='Potential Savings', color='#e74c3c', alpha=0.6)
        
        ax.set_title('Cost Optimization Potential by Service',
                     fontsize=14, fontweight='bold')
        ax.set_xlabel('Service', fontsize=12)
        ax.set_ylabel('Cost ($)', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(services, rotation=45, ha='right')
        
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        def add_labels(bars):
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + height/2,
                        f'${height:,.0f}',
                        ha='center', va='center', fontsize=9, fontweight='bold',
                        color='black')
        
        add_labels(bars1)
        add_labels(bars2)
        
        plt.tight_layout()
        return fig    
    
    def plot_service_costs(self, cost_table: pd.DataFrame, title="Cost Distribution by Service"):
        """Create a pie chart of costs by service"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Calculate service costs
        service_costs = cost_table.groupby('Service description')['Cost ($)'].sum()
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(service_costs.values, 
                                         labels=service_costs.index,
                                         autopct='%1.1f%%',
                                         colors=self.colors)
        
        ax.set_title(title, pad=20, fontsize=12, fontweight='bold')
        return fig
    
    def plot_cost_trends(self, daily_costs: pd.DataFrame):
        """Create a line plot of daily costs with anomalies highlighted"""
        fig, ax = plt.subplots(figsize=(15, 6))
        
        # Plot normal costs
        normal_costs = daily_costs[~daily_costs['is_anomaly']]
        anomaly_costs = daily_costs[daily_costs['is_anomaly']]
        
        ax.plot(daily_costs['date'], daily_costs['Cost ($)'], 
                label='Daily Cost', color='#3498db', alpha=0.6)
        
        # Plot moving average
        ax.plot(daily_costs['date'], daily_costs['MA7_cost'],
                label='7-day Moving Average', color='#2ecc71', linestyle='--')
        
        # Highlight anomalies
        if len(anomaly_costs) > 0:
            ax.scatter(anomaly_costs['date'], anomaly_costs['Cost ($)'],
                      color='#e74c3c', label='Cost Anomalies', s=100)
        
        ax.set_title('Daily Cost Trends with Anomaly Detection', 
                    fontsize=12, fontweight='bold')
        ax.set_xlabel('Date', fontsize=10)
        ax.set_ylabel('Cost ($)', fontsize=10)
        
        plt.xticks(rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
    
    def plot_cost_by_project(self, cost_table: pd.DataFrame):
        """Create a bar chart of costs by project"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        project_costs = cost_table.groupby('Project name')['Cost ($)'].sum()
        bars = ax.bar(range(len(project_costs)), project_costs.values, color=self.colors)
        
        ax.set_xticks(range(len(project_costs)))
        ax.set_xticklabels(project_costs.index, rotation=45, ha='right')
        
        ax.set_title('Total Cost by Project', fontsize=12, fontweight='bold')
        ax.set_xlabel('Project', fontsize=10)
        ax.set_ylabel('Cost ($)', fontsize=10)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:,.0f}',
                   ha='center', va='bottom')
        
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig    

    
    def plot_usage_patterns(self, cost_table: pd.DataFrame):
        """Create a heatmap of usage patterns"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create usage matrix by hour and day
        df = cost_table.copy()
        df['hour'] = pd.to_datetime(df['Usage start date']).dt.hour
        df['day'] = pd.to_datetime(df['Usage start date']).dt.day_name()
        
        usage_matrix = df.pivot_table(
            values='Usage amount',
            index='hour',
            columns='day',
            aggfunc='mean'
        )
        
        im = ax.imshow(usage_matrix, aspect='auto')
        plt.colorbar(im, ax=ax, label='Average Usage')
        
        ax.set_title('Usage Patterns by Hour and Day', 
                    fontsize=12, fontweight='bold')
        ax.set_xlabel('Day of Week', fontsize=10)
        ax.set_ylabel('Hour of Day', fontsize=10)
        
        ax.set_xticks(range(len(usage_matrix.columns)))
        ax.set_yticks(range(len(usage_matrix.index)))
        ax.set_xticklabels(usage_matrix.columns, rotation=45)
        ax.set_yticklabels(usage_matrix.index)
        
        plt.tight_layout()
        return fig

def create_executive_dashboard(cost_optimizer, output_dir="reports"):
    """Create a comprehensive executive dashboard"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create visualizer
    visualizer = CostVisualizer()
    
    # Get data
    daily_costs = cost_optimizer.daily_costs
    cost_table = cost_optimizer.cost_table
    recommendations = cost_optimizer.get_recommendations()
    
    print("\nGenerating visualizations...")
    
    # 1. Service Costs
    print("Creating service costs plot...")
    fig = visualizer.plot_service_costs(cost_table)
    fig.savefig(os.path.join(output_dir, "service_costs.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    # 2. Cost Trends
    print("Creating cost trends plot...")
    fig = visualizer.plot_cost_trends(daily_costs)
    fig.savefig(os.path.join(output_dir, "cost_trends.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    # 3. Project Costs
    print("Creating project costs plot...")
    fig = visualizer.plot_cost_by_project(cost_table)
    fig.savefig(os.path.join(output_dir, "project_costs.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    # 4. Optimization Potential
    print("Creating optimization potential plot...")
    fig = visualizer.plot_optimization_potential(cost_table, recommendations)
    fig.savefig(os.path.join(output_dir, "optimization.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    # 5. Usage Patterns
    print("Creating usage patterns plot...")
    fig = visualizer.plot_usage_patterns(cost_table)
    fig.savefig(os.path.join(output_dir, "usage_patterns.png"), dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    # Create summary report
    print("Generating summary report...")
    summary = cost_optimizer.get_optimization_summary()
    report_path = os.path.join(output_dir, "summary_report.txt")
    
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
    
    print("\nDashboard generation complete!")
    print(f"\nFiles generated in: {output_dir}")
    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        size = os.path.getsize(file_path)
        print(f"- {file}: {size:,} bytes")