
from fastapi import Request, HTTPException

from src.infra.oauth.yandex import get_user_info

from src.infra.schemas import UserLoginDTO


async def check_token_dep(request: Request):
    access_token = request.cookies.get('access_token', None)
    if not access_token:
        raise HTTPException(status_code=401, detail='Unauthorized')
    user_info = await get_user_info(access_token)
    if user_info.get('login'):
        return UserLoginDTO(**user_info)
    else:
        raise HTTPException(status_code=401, detail='Unauthorized')

