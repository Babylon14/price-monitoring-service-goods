from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.product import Product


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_url(self, url: str) -> Product | None:
        """Метод для получения продукта по url"""
        result = await self.db.execute(select(Product).where(Product.url == str(url)))
        return result.scalar_one_or_none()
    
    
    async def create(self, **kwargs) -> Product:
        """Метод для создания продукта"""
        instance = Product(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance


    


