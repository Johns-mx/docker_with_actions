import sqlalchemy as sa
from settings import URL_DATABASE, URL_LOCAL_DATABASE
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = sa.create_engine(URL_LOCAL_DATABASE, echo=False,
    pool_pre_ping=True,
    pool_timeout=20,
    pool_recycle=-1
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#>> Crear una instancia de la clase base declarativa
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

