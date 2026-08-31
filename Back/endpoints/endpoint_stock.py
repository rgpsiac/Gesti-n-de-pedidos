from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Back.repositories.bd import get_db
from Back.repositories.repositories import RepositoryCatalogoProductos, RepositoryOrdenes
from Back.orquestadores.orquestador_stock import OrquestadorStock
from Back.models.dtos_tipob import DTOBInventarios
from Back.utils.api_verification import verificar_api
import traceback

router = APIRouter(prefix="/api/v1/inventarios", tags=["Gestión de inventario"], dependencies=[Depends(verificar_api)])

@router.post("/")
def agregar_inventario_endpoint(payload: DTOBInventarios, db: Session = Depends(get_db)):
    try:
        orquestador = OrquestadorStock(db=db)

        orquestador.procesar_stock(dto_inventario=payload)

        orquestador.asignar_items()

        return {"mensaje":"Actualización exitosa"}

    except Exception as e:
        error_msg = traceback.format_exc()

        raise HTTPException(status_code=500, detail=f"Error procesando los datos: {str(e)}")

@router.get("/")
def traer_catalogo_productos_endpoint(db: Session = (Depends(get_db))):
    try:
        orquestador = RepositoryCatalogoProductos(db_session=db)
        operacion = orquestador.traer_stock()
        return operacion
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante la query: {e}")