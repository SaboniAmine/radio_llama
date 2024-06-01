from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

Base = declarative_base()

engine = create_engine(settings.db_url, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
