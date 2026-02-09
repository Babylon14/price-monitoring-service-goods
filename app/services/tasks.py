import asyncio
import time
import logging

from app.core.celery_app import celery_app
from app.database import async_session_factory
from app.repositories.product_repository import ProductRepository
from app.services.parser import get_product_price


logger = logging.getLogger(__name__)

@celery_app.task(name="update_product_price")
def update_product_price_task(product_id: int, url: str):
    """Задача для обновления цены продукта"""
    # Замеряем время старта
    start_time = time.perf_counter()

    # Запускаем асинхронный парсинг внутри синхронного Celery
    loop = asyncio.get_event_loop()
    price = loop.run_until_complete(_async_update_price(product_id, url))

    # Замеряем время окончания
    duration = time.perf_counter() - start_time
    print(f"--- Задача выполнена за {duration:.2f} сек. ---")
    logger.info(f"--- Задача ID {product_id} выполнена за {duration:.2f} сек. Цена: {price} ---")
    

async def _async_update_price(product_id: int, url: str):
    # Фабрика сессий
    async with async_session_factory() as db:
        repo = ProductRepository(db)

        # 2. Вызываем парсинг (из app/services/parser.py)
        # Если парсер вернет None, цена в базе останется прежней
        new_price = await get_product_price(url)

        if new_price is not None:
            await repo.update_price(product_id, new_price)
            print(f"!!! БАЗА ОБНОВЛЕНА: Товар {product_id}, цена {new_price}")
            return new_price
        
        logger.warning(f"Не удалось получить цену для товара {product_id}")
        return None   


