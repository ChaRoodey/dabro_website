from typing import Optional

from pydantic import BaseModel, Field


class ProductAddSchema(BaseModel):
    excel_product_id: int
    brand: str
    category: str
    description: str
    cost: int = Field(ge=0)
    size: str
    img_id: str
    items_left: int = Field(ge=0)


class ProductSchema(ProductAddSchema):
    product_id: int = Field(ge=0)


class ProductDeleteSchema(BaseModel):
    product_id: int = Field(ge=0)


class ProductPatchSchema(ProductDeleteSchema):
    excel_product_id: Optional[int] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[int] = None
    size: Optional[str] = None
    img_id: Optional[str] = None
    items_left: Optional[int] = None
