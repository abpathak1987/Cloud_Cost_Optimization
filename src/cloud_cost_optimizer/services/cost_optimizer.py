import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from ..data.processors.billing_data_processor import BillingDataProcessor

class CostOptimizer:
    def __init__(self):
        self.processor = BillingDataProcessor()
        
    def initialize_monitoring(self, cost_table_path: str, cost_breakdown_path: str, reports_path: str):
        """Initialize the monitoring system with historical data"""
        # Load and process data
        self.cost_table, self.cost_breakdown, self.reports = self.processor.load_billing_data(
            cost_table_path, cost_breakdown_path, reports_path
        )
        
        # Process daily costs
        self.daily_costs = self.processor.preprocess_data(self.cost_table)
        
        # Detect anomalies
        self.daily_costs = self.processor.detect_anomalies(self.daily_costs)
        
        print(f"Processed {len(self.cost_table)} billing records")
        print(f"Found {self.daily_costs['is_anomaly'].sum()} cost anomalies")
    
    def get_current_status(self) -> dict:
        """Get current cost and usage status"""
        latest_date = self.daily_costs['date'].max()
        current_costs = self.daily_costs[self.daily_costs['date'] == latest_date].copy()
        
        status = {
            'total_cost': self.cost_table['Cost ($)'].sum(),
            'by_service': self.cost_table.groupby('Service description')['Cost ($)'].sum().to_dict(),
            'by_project': self.cost_table.groupby('Project name')['Cost ($)'].sum().to_dict(),
            'active_anomalies': current_costs[current_costs['is_anomaly']].to_dict('records')
        }
        
        return status
    
    def get_recommendations(self) -> list:
        """Get cost optimization recommendations"""
        recommendations = []
        
        # Analyze service costs
        service_costs = self.cost_table.groupby('Service description').agg({
            'Cost ($)': ['sum', 'mean', 'std']
        }).reset_index()
        
        service_costs.columns = ['Service description', 'total_cost', 'mean_cost', 'std_cost']
        
        for _, row in service_costs.iterrows():
            service = row['Service description']
            cv = row['std_cost'] / row['mean_cost'] if row['mean_cost'] > 0 else 0
            
            if cv > 0.5:  # High variation
                recommendations.append({
                    'service': service,
                    'message': 'High cost variation detected. Consider implementing cost controls.',
                    'potential_savings': f"{min(cv * 100, 30):.1f}%"  # Cap at 30%
                })
        
        return recommendations
    
    def get_optimization_summary(self) -> dict:
        """Get a summary of optimization opportunities"""
        recommendations = self.get_recommendations()
        
        total_cost = self.cost_table['Cost ($)'].sum()
        potential_savings = sum(
            float(rec['potential_savings'].rstrip('%')) / 100 * 
            self.cost_table[self.cost_table['Service description'] == rec['service']]['Cost ($)'].sum()
            for rec in recommendations
        )
        
        return {
            'total_potential_savings': potential_savings,
            'optimization_count': len(recommendations),
            'services_to_optimize': list(set(rec['service'] for rec in recommendations))
        }
    
    __all__ = ['CostOptimizer']