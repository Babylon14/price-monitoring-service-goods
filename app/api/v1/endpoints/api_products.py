from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.schema_product import ProductCreate, ProductResponse
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService


router = APIRouter()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    """Создание продукта"""

    repo = ProductRepository(db)   # Репозиторий
    service = ProductService(repo) # Сервис
    product = await service.create_new_monitor(product_in) # Бизнес-логика

    # Если продукт с таким url уже существует
    if not product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такой с указанным url уже существует"
        )
    return product


# @router.get("/{product_id}", response_model=ProductResponse)
# async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
#     """Метод для получения продукта по id"""
#     repo = ProductRepository(db)
#     pass

