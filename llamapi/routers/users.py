from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from fief_client import FiefAccessTokenInfo
from sqlalchemy.orm import Session

from config import settings
from schemas import schemas
from services.auth_service import AuthService

auth_service = AuthService(settings=settings)

router = APIRouter()


@router.get("/user")
@inject
async def get_user(
        access_token_info: FiefAccessTokenInfo = Depends(auth_service.authenticated()),
):
    return access_token_info


@router.post("/register")
@inject
def register_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(models.User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password =get_hashed_password(user.password)

    new_user = models.User(username=user.username, email=user.email, password=encrypted_password )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message":"user created successfully"}
