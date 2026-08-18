from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Back.repositories.bd import get_db
from Back.repositories.repositories import RepositoryOrdenes
from Back.models.dtos_tipoa import OrdenResponse, DetalleOrdenResponse

router = APIRouter(prefix="/api/v1/ordenes", tags=["Gestión de pedidos"])

@router.get("/", response_model=List[OrdenResponse])
def traer_ordenes_endpoint(db: Session = Depends(get_db)):
    try:
        repo_ordenes = RepositoryOrdenes(db)
        lista_ordenes = repo_ordenes.traer_ordenes()
        return lista_ordenes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las órdenes: {e}")