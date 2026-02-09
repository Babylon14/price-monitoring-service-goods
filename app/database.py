from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings


# Используем URL из конфига
engine = create_async_engine(settings.async_database_url, echo=True)

# Создаем асинхронную фабрику сессии
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Функция для получения сессии
async def get_db():
    async with async_session_factory() as session:
        yield session

