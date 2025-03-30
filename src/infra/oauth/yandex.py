import httpx

from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import RedirectResponse

from pydantic import BaseModel, ConfigDict

from src.container import Container, init_container
from src.config import Settings
#
from src.infra.services import LoginService


router = APIRouter()

container: Container = init_container()
settings: Settings = container.resolve(Settings)

LoginService = Annotated[LoginService, Depends(container.resolve(LoginService))]


class AuthorizationCodeSchema(BaseModel):
    code: str

    model_config = ConfigDict(extra='ignore')


class AccessTokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int

    model_config = ConfigDict(extra='ignore')


async def get_user_info(access_token: str):
    headers = {
        'Authorization': f'OAuth {access_token}'
    }
    async with httpx.AsyncClient() as client:
        res = await client.get(f'{settings.yandex_user_info}', headers=headers)
        return res.json()


@router.get('/token', include_in_schema=False)
async def set_token(
    response: Response,
    service: LoginService,
    code: AuthorizationCodeSchema = Depends(),
):
    try:
        data = {
            'grant_type': 'authorization_code',
            'code': code.code,
            'client_id': settings.yandex_client_id,
            'client_secret': settings.yandex_client_secret
        }

        headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(f'{settings.yandex_token}', headers=headers, data=data)

        if res.status_code == 200:
            token = AccessTokenSchema(**dict(res.json()))
            user = await get_user_info(token.access_token)
            service.update(user.get('login'), token)
            response.set_cookie(key='access_token', value=token.access_token, httponly=True)
        else:
            raise HTTPException(status_code=401, detail='Unauthorized')
    except Exception as e:
        print(e)


@router.get('/login_yandex', include_in_schema=False)
async def login():
    url = f'{settings.yandex_authorize}{settings.yandex_client_id}'
    return RedirectResponse(f"{url}")


@router.get('/check_token', include_in_schema=False)
async def check_token(access_token: str):
    res = await get_user_info(access_token)
    return res

