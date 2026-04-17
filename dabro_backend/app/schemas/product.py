from typing import Optional

from pydantic import BaseModel, Field


class ProductAddSchema(BaseModel):
    title: str
    excel_product_id: int
    brand: str | None
    category: str | None
    description: str | None
    cost: int = Field(ge=0)
    size: str | None
    img_url: str = None
    items_left: int = Field(ge=0)


class ProductSchema(ProductAddSchema):
    product_id: int = Field(ge=0)


class ProductDeleteSchema(BaseModel):
    product_id: int = Field(ge=0)


class ProductPatchSchema(ProductDeleteSchema):
    excel_product_id: Optional[int] = None
    title: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[int] = None
    size: Optional[str] = None
    img_url: Optional[str] = None
    items_left: Optional[int] = None
