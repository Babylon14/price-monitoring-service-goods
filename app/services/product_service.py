from app.repositories.product_repository import ProductRepository
from app.schemas.schema_product import ProductCreate, ProductResponse
from app.services.tasks import update_product_price_task


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    
    async def create_new_monitor(self, product_data: ProductCreate) -> ProductResponse:
        """Метод для бизнес-логики создания продукта"""

        clean_data = product_data.model_dump(mode="json") # Преобразуем в словарь

        # Проверяем дубликаты через репозиторий
        existing = await self.repository.get_by_url(clean_data["url"])
        if existing:
            return None  # Такой продукт уже существует

        # Сохраняем продукт 
        product = await self.repository.create(**clean_data)

        # Отправляем задачу в Celery (не ждем выполнения!)
        update_product_price_task.delay(product.id)
        return product


