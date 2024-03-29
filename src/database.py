from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, MetaData


from configs import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
Async_DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Синхронная сессия
engine = create_engine(DATABASE_URL, echo=True)
session_ = sessionmaker(bind=engine)

# Асинхронная сессия
async_engine = create_async_engine(Async_DATABASE_URL, echo=True)
async_session = async_sessionmaker(async_engine, class_=AsyncSession)


# Объявление базового класса
class Base(DeclarativeBase):
    pass


metadata = MetaData()
