
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
import httpx

from pydantic import BaseModel, ConfigDict

from src.config import get_settings


app = FastAPI()

settings = get_settings()


class AuthorizationCodeSchema(BaseModel):
    code: str

    model_config = ConfigDict(extra='allow')


class AccessToken(BaseModel):
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


@app.get('/token')
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
            token = AccessToken(**dict(res.json()))
            await get_user_info(token.access_token)
        else:
            raise HTTPException(status_code=401, detail='Unauthorized')
    except Exception as e:
        print(e)

@app.get('/login_yandex')
async def login():
    url = f'https://oauth.yandex.ru/authorize?response_type=code&client_id={settings.yandex_client_id}'
    return RedirectResponse(f"{url}")


