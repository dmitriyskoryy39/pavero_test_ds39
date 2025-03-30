
from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: int
    username: str
    role_id: int


class RoleAddSchema(BaseModel):
    role: str


class RoleSchema(RoleAddSchema):
    id: int


class AudiofileRespSchema(BaseModel):
    id: int
    title: str
    path: str


class AccessTokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int

    model_config = ConfigDict(extra='ignore')