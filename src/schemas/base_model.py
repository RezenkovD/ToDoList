from pydantic import BaseModel as BaseSchema


class BaseModel(BaseSchema):
    class Config:
        from_attributes = True
