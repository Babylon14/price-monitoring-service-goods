from fastapi import FastAPI
from app.api.v1.api import api_router


app = FastAPI(
    title="Price Monitoring Service Goods API",
    description="Service for tracking prices across various platforms",
    version="1.0.0"
)

# Подключаем большой роутер со всеми эндпоинтами v1
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok"}

