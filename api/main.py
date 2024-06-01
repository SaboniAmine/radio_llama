from dependency_injector.wiring import Provide, inject

from api.config import settings
from fastapi import Depends, FastAPI, APIRouter
from fief_client import FiefAccessTokenInfo

from api.container import ServerContainer
from api.routers import users
from api.services.auth import AuthService


def create_app() -> FastAPI:
    container = init_container()

    init_db(container)
    server = init_server(container)
    # server.add_exception_handler(DBException, db_exception_handler)
    # server.add_exception_handler(ValidationError, validation_exception_handler)
    # server.add_exception_handler(Exception, generic_exception_handler)

    return server


def init_container():
    container = ServerContainer()
    container.wire(
        modules=[
            # emissions,
            # runs,
            # experiments,
            # projects,
            # teams,
            # organizations,
            users,
            # authenticate,
        ]
    )
    return container


def init_db(container):
    db = container.db()
    db.create_database()
    # sql_models.Base.metadata.create_all(bind=engine)


def init_server(container):
    server = FastAPI()
    server.container = container
    server.include_router(users.router)
    return server


app = create_app()
