from fastapi import status, Header
from fastapi import APIRouter
from models.models import ResponseModel, Token, UserModel, UserToJwtModel, UserLogin
from config.functions import response_modelx
from core.security.jwt import create_access_token, validate_access_token
from config.queries import *


auth_router = APIRouter()


@auth_router.post("/login")
async def auth_login(user: UserLogin):
    query_response: ResponseModel = await query_authenticate_user(user.username, user.password)
    if query_response.error is True:
        return response_modelx(status.HTTP_400_BAD_REQUEST, True, "Usuario no autenticado.", None)
    
    user_jwt= UserToJwtModel(sub=user.username, email=query_response.res.email)
    token= await create_access_token(user_jwt.model_dump())
    return response_modelx(status.HTTP_200_OK, False, "Usuario autenticado.", token)


@auth_router.get("/verify_token")
async def auth_verify_token(Authorization: str = Header(None)):
    if not Authorization:
        return response_modelx(status.HTTP_401_UNAUTHORIZED, True, "No se ha proporcionado ningún esquema 'Authorization'.", None)
    token= Authorization.split(" ")[1]
    response: ResponseModel = await validate_access_token(token)
    if response.error is True:
        return response_modelx(response.status, True, response.message, None)
    return response_modelx(status.HTTP_200_OK, False, "Usuario autorizado.", None)