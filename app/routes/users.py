from fastapi import APIRouter, status
from core.middlewares.verify_token_routes import VerifyTokenRoute
from core.security.functions import response_modelx
from models.models import UserInternalModel
from db.connection import engine
from db.models import users


users_route = APIRouter()


@users_route.post("/create", status_code=200)
async def create_user(user: UserInternalModel):
    try:
        with engine.connect() as conn:
            conn.execute(users.insert().values(username=user.username, password=user.password, email=user.email, full_name=user.full_name))
            conn.connection.commit()
            return response_modelx(status.HTTP_200_OK, False, "Usuario creado.", user.model_dump())
    except:
        return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Error al crear el usuario.", None)
