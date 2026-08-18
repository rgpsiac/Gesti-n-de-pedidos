from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Back.repositories.bd import get_db
from Back.models.dtos_tipob import DTOBSheets
from Back.orquestadores.orquestador_kits import OrquestadorPipelineKits
import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)
def verificar_api_key(api_key: str = Security(api_key_header)):
    llave = os.getenv("API_SECRET_KEY")
    if api_key != llave:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado: API Key inválida"
        )
    return api_key


router = APIRouter(prefix="/api/v1/pipeline_sheets_kits", tags=["Integraciones"])

@router.post("/sheets")
def recibir_webhook_kits(payload: DTOBSheets, db: Session = Depends(get_db), api_key: str = Depends(verificar_api_key)):
    try:
        orquestador = OrquestadorPipelineKits(db=db)
        orquestador.procesar_pedido(payload)
        return {"mensaje":"Pedido guardado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el webhook: {str(e)}")