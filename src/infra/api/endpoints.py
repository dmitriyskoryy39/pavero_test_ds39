
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    Query
)

from src.infra.services import (
    # RoleService,
    FileService
)

from src.infra.schemas import AudiofileRespSchema

from src.container import Container, init_container


router = APIRouter()


container: Container = init_container()

# RoleService = Annotated[RoleService, Depends(container.resolve(RoleService))]
FileService = Annotated[FileService, Depends(container.resolve(FileService))]


@router.post('/upload_file')
async def upload_file(
        uploaded_file: UploadFile,
        service: FileService,
        name: str = Query(description='Имя файла'),
):
    try:
        user_id = 1
        result = await service.upload(uploaded_file, name, user_id)
        return result
    except Exception:
        return HTTPException(status_code=400, detail='error upload')


@router.get(
    '/file_info',
    response_model=list[AudiofileRespSchema]
)
async def upload_file(
        user_id: int,
        service: FileService):
    try:
        result = await service.get(user_id)
        return result
    except Exception:
        return HTTPException(status_code=400, detail='error get file info')

