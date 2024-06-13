from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ..config import Config

engine = create_engine(Config.DATABASE_URL)

SessionLocal = scoped_session(sessionmaker(bind=engine))
