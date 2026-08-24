from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Back.repositories.bd import get_db
from Back.services.services_metricas import ServiceMetricas
from Back.repositories.repositories import RepositoryOrdenes, RepositoryCatalogoProductos
from Back.utils.api_verification import verificar_api

router = APIRouter(prefix="/api/v1/metricas", tags=["Dashboard BI"], dependencies=[Depends(verificar_api)])

@router.get("/")
def obtener_metricas(db: Session = Depends(get_db)):
    try:
        servicio = ServiceMetricas(db=db)
        return servicio.obtener_kpis()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extrayendo los KPIs: {e}")