from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ..orchestrator import CloudCostOptimizer
from cloud_cost_optimizer.services.cost_optimizer import CostOptimizer

app = FastAPI()
optimizer = CloudCostOptimizer()

def get_cost_data():
    optimizer = CostOptimizer()
    return optimizer.get_cost_data()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/dashboard")
async def get_dashboard_data():
    try:
        return {
            "monitoring": {
                "totalCost": optimizer.get_status()['total_cost'],
                "anomalies": len(optimizer.monitor.historical_data),
                "alerts": optimizer.monitor.get_current_alerts()
            },
            "recommendations": optimizer.recommender.analyze_resource_usage(
                optimizer.monitor.historical_data
            ),
            "automation": {
                "actionsExecuted": len(optimizer.executor.executed_actions),
                "successRate": optimizer.executor.get_success_rate(),
                "recentActions": optimizer.executor.get_recent_actions()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/actions/{action_id}/execute")
async def execute_action(action_id: str):
    try:
        result = optimizer.executor.execute_action(action_id)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))