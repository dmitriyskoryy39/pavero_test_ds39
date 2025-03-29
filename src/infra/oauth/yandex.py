
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
import httpx

from pydantic import BaseModel, ConfigDict

from src.container import Container, init_container
from src.config import Settings


router = APIRouter()

container: Container = init_container()
settings: Settings = container.resolve(Settings)


class AuthorizationCodeSchema(BaseModel):
    code: str

    model_config = ConfigDict(extra='allow')


class AccessTokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int

    model_config = ConfigDict(extra='allow')


async def get_user_info(access_token: str):
    headers = {
        'Authorization': f'OAuth {access_token}'
    }
    async with httpx.AsyncClient() as client:
        res = await client.get(f'https://login.yandex.ru/info', headers=headers)
        print(f"{res.json()=}")


@router.get('/token')
async def set_token(
    code: AuthorizationCodeSchema = Depends()
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
            res = await client.post(f'https://oauth.yandex.ru/token', headers=headers, data=data)

        if res.status_code == 200:
            token = AccessTokenSchema(**dict(res.json()))
            await get_user_info(token.access_token)
        else:
            raise HTTPException(status_code=401, detail='Unauthorized')
    except Exception as e:
        print(e)

@router.get('/login_yandex')
async def login():
    url = f'https://oauth.yandex.ru/authorize?response_type=code&client_id={settings.yandex_client_id}'
    return RedirectResponse(f"{url}")

