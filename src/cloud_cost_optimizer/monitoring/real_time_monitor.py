import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class RealTimeMonitor:
    def __init__(self):
        self.anomaly_detector = IsolationForest(contamination=0.1)
        self.scaler = StandardScaler()
        self.historical_data = pd.DataFrame()
        self.thresholds = {}
        
    def process_real_time_data(self, new_data: pd.DataFrame) -> Dict[str, Any]:
        """Process new data and detect anomalies in real-time"""
        # Update historical data
        self.historical_data = pd.concat([self.historical_data, new_data]).tail(1000)
        
        # Detect anomalies
        anomalies = self.detect_anomalies(new_data)
        
        # Calculate current metrics
        metrics = self.calculate_metrics(new_data)
        
        return {
            'anomalies': anomalies,
            'metrics': metrics,
            'alerts': self.generate_alerts(new_data, anomalies)
        }
    
    def detect_anomalies(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect cost and usage anomalies"""
        anomalies = []
        
        # Group by service
        for service in data['Service description'].unique():
            service_data = data[data['Service description'] == service]
            
            # Prepare features for anomaly detection
            features = ['Cost ($)', 'Usage amount']
            X = service_data[features].values
            
            if len(X) > 0:
                # Scale features
                X_scaled = self.scaler.fit_transform(X)
                
                # Detect anomalies
                predictions = self.anomaly_detector.fit_predict(X_scaled)
                
                # Record anomalies
                anomaly_indices = np.where(predictions == -1)[0]
                for idx in anomaly_indices:
                    anomalies.append({
                        'service': service,
                        'timestamp': service_data.iloc[idx]['Usage start date'],
                        'cost': service_data.iloc[idx]['Cost ($)'],
                        'usage': service_data.iloc[idx]['Usage amount'],
                        'severity': 'high' if service_data.iloc[idx]['Cost ($)'] > 100 else 'medium'
                    })
        
        return anomalies
    
    def calculate_metrics(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate real-time metrics"""
        return {
            'total_cost': data['Cost ($)'].sum(),
            'average_usage': data['Usage amount'].mean(),
            'cost_rate': data['Cost ($)'].sum() / len(data) if len(data) > 0 else 0,
            'service_count': data['Service description'].nunique()
        }
    
    def generate_alerts(self, data: pd.DataFrame, anomalies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate alerts based on anomalies and thresholds"""
        alerts = []
        
        # Cost threshold alerts
        for service in data['Service description'].unique():
            service_cost = data[data['Service description'] == service]['Cost ($)'].sum()
            threshold = self.thresholds.get(service, 1000)  # Default threshold
            
            if service_cost > threshold:
                alerts.append({
                    'type': 'cost_threshold',
                    'service': service,
                    'message': f'Cost threshold exceeded for {service}: ${service_cost:,.2f}',
                    'severity': 'high'
                })
        
        # Anomaly-based alerts
        for anomaly in anomalies:
            alerts.append({
                'type': 'anomaly',
                'service': anomaly['service'],
                'message': f'Anomaly detected in {anomaly["service"]}: Cost=${anomaly["cost"]:,.2f}',
                'severity': anomaly['severity']
            })
        
        return alerts