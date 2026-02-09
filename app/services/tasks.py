import asyncio
import random

from app.core.celery_app import celery_app
from app.database import get_db
from app.repositories.product_repository import ProductRepository


@celery_app.task(name="update_product_price")
def update_product_price(product_id: int):
    """Задача для обновления цены продукта"""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_async_update_price(product_id))
    

async def _async_update_price(product_id: int):
    db = await get_db()
    repo = ProductRepository(db)
    await asyncio.sleep(2)
    new_price = random.uniform(50000, 150000)

    # Тут будет логика обновления в БД через репозиторий
        # await repo.update_price(product_id, new_price)
    print(f"!!! ПАРСЕР: Товар {product_id} обновлен. Цена: {new_price}")

