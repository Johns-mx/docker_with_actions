from fastapi import APIRouter, status, Depends
from core.middlewares.verify_token_routes import VerifyTokenRoute
from models.models import MembershipFull, ResponseModel, UserCreate, UserFullModel, UserLogin, UserUpdate
from config.functions import response_modelx
from core.modules import UsersManagement
from config.queries import *
from sqlalchemy.orm import Session
from db.connection import get_db


membership_route = APIRouter()


@membership_route.get("/get_all", status_code=200)
async def get_all_memberships():
    try:
        query_response: ResponseModel = await query_get_all_memberships()
        if query_response.error is True:
            return response_modelx(query_response.status, True, query_response.message, None)
        if not len(query_response.res) > 0:
            return response_modelx(status.HTTP_404_NOT_FOUND, True, "No hay membresias registradas.", None)
        return response_modelx(status.HTTP_200_OK, False, "Todas las membresias.", query_response.res)
    except:
        return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al obtener las membresias.", None)


@membership_route.post("/create", status_code=200)
async def create_membership(user: MembershipCreate):
    #try:
    query_response: ResponseModel = await query_get_full_user(user.username, user.password)
    if query_response.error is True:
        return response_modelx(query_response.status, True, query_response.message, None)
    
    if await UsersManagement().config_user_is_blocked(query_response.res):
        return response_modelx(status.HTTP_400_BAD_REQUEST, True, "Usuario no activo / bloqueado.", None)
    
    response: ResponseModel = await query_insert_new_membership(query_response.res)
    if response.error is True:
        return response_modelx(query_response.status, True, query_response.message, None)
    
    return response_modelx(status.HTTP_200_OK, False, "Membresia creada exitosamente.", response.res)
    #except:
        #return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al crear la membresia.", None)