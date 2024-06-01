from dependency_injector import containers, providers

from config import settings
from database import Database


class ServerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    db_url = settings.db_url
    db = providers.Singleton(
        Database,
        db_url=config.db_url,
    )
