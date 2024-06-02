import uvicorn
from fastapi import FastAPI

from llamapi.container import ServerContainer
from llamapi.routers import users, programs


def create_app() -> FastAPI:
    container = init_container()

    init_db(container)
    server = init_server(container)
    return server


def init_container():
    container = ServerContainer()
    container.wire(
        modules=[
            users,
            programs
        ]
    )
    return container


def init_db(container):
    db = container.db()
    db.create_database()


def init_server(container):
    server = FastAPI()
    server.container = container
    server.include_router(users.router)
    server.include_router(programs.router)
    return server


app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        'llamapi.main:app',
        host='0.0.0.0',
    )
