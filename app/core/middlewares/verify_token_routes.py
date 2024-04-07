from fastapi import Request, status
from fastapi.routing import APIRoute
from core.security.functions import response_modelx
from core.security.jwt import validate_access_token
from models.models import ResponseModel


class VerifyTokenRoute(APIRoute):
    """Verify Token Route"""
    def get_route_handler(self):
        original_route = super().get_route_handler()
    
        async def verify_token_middlewares(request: Request):
            """Verify token middlewares"""
            if 'Authorization' not in request.headers:
                return response_modelx(status.HTTP_401_UNAUTHORIZED, True, "No se ha proporcionado ningún token.", None)
            
            try:
                token = request.headers['Authorization'].split(" ")[1]
                response: ResponseModel = await validate_access_token(token)
                if response.res is not None:
                    return await original_route(request)
                else:
                    return response_modelx(status.HTTP_401_UNAUTHORIZED, True, "Token proporcionado invalido.", None)
            except Exception:
                return response_modelx(status.HTTP_500_INTERNAL_SERVER_ERROR, True, "Surgió un error al procesar el token, por favor vuelva a intentarlo en un momento.", None)
        
        return verify_token_middlewares
