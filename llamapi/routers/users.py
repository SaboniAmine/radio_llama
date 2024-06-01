from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fief_client import FiefAccessTokenInfo

from config import settings
from services.auth import AuthService

auth_service = AuthService(settings=settings)

router = APIRouter()


@router.get("/user")
@inject
async def get_user(
        access_token_info: FiefAccessTokenInfo = Depends(auth_service.authenticated()),
):
    return access_token_info
