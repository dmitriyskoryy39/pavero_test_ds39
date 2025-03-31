
from pydantic import BaseModel, ConfigDict


class UserLoginDTO(BaseModel):
    id: str
    login: str
    client_id: str
    display_name: str
    real_name: str
    first_name: str
    last_name: str
    sex: str
    psuid: str


class UserSchema(BaseModel):
    id: int
    username: str


class RoleAddSchema(BaseModel):
    role: str


class RoleSchema(RoleAddSchema):
    id: int


class AudiofileRespSchema(BaseModel):
    id: int
    title: str
    path: str


class AccessTokenSchemaDTO(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int

    model_config = ConfigDict(extra='ignore')


class AuthorizationCodeSchema(BaseModel):
    code: str

    model_config = ConfigDict(extra='ignore')