from typing import Optional

from pydantic import BaseModel, Field


class StaffAddSchema(BaseModel):
    name: str
    grade: str
    description: str
    img_url: Optional[str] = None


class StaffSchema(StaffAddSchema):
    staff_id: int = Field(ge=0)


class StaffDeleteSchema(BaseModel):
    staff_id: int = Field(ge=0)


class StaffPatchSchema(StaffDeleteSchema):
    name: Optional[str] = None
    grade: Optional[str] = None
    description: Optional[str] = None
    img_url: Optional[str] = None
