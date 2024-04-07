import uvicorn
from fastapi import FastAPI
from core.security.auth import auth_router
from routes.movies import movies_route
from routes.users import users_route 
from models.models import VersionAPI


version= VersionAPI()


app = FastAPI()
app.title = f"API: Proyecto Github Actions - {version.major}"
app.description = "API del curso de Github Actions en Platzi"
app.version = version.version


#>> Routes
app.include_router(auth_router, prefix=f"/v{version.major}/api/auth", tags=["Authentication"])
app.include_router(movies_route, prefix=f"/v{version.major}/api/movies", tags=["Movies"])
app.include_router(users_route, prefix=f"/v{version.major}/api/users", tags=["Users"])


if __name__ == "__main__":
    uvicorn.run(app, port=8000, reload=False)