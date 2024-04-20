from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime


class VersionAPI(BaseModel):
    version: str= "v1.1.1"
    major: int= 1
    minor: int= 1
    patch: int= 1

version= VersionAPI()


#region: Users
@dataclass
class UserDataInternal:
    user_id: Optional[int]= None
    username: Optional[str]= None
    email: Optional[str]= None
    full_name: Optional[str]= None


class ResponseModel(BaseModel):
    status: int
    error: bool= True
    message: str= ""
    res: Optional[Any] = None
    version: Optional[str]= version.version


class Movie(BaseModel):
    id: int
    title: str
    year: Optional[int] = None


class User(BaseModel):
    user_id: Optional[int]= None
    username: Optional[str]= None
    password: Optional[str]= None
    email: Optional[str]= None
    full_name: Optional[str]= None


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    full_name: str


class UserModel(BaseModel):
    username: str
    email: str


class UserToJwtModel(BaseModel):
    sub: Optional[str] = None
    email: Optional[str]= None


class Token(BaseModel):
    token: str


class UserUpdate(UserLogin):
    full_name: Optional[str]= None
    phone: Optional[str]= None
    language: Optional[str]= None
    country: Optional[str]= None
    address: Optional[str]= None
    membership: Optional[str]= None


class UserUpdateInternal(BaseModel):
    full_name: Optional[str]= None
    phone: Optional[str]= None
    language: Optional[str]= None
    country: Optional[str]= None
    address: Optional[str]= None
    membership: Optional[str]= None


class UserFullModel(BaseModel):
    user_id: Optional[int]= None
    username: Optional[str]= None
    email: Optional[str]= None
    full_name: Optional[str]= None
    phone: Optional[str]= None
    language: Optional[str]= None
    country: Optional[str]= None
    address: Optional[str]= None
    membership: Optional[str]= None
    invoices: Optional[str]= None
    created_at: Optional[str]= None
    updated_at: Optional[str]= None
    block: Optional[bool]= None
    code_tmp: Optional[str]= None
#endregion


#region: Enums
class eTypePlan(Enum):
    STANDARD= 1
    PREMIUM= 2
    ULTIMATE= 3

class eMembershipStatus(Enum):
    ACTIVO= 1
    SUSPENDIDO= 2
    CANCELADO= 3

class ePaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CRYPTO = "crypto"
#endregion



#region: Membership
class MembershipFull(BaseModel):
    membership_id: Optional[int] = None
    user_id: Optional[int] = None
    plan_id: Optional[int] = None
    status: Optional[int] = None
    payment_method: Optional[str] = None
    billing_information: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MembershipCreate(UserLogin):
    payment_method: Optional[ePaymentMethod] = None
