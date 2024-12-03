import React, { useState, useEffect } from 'react';
import { LineChart, BarChart, Bar, XAxis, YAxis, Tooltip, Line, ResponsiveContainer } from 'recharts';
import { AlertTriangle, TrendingDown, Settings, DollarSign, Activity } from 'lucide-react';

export default function Dashboard() {
  const [data, setData] = useState({
    monitoring: {
      totalCost: 6393.59,
      anomalies: 5,
      alerts: [
        { service: 'Cloud SQL', severity: 'high', message: 'Cost spike detected' },
        { service: 'Compute Engine', severity: 'medium', message: 'Unusual usage pattern' }
      ]
    },
    recommendations: [
      { service: 'Cloud SQL', savings: 1278.72, message: 'Consider right-sizing' },
      { service: 'Compute Engine', savings: 651.44, message: 'Optimize instance types' }
    ],
    automation: {
      actionsExecuted: 3,
      successRate: 0.95,
      recentActions: [
        { service: 'Cloud SQL', action: 'Right-sized instances', status: 'success' }
      ]
    }
  });

  return (
    <div className="p-6 max-w-7xl mx-auto bg-gray-50">
      <h1 className="text-2xl font-bold mb-6">Cloud Cost Optimization</h1>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <h3 className="text-gray-500">Total Cost</h3>
            <DollarSign className="w-5 h-5 text-blue-500" />
          </div>
          <p className="text-2xl font-bold">${data.monitoring.totalCost.toLocaleString()}</p>
        </div>

        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <h3 className="text-gray-500">Potential Savings</h3>
            <TrendingDown className="w-5 h-5 text-green-500" />
          </div>
          <p className="text-2xl font-bold text-green-600">${1278.72.toLocaleString()}</p>
        </div>

        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <h3 className="text-gray-500">Anomalies</h3>
            <AlertTriangle className="w-5 h-5 text-orange-500" />
          </div>
          <p className="text-2xl font-bold">{data.monitoring.anomalies}</p>
        </div>

        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <h3 className="text-gray-500">Actions Success</h3>
            <Activity className="w-5 h-5 text-purple-500" />
          </div>
          <p className="text-2xl font-bold">{(data.automation.successRate * 100).toFixed(1)}%</p>
        </div>
      </div>

      {/* Alerts Section */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-4">Active Alerts</h2>
        <div className="space-y-3">
          {data.monitoring.alerts.map((alert, index) => (
            <div key={index} className={`p-3 rounded-lg ${
              alert.severity === 'high' ? 'bg-red-50' : 'bg-orange-50'
            }`}>
              <div className="flex items-start gap-2">
                <AlertTriangle className={`w-5 h-5 ${
                  alert.severity === 'high' ? 'text-red-500' : 'text-orange-500'
                }`} />
                <div>
                  <p className="font-semibold">{alert.service}</p>
                  <p className="text-sm text-gray-600">{alert.message}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-4">Optimization Recommendations</h2>
        <div className="space-y-3">
          {data.recommendations.map((rec, index) => (
            <div key={index} className="p-4 border rounded-lg hover:bg-gray-50">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold flex items-center gap-2">
                    <Settings className="w-5 h-5 text-blue-500" />
                    {rec.service}
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">{rec.message}</p>
                  <p className="text-sm text-green-600 mt-1">
                    Potential savings: ${rec.savings.toLocaleString()}
                  </p>
                </div>
                <button className="px-3 py-1 bg-blue-50 text-blue-600 rounded-md text-sm hover:bg-blue-100">
                  Apply
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Actions */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Recent Actions</h2>
        <div className="space-y-3">
          {data.automation.recentActions.map((action, index) => (
            <div key={index} className="p-3 border rounded-lg">
              <div className="flex items-center gap-2">
                <Activity className="w-5 h-5 text-purple-500" />
                <div>
                  <p className="font-semibold">{action.service}</p>
                  <p className="text-sm text-gray-600">{action.action}</p>
                </div>
                <span className="ml-auto text-sm text-green-600">
                  {action.status === 'success' && '✓ Completed'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}