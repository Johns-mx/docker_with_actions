from fastapi import APIRouter, status
from core.middlewares.verify_token_routes import VerifyTokenRoute
from config.functions import response_modelx


movies_route = APIRouter(route_class=VerifyTokenRoute)


movies_list = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Accion"
    }
]


@movies_route.get("/get_movie/{id}", tags=["Movies"])
def get_movie(id: int):
    #movie= next(movie for movie in movies_list if movie["id"] == id)
    for movie in movies_list:
        if movie["id"] == id:
            return movie
    return None


@movies_route.get("/all", tags=["Movies"])
def get_all_movies():
    return response_modelx(status.HTTP_200_OK, False, "Todas las peliculas", movies_list)


@movies_route.get("/by_category/{category}", tags=["Movies"])
def get_movie_by_category(category: str):
    return [movie for movie in movies_list if movie["category"] == category]