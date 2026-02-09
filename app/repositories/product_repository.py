from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

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


    async def update_price(self, product_id: int, new_price: float):
        """Метод для обновления цены продукта"""
        query = update(Product).where(Product.id == product_id).values(current_price=new_price)
        await self.db.execute(query)
        await self.db.commit()


