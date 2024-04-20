from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from core.security.auth import auth_router
from routes.movies import movies_route
from routes.users import users_route, users_private_route
from routes.memberships import membership_route
from config.functions import response_modelx
from routes.plans import plan_route
from models.models import VersionAPI


version= VersionAPI()


app = FastAPI()
app.title = f"API: Proyecto Github Actions v{version.major}"
app.description = "API con Fastapi + SqlAlchemy + Github Actions, por el curso de Github Actions en Platzi"
app.version = version.version


#>> Funcion para responder cuando el usuario ingrese una ruta invalida
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return response_modelx(status.HTTP_404_NOT_FOUND, True, "Ruta inválida / no definida.", None)


#>> Funcion para responder cuando faltan campos
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return response_modelx(status.HTTP_422_UNPROCESSABLE_ENTITY, True, "Inexistencia de campos.", None)


#Solucion CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#>> Routes
app.include_router(auth_router, prefix=f"/v{version.major}/api/auth", tags=["Authentication"])
app.include_router(movies_route, prefix=f"/v{version.major}/api/movies", tags=["Movies"])
app.include_router(users_route, prefix=f"/v{version.major}/api/user", tags=["Users"])
app.include_router(users_private_route, prefix=f"/v{version.major}/api/user", tags=["Users"])
app.include_router(membership_route, prefix=f"/v{version.major}/api/membership", tags=["Memberships"])
app.include_router(plan_route, prefix=f"/v{version.major}/api/plan", tags=["Plans"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000, reload=True)