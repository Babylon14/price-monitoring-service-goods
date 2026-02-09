from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import Optional
from datetime import datetime

# Общие поля
class ProductBase(BaseModel):
    name: str
    url: HttpUrl


# То, что присылает пользователь при создании
class ProductCreate(ProductBase):
    pass


# То, что мы отдаем пользователю
class ProductResponse(ProductBase):
    id: int
    current_price: Optional[float] = None
    last_updated: datetime


# Включаем режим совместимости с моделями SQLAlchemy
model_config = ConfigDict(from_attributes=True)

