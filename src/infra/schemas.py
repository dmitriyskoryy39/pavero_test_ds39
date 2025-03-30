
from pydantic import BaseModel, ConfigDict


class RoleAddSchema(BaseModel):
    role: str


class RoleSchema(RoleAddSchema):
    id: int


class AudiofileRespSchema(BaseModel):
    id: int
    title: str
    path: str
