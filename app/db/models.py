from db.connection import engine, Base
from sqlalchemy import DECIMAL, Boolean, Column, String, Integer, ForeignKey, DATETIME, TIMESTAMP


class User(Base):
    __tablename__ = "users"
    user_id = Column("user_id", Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    username = Column("username", String(65), nullable=False)
    password = Column("password", String(100), nullable=True)
    email = Column("email", String(65), nullable=False)
    full_name = Column("full_name", String(100), nullable=True)
    phone = Column("phone", String(20), nullable=True)
    language = Column("language", String(20), nullable=True)
    country = Column("country", String(20), nullable=True)
    address = Column("address", String(100), nullable=True)
    membership = Column("membership", String(20), nullable=True)
    invoices = Column("invoices", String(100), nullable=True)
    created_at = Column("created_at", TIMESTAMP, nullable=True)
    updated_at = Column("updated_at", TIMESTAMP, nullable=True)
    block = Column("block", Boolean, nullable=True)
    code_tmp = Column("code_tmp", String(10), nullable=True)


class DevKeys(Base):
    __tablename__ = "dev_keys"
    dev_id = Column("dev_id", Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    user_id = Column("user_id", Integer, ForeignKey('users.user_id'), nullable=False)
    username = Column("username", String(100), nullable=False)
    permission = Column("permission", String(100), nullable=True)
    public_key = Column("public_key", String(250), nullable=True)
    private_key = Column("private_key", String(250), nullable=True)


class Membership(Base):
    __tablename__ = "memberships"
    membership_id = Column("membership_id", Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    user_id = Column("user_id", Integer, ForeignKey('users.user_id'), nullable=False)
    plan_id = Column("plan_id", Integer, ForeignKey('plans.plan_id'), nullable=False)
    status = Column("status", Integer, nullable=True)
    payment_method = Column("payment_method", String(100), nullable=True)
    billing_information = Column("billing_information", String(100), nullable=True)
    created_at = Column("created_at", TIMESTAMP, nullable=True)
    updated_at = Column("updated_at", TIMESTAMP, nullable=True)


class Plan(Base):
    __tablename__ = "plans"
    plan_id = Column("plan_id", Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name = Column("name", String(100), nullable=False)
    description = Column("description", String(100), nullable=True)
    price = Column("price", DECIMAL(10, 2), nullable=True)
    max_streams = Column("max_streams", Integer, nullable=True)
    max_devices = Column("max_devices", Integer, nullable=True)
    created_at = Column("created_at", TIMESTAMP, nullable=True)
    updated_at = Column("updated_at", TIMESTAMP, nullable=True)


Base.metadata.create_all(engine)
