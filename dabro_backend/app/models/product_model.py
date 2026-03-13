from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class ProductModel(Base):
    __tablename__ = 'product'

    product_id: Mapped[int] = mapped_column(primary_key=True)
    excel_product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    brand: Mapped[str] = mapped_column(String(30), nullable=True)
    category: Mapped[str] = mapped_column(String(30), nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    size: Mapped[str] = mapped_column(String, nullable=True)
    img_url: Mapped[str] = mapped_column(Text, nullable=True)
    items_left: Mapped[int] = mapped_column(Integer, nullable=False)
