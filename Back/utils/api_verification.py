from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_SECRET_KEY")
header = APIKeyHeader(name="X-API-Key", auto_error=False)
def verificar_api(api_key_header: str = Security(header)):
    if not api_key:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error de configuración del servidor. Falta API_KEY")
    if api_key_header != api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado"
        )
    return api_key_header