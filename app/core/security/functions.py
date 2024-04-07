from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.models import VersionAPI


version = VersionAPI()


#>> Metodo para enviar respuesta 200, 300, 400, 500 ~
def response_modelx(status_code, error: bool, message: str, res, headers=None):
    """[method]: Devuelve un JSONResponse en cada solicitud a la API, para mostrar la respuesta al usuario."""
    response_headers = {"Content-Type": "application/json"}
    if headers:
        response_headers.update(headers)

    return JSONResponse(
        status_code=status_code,
        headers=response_headers,
        content=jsonable_encoder({
            "error": error,
            "message": message,
            "res": res,
            "version": version.version
        }),
    )