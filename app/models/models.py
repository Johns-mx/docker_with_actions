from pydantic import BaseModel
from typing import Optional, Any


class ResponseModel(BaseModel):
    status: int
    error: bool= True
    message: str
    res: Any= None
    version: str= "v1.0.0"


class VersionAPI(BaseModel):
    version: str= "v1.0.0"
    major: int= 1
    minor: int= 0
    patch: int= 0


class Movie(BaseModel):
    id: int
    title: str
    year: Optional[int] = None


class User(BaseModel):
    user_id: int
    username: str
    password: str
    email: str
    full_name: str


class UserInternalModel(BaseModel):
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