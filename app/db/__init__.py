from sqlmodel import create_engine
from app.config import Config
from sqlalchemy.orm import sessionmaker
from app.db.session import CustomSession


db_url = f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"

engine = create_engine(db_url, echo=Config.DB_LOGGING)


CustomSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=CustomSession
)


def get_session():
    with CustomSessionLocal() as db_session:
        yield db_session
