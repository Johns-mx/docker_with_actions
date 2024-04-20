from fastapi import APIRouter, status, Depends
from core.middlewares.verify_token_routes import VerifyTokenRoute
from models.models import ResponseModel, UserCreate, UserFullModel, UserLogin, UserUpdate
from config.functions import response_modelx
from core.modules import UsersManagement
from config.queries import *
from sqlalchemy.orm import Session
from db.connection import get_db


users_route = APIRouter()
users_private_route = APIRouter(route_class=VerifyTokenRoute)


@users_route.post("/create", status_code=200)
async def create_user(user: UserCreate):
    """🗿ENDPOINT: Create a new user in the database."""
    try:
        query_response: ResponseModel = await query_insert_new_user(user)
        if query_response.error is True:
            return response_modelx(query_response.status, True, query_response.message, user)
        return response_modelx(status.HTTP_200_OK, False, "Usuario creado.", None)
    except:
        return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al crear el usuario.", None)


@users_route.post("/get", status_code=200)
async def get_user(user: UserLogin):
    """🗿ENDPOINT: Get user from the database by username."""
    try:
        query_response: ResponseModel = await query_get_full_user(user.username, user.password)
        if query_response.error is True:
            return response_modelx(query_response.status, True, query_response.message, None)
        
        return response_modelx(status.HTTP_200_OK, False, "Usuario encontrado.", query_response.res)
    except:
        return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al obtener el usuario.", None)


@users_route.put("/update", status_code=200)
async def update_user(user: UserUpdate):
    try:
        query_response: ResponseModel = await query_get_full_user(user.username, user.password)
        if query_response.error is True:
            return response_modelx(query_response.status, True, query_response.message, None)
        
        if await UsersManagement().config_user_is_blocked(query_response.res):
            return response_modelx(status.HTTP_400_BAD_REQUEST, True, "Usuario no activo / bloqueado.", None)
        
        query_response: ResponseModel = await query_update_user(user)
        if query_response.error is True:
            return response_modelx(query_response.status, True, query_response.message, None)
        
        return response_modelx(status.HTTP_200_OK, False, "Usuario actualizado exitosamente.", None)
    except:
        return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al actualizar el usuario.", None)


@users_route.get("/get_all_users", status_code=200)
async def get_all_users():
    """🗿ENDPOINT: Get all users from the database"""
    try:
        query_response: ResponseModel = await query_get_all_users()
        if query_response.error is True:
            return response_modelx(query_response.status, True, query_response.message, None)
        if not len(query_response.res) > 0:
            return response_modelx(status.HTTP_404_NOT_FOUND, True, "No hay usuarios registrados.", None)
        return response_modelx(status.HTTP_200_OK, False, "Todos los usuarios.", query_response.res)
    except:
        return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al obtener los usuarios.", None)
