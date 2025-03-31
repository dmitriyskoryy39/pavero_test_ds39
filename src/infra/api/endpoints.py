
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    Query
)

from src.infra.services import (
    FileService
)

from src.infra.schemas import UserLoginDTO

from src.infra.api.dependencies import check_token_dep

from src.container import Container, init_container


router = APIRouter()


container: Container = init_container()

FileService = Annotated[FileService, Depends(container.resolve(FileService))]


@router.post('/upload_file')
async def upload_file(
    uploaded_file: UploadFile,
    service: FileService,
    name: str = Query(description='Имя файла'),
    user: UserLoginDTO = Depends(check_token_dep)
):
    try:
        result = await service.upload(uploaded_file, name, user)
        return result
    except Exception:
        return HTTPException(status_code=400, detail='error upload')


@router.get(
    '/file_info',
)
async def upload_file(
    service: FileService,
    user: UserLoginDTO = Depends(check_token_dep)
):
    try:
        result = await service.get(user)
        return result
    except Exception:
        return HTTPException(status_code=400, detail='error get file info')

