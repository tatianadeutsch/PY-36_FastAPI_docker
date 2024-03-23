from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, Annotated

from src.database import Base, engine

intpk = Annotated[int, mapped_column(primary_key=True)]


class Documents(Base):
    __tablename__ = "documents"

    id: Mapped[intpk]
    path: Mapped[str] = mapped_column(unique=True)
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=True)

    doc_text_: Mapped["Documents_text"] = relationship(
        back_populates="orders__emp", uselist=False
    )


class Documents_text(Base):
    __tablename__ = "documents_text"

    id: Mapped[intpk]
    id_doc: Mapped[int] = mapped_column(ForeignKey(Documents.id))
    text: Mapped[str]

    orders__emp: Mapped["Documents"] = relationship(back_populates="doc_text_")


# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
