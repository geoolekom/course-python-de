from datetime import datetime
from sqlalchemy import DateTime, String, ForeignKey
from storage.relational_db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(100))

    articles = relationship("ScientificArticle", back_populates="author")


class ScientificArticle(Base):
    __tablename__ = "scientific_articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    summary: Mapped[str] = mapped_column(String(200))
    file_path: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=True)
    author = relationship("Author", back_populates="articles")
