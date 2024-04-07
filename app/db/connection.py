import sqlalchemy as sa
from settings import URL_DATABASE
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = sa.create_engine(URL_DATABASE, echo=False,
    pool_pre_ping=True,
    pool_timeout=20,
    pool_recycle=-1
)


# Crear una instancia de la clase base declarativa
#Base = declarative_base()

metadata = sa.MetaData()
conn = engine.connect()
#Session = sessionmaker(bind=engine)
