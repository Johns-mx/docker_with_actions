from fastapi import status, Header
from fastapi import APIRouter
from models.models import ResponseModel, Token, UserModel, UserToJwtModel
from core.security.functions import response_modelx
from core.security.jwt import create_access_token, validate_access_token


auth_router = APIRouter()


@auth_router.post("/login")
async def auth_login(user: UserModel):
    username= user.username
    email= user.email
    user_jwt= UserToJwtModel(sub=username, email=email)
    if username=="johns_mx":
        token= await create_access_token(user_jwt.model_dump())
        return response_modelx(status.HTTP_200_OK, False, "Usuario autenticado.", token)
    return response_modelx(status.HTTP_400_BAD_REQUEST, True, "Usuario no autenticado.", None)


@auth_router.post("/verify_token")
async def auth_verify_token(Authorization: str = Header(None)):
    token= Authorization.split(" ")[1]
    response: ResponseModel = await validate_access_token(token)
    if response.error is True:
        return response_modelx(response.status, True, response.message, None)
    return response_modelx(status.HTTP_200_OK, False, "Usuario autorizado.", None)