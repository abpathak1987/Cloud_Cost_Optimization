document.addEventListener('DOMContentLoaded', () => {
    fetch('data/dashboard_data.json')
        .then(response => response.json())
        .then(data => {
            populateDashboard(data);
        })
        .catch(error => console.error('Error loading dashboard data:', error));
});

function populateDashboard(data) {
    document.getElementById('timestamp').textContent = data.TIMESTAMP;
    document.getElementById('total-cost').textContent = data.MONITORING.total_cost.toFixed(2);
    document.getElementById('anomalies-count').textContent = data.MONITORING.anomalies;
    
    const highAlerts = data.MONITORING.alerts.filter(alert => alert.severity === 'high');
    const highAlertsList = document.getElementById('high-alerts');
    highAlerts.forEach(alert => {
        const li = document.createElement('li');
        li.textContent = `${alert.service}: ${alert.message}`;
        highAlertsList.appendChild(li);
    });

    document.getElementById('potential-savings').textContent = data.OPTIMIZATION.potential_savings.toFixed(2);
    const recommendationsList = document.getElementById('top-recommendations');
    data.OPTIMIZATION.top_recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = `${rec.service}: ${rec.message} (Potential savings: ${rec.potential_savings})`;
        recommendationsList.appendChild(li);
    });
}