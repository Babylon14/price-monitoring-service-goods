from app.repositories.product_repository import ProductRepository
from app.schemas.schema_product import ProductCreate, ProductResponse


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

        # ЛОГИКА с вызовом Celery будет описана позже...
        # celery_app.send_task("parse_price", args=[product.id])

        return product


