
from pydantic import BaseModel


class RoleAddSchema(BaseModel):
    role: str


class RoleSchema(RoleAddSchema):
    id: int

