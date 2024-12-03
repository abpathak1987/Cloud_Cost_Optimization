from typing import List, Dict, Any
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class RecommendationEngine:
    def __init__(self):
        self.scaler = StandardScaler()
        self.usage_patterns = {}
        self.cost_history = pd.DataFrame()
        
    def analyze_resource_usage(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze resource usage patterns and generate optimization recommendations"""
        recommendations = []
        
        # Analyze by service
        for service in data['Service description'].unique():
            service_data = data[data['Service description'] == service]
            
            # Resource right-sizing recommendations
            sizing_recs = self.analyze_resource_sizing(service_data)
            recommendations.extend(sizing_recs)
            
            # Usage optimization recommendations
            usage_recs = self.analyze_usage_patterns(service_data)
            recommendations.extend(usage_recs)
            
            # Cost optimization recommendations
            cost_recs = self.analyze_cost_patterns(service_data)
            recommendations.extend(cost_recs)
        
        return recommendations
    
    def analyze_resource_sizing(self, service_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze and recommend resource sizing optimizations"""
        recommendations = []
        
        # Calculate usage percentiles
        usage_stats = service_data['Usage amount'].describe()
        max_usage = usage_stats['max']
        p75_usage = usage_stats['75%']
        
        # Check for oversized resources
        if p75_usage < max_usage * 0.5:
            potential_savings = (max_usage - p75_usage) * service_data['Cost ($)'].mean()
            recommendations.append({
                'type': 'right_sizing',
                'service': service_data['Service description'].iloc[0],
                'message': f'Resource appears oversized. 75th percentile usage is {p75_usage:.1f}',
                'potential_savings': f'${potential_savings:.2f}',
                'confidence': 'high' if potential_savings > 100 else 'medium',
                'action': 'resize_resource',
                'parameters': {
                    'current_size': max_usage,
                    'recommended_size': p75_usage * 1.2  # Add 20% buffer
                }
            })
        
        return recommendations
    
    def analyze_usage_patterns(self, service_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze usage patterns for optimization opportunities"""
        recommendations = []
        
        # Convert timestamps to hour of day
        service_data['hour'] = pd.to_datetime(service_data['Usage start date']).dt.hour
        
        # Cluster usage patterns
        if len(service_data) >= 24:  # Need enough data points
            X = self.scaler.fit_transform(service_data[['Usage amount', 'hour']].values)
            kmeans = KMeans(n_clusters=3, random_state=42)
            clusters = kmeans.fit_predict(X)
            
            # Find low usage clusters
            for cluster_id in range(3):
                cluster_data = service_data[clusters == cluster_id]
                avg_usage = cluster_data['Usage amount'].mean()
                avg_cost = cluster_data['Cost ($)'].mean()
                
                if avg_usage < service_data['Usage amount'].mean() * 0.5:
                    recommendations.append({
                        'type': 'usage_optimization',
                        'service': service_data['Service description'].iloc[0],
                        'message': f'Low usage detected during hours: {cluster_data["hour"].unique().tolist()}',
                        'potential_savings': f'${avg_cost * len(cluster_data):.2f}',
                        'action': 'schedule_scaling',
                        'parameters': {
                            'hours': cluster_data['hour'].unique().tolist(),
                            'scale_factor': 0.5
                        }
                    })
        
        return recommendations
    
    def analyze_cost_patterns(self, service_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze cost patterns for optimization opportunities"""
        recommendations = []
        
        # Calculate cost metrics
        daily_costs = service_data.groupby(
            pd.to_datetime(service_data['Usage start date']).dt.date
        )['Cost ($)'].sum()
        
        cost_variation = daily_costs.std() / daily_costs.mean()
        
        if cost_variation > 0.5:  # High cost variation
            recommendations.append({
                'type': 'cost_optimization',
                'service': service_data['Service description'].iloc[0],
                'message': 'High cost variation detected. Consider implementing cost controls.',
                'potential_savings': f'${daily_costs.std() * 2:.2f}',  # Potential savings from stabilizing costs
                'action': 'implement_cost_control',
                'parameters': {
                    'budget_threshold': daily_costs.mean() * 1.5,
                    'alert_threshold': daily_costs.mean() * 1.2
                }
            })
        
        return recommendations