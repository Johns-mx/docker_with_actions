from fastapi import APIRouter, status, Depends
from core.middlewares.verify_token_routes import VerifyTokenRoute
from models.models import ResponseModel, UserCreate, UserFullModel, UserLogin, UserUpdate
from config.functions import response_modelx
from core.modules import UsersManagement
from config.queries import *
from sqlalchemy.orm import Session
from db.connection import get_db


plan_route = APIRouter()


@plan_route.get("/get_all", status_code=200)
async def get_all_plans():
    try:
        query_response: ResponseModel = await query_get_all_plans()
        if query_response.error is True:
            return response_modelx(query_response.status, True, query_response.message, None)
        if not len(query_response.res) > 0:
            return response_modelx(status.HTTP_404_NOT_FOUND, True, "No existen planes registrados.", None)
        return response_modelx(status.HTTP_200_OK, False, "Todos los planes.", query_response.res)
    except:
        return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al obtener los planes.", None)
