from typing import Any
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    
    id: Any
    __name__: str

    # Автоматическое определение имени таблицы
    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

