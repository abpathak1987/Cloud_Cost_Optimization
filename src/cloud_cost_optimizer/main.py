from fastapi import FastAPI
from cloud_cost_optimizer.config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.get("/")
async def root():
    return {"message": "Welcome to Cloud Cost Optimizer"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}