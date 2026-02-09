from fastapi import Depends, APIRouter

from app.database import get_db
from app.schemas.schema_product import ProductCreate
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService


router = APIRouter()

@router.post("/")
async def add_product(data: ProductCreate, db = Depends(get_db)):
    """Создание продукта"""
    repo = ProductRepository(db)
    service = ProductService(repo)
    return await service.create_new_monitor(data)

