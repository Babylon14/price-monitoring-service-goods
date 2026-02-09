from app.repositories.product_repository import ProductRepository
from app.schemas.schema_product import ProductCreate, ProductResponse


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    
    async def create_new_monitor(self, product_data: ProductCreate) -> ProductResponse:
        """Метод для бизнес-логики создания продукта"""

        # 1. Проверяем дубликаты через репозиторий
        existing = await self.repository.get_by_url(str(product_data.url))
        if existing:
            return None  # Такой продукт уже существует

        # 2. Сохраняем продукт 
        product = await self.repository.create(**product_data.model_dump())

        # 3. ЛОГИКА с вызовом Celery будет описана позже...
        # celery_app.send_task("parse_price", args=[product.id])

        return product


