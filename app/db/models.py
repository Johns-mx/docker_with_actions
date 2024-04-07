from db.connection import engine, metadata
from sqlalchemy import Table, Column, String, Integer, ForeignKey


users = Table(
    "users", metadata,
    Column('user_id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True),
    Column('username', String(100), nullable=False),
    Column('password', String(100), nullable=True),
    Column('email', String(100), nullable=True),
    Column('full_name', String(100), nullable=True)
)


devs = Table(
    "dev_keys", metadata,
    Column('dev_id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True),
    Column('user_id', Integer, ForeignKey('users.user_id'), nullable=False),
    Column('username', String(100), nullable=False),
    Column('permission', String(100), nullable=True),
    Column('public_key', String(250), nullable=True),
    Column('private_key', String(250), nullable=True)
)


#>> Crear la tabla en la base de datos
metadata.create_all(engine)


"""class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    full_name = Column(String(100), nullable=True)


class DevKeys(Base):
    __tablename__ = "dev_keys"
    dev_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    username = Column(String(100), nullable=False)
    permission = Column(String(100), nullable=True)
    public_key = Column(String(250), nullable=True)
    private_key = Column(String(250), nullable=True)
    
#Base.metadata.create_all(engine)
"""
