from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Back.repositories.bd import get_db
from Back.models.dtos_tipob import DTOBSheets
from Back.orquestadores.orquestador_kits import OrquestadorPipelineKits
from fastapi import HTTPException, status
from Back.utils.api_verification import verificar_api


router = APIRouter(prefix="/api/v1/pipeline_sheets_kits", tags=["Integraciones"], dependencies=[Depends(verificar_api)])

@router.post("/sheets")
def recibir_webhook_kits(payload: DTOBSheets, db: Session = Depends(get_db)):
    try:
        orquestador = OrquestadorPipelineKits(db=db)
        orquestador.procesar_pedido(payload)
        return {"mensaje":"Pedido guardado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el webhook: {str(e)}")