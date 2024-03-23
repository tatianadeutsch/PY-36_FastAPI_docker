from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, MetaData, NullPool
from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

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

    # def __repr__(self):
    #     cols = []
    #     for idx, col in enumerate(self.__table__.columns.keys()):
    #         if col in self.repr_cols or idx < self.repr_cols_num:
    #             cols.append(f"{col}={getattr(self, col)}")
    #
    #     return f'<{self.__class__.__name__} {", ".join(cols)}>'


metadata = MetaData()
