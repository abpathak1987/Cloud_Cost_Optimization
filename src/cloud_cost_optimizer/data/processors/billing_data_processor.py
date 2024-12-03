import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, Dict

class BillingDataProcessor:
    def load_billing_data(
        self, 
        cost_table_path: str, 
        cost_breakdown_path: str, 
        reports_path: str
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Load billing data from CSV files"""
        # Load data
        cost_table = pd.read_csv(cost_table_path)
        cost_breakdown = pd.read_csv(cost_breakdown_path)
        reports = pd.read_csv(reports_path)
        
        # Convert date columns
        date_columns = ['Usage start date', 'Usage end date']
        for col in date_columns:
            if col in cost_table.columns:
                cost_table[col] = pd.to_datetime(cost_table[col])
        
        return cost_table, cost_breakdown, reports
    
    def preprocess_data(self, cost_table: pd.DataFrame) -> pd.DataFrame:
        """Preprocess billing data for analysis"""
        df = cost_table.copy()
        
        # Create daily aggregation
        df['date'] = df['Usage start date'].dt.date
        daily_costs = df.groupby(['date', 'Service description', 'Project name'])[
            ['Cost ($)', 'Usage amount']
        ].sum().reset_index()
        
        # Calculate moving averages
        daily_costs['MA7_cost'] = daily_costs.groupby(['Service description', 'Project name'])['Cost ($)'].transform(
            lambda x: x.rolling(window=7, min_periods=1).mean()
        )
        
        return daily_costs

    def detect_anomalies(self, daily_costs: pd.DataFrame, zscore_threshold: float = 2.0) -> pd.DataFrame:
        """Detect cost anomalies using z-score method"""
        df = daily_costs.copy()
        df['is_anomaly'] = False
        
        # Calculate z-scores for costs by service
        for service in df['Service description'].unique():
            service_data = df[df['Service description'] == service]
            mean_cost = service_data['Cost ($)'].mean()
            std_cost = service_data['Cost ($)'].std()
            
            if std_cost > 0:  # Avoid division by zero
                z_scores = np.abs((service_data['Cost ($)'] - mean_cost) / std_cost)
                df.loc[service_data.index, 'is_anomaly'] = z_scores > zscore_threshold
        
        return df