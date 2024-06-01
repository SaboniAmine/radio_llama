from dependency_injector import containers, providers
from fastapi.security import OAuth2AuthorizationCodeBearer
from fief_client import FiefAsync
from fief_client.integrations.fastapi import FiefAuth

from api.config import settings
from api.database import Database
from api.services.auth import AuthService


class ServerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    db_url = settings.db_url
    db = providers.Singleton(
        Database,
        db_url=config.db_url,
    )
    