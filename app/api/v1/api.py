from fastapi import APIRouter
from app.api.v1.endpoints import api_products


api_router = APIRouter()

# Объединяем все модули эндпоинтов
api_router.include_router(api_products.router, prefix="/products", tags=["products"])

