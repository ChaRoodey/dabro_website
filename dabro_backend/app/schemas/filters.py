from typing import Annotated
from fastapi import Query, HTTPException
from pydantic import BaseModel, Field, model_validator, ValidationError


class FiltersSchema(BaseModel):
    brands: list[str] | None = None
    categories: list[str] | None = None
    min_price: int | None = Field(default=None, ge=0)
    max_price: int | None = Field(default=None, ge=0)

    # @model_validator(mode="after")
    # def check_price_range(self):
    #     if (
    #             self.min_price is not None
    #             and self.max_price is not None
    #             and self.min_price > self.max_price
    #     ):
    #         raise ValidationError("min_price cannot be greater than max_price")
    #     return self


def filters_query(
        brands: Annotated[list[str] | None, Query()] = None,
        categories: Annotated[list[str] | None, Query()] = None,
        min_price: Annotated[int | None, Query(ge=0)] = None,
        max_price: Annotated[int | None, Query(ge=0)] = None,
) -> FiltersSchema:
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=422,
            detail={
                "field": "price",
                "message": "Минимальная цена не может быть больше максимальной"
            }
        )

    return FiltersSchema(
        brands=brands,
        categories=categories,
        min_price=min_price,
        max_price=max_price,
    )
