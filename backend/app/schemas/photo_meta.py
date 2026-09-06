from pydantic import BaseModel


class PhotoMetaSchema(BaseModel):
    id: int
    index: int
