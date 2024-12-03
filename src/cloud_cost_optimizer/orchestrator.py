from .monitoring.real_time_monitor import RealTimeMonitor
from .optimization.recommendation_engine import RecommendationEngine
from .automation.action_executor import ActionExecutor
import pandas as pd
from typing import Dict, Any
import time
from datetime import datetime, timedelta

class CloudCostOptimizer:
    def __init__(self):
        self.monitor = RealTimeMonitor()
        self.recommender = RecommendationEngine()
        self.executor = ActionExecutor()
        self.running = False
        self.last_update = None
        
    def start_monitoring(self, data_source: str, update_interval: int = 60):
        """Start real-time monitoring"""
        self.running = True
        while self.running:
            try:
                # Get new data
                new_data = self._get_new_data(data_source)
                
                # Process monitoring data
                monitoring_results = self.monitor.process_real_time_data(new_data)
                
                # Generate recommendations
                recommendations = self.recommender.analyze_resource_usage(new_data)
                
                # Schedule automated actions
                scheduled_actions = []
                for rec in recommendations:
                    if rec['confidence'] == 'high':
                        if self.executor.schedule_action(rec):
                            scheduled_actions.append(rec)
                
                # Execute scheduled actions
                action_results = self.executor.execute_scheduled_actions()
                
                # Update dashboard
                dashboard_data = self._update_dashboard(
                    monitoring_results, 
                    recommendations, 
                    action_results
                )
                
                self.last_update = datetime.now()
                
                # Wait for next iteration
                time.sleep(update_interval)
                
            except Exception as e:
                print(f"Error in monitoring loop: {str(e)}")
                time.sleep(update_interval)
    
    def stop_monitoring(self):
        """Stop the monitoring loop"""
        self.running = False
    
    def _get_new_data(self, data_source: str) -> pd.DataFrame:
        """Get new data from source"""
        if isinstance(data_source, str):
            # Load from CSV file
            return pd.read_csv(data_source)
        elif isinstance(data_source, pd.DataFrame):
            # Use provided DataFrame
            return data_source
        else:
            raise ValueError("Unsupported data source type")
    
    def _update_dashboard(
        self, 
        monitoring_results: Dict[str, Any],
        recommendations: list,
        action_results: list
    ) -> Dict[str, Any]:
        """Update dashboard with new data"""
        dashboard_data = {
            'timestamp': datetime.now(),
            'monitoring': {
                'total_cost': monitoring_results['metrics']['total_cost'],
                'anomalies': len(monitoring_results['anomalies']),
                'alerts': monitoring_results['alerts']
            },
            'optimization': {
                'recommendations_count': len(recommendations),
                'potential_savings': sum(
                    float(r['potential_savings'].replace('$', '').replace(',', ''))
                    for r in recommendations
                ),
                'top_recommendations': recommendations[:3]
            },
            'automation': {
                'actions_executed': len(action_results),
                'success_rate': len([r for r in action_results if r['status'] == 'simulated']) / 
                               len(action_results) if action_results else 0,
                'recent_actions': action_results[-5:] if action_results else []
            }
        }
        
        return dashboard_data

    def get_status(self) -> Dict[str, Any]:
        """Get current optimizer status"""
        return {
            'running': self.running,
            'last_update': self.last_update,
            'monitor_stats': {
                'data_points': len(self.monitor.historical_data),
                'active_anomalies': len([
                    a for a in self.monitor.historical_data.get('is_anomaly', [])
                    if a
                ])
            },
            'automation_stats': {
                'scheduled_actions': len(self.executor.scheduled_actions),
                'executed_actions': len(self.executor.executed_actions)
            }
        }