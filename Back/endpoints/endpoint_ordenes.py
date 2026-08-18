from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from Back.repositories.bd import get_db
from Back.services.services_ordenes import ServiceOrdenes
from Back.repositories.repositories import RepositoryOrdenes
from Back.models.dtos_tipoa import OrdenResponse, DetalleOrdenResponse, OrdenRequest, DetalleOrdenRequest, PatchDetallesOrden, PatchEstadoOrden, PatchFechaEntrega, PatchNombre, PatchPago

router = APIRouter(prefix="/api/v1/ordenes", tags=["Gestión de pedidos"])

@router.get("/", response_model=List[OrdenResponse])
def traer_ordenes_endpoint(db: Session = Depends(get_db)):
    try:
        servicio = ServiceOrdenes(db=db)
        return servicio.unir_columnas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo órdenes: {e}")

@router.patch("/{id_orden}/estado")
def actualizar_estado_orden_endpoint(id_orden: int, payload: PatchEstadoOrden, db: Session = Depends(get_db)):
    try:
        servicio = ServiceOrdenes(db=db)
        filas = servicio.actualizar_estado(id_orden=id_orden, nuevo_estado=payload.nuevo_estado)
        if filas == 0:
            raise HTTPException(status_code=404, detail="La orden no existe")
        db.commit()
        return {"mensaje": "Estado actulizado con éxito"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{id_orden}/fecha_entrega")
def actualizar_fecha_entrega_endpoint(id_orden: int, payload: PatchFechaEntrega, db: Session = Depends(get_db)):
    try:
        servicio = ServiceOrdenes(db=db)
        fecha_actualizada = servicio.actualizar_fecha_entrega(id_orden=id_orden, nueva_fecha=payload.nueva_fecha)
        if fecha_actualizada == 0:
            raise HTTPException(status_code=404, detail="La orden no existe")
        db.commit()
        return {"mensaje": "Fecha de entrega actualizada con éxito"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{id_orden}/nombre")
def actualizar_nombre_endpoint(id_orden: int, payload: PatchNombre, db: Session = Depends(get_db)):
    try:
        servicio = ServiceOrdenes(db=db)
        nuevo_nombre = servicio.actualizar_nombre(id_orden=id_orden, nuevo_nombre=payload.nuevo_nombre)
        if nuevo_nombre == 0:
            raise HTTPException(status_code=404, detail="La orden no existe")
        db.commit()
        return {"mensaje": "Nombre del cliente actualizado con éxito"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/detalles/{id_detalle}")
def actualizar_detalle_orden(id_detalle: int, payload: PatchDetallesOrden, db: Session = Depends(get_db)):
    try:
        servicio = ServiceOrdenes(db=db)
        nuevo_detalle = servicio.actualizar_detalles_orden(
            id_detalle=id_detalle,
            detalle_nuevo=payload.nuevo_detalle,
            cantidad_nueva=payload.cantidad
        )
        if nuevo_detalle == 0:
            raise HTTPException(status_code=404, detail="No existe detalle para la orden")
        db.commit()
        return {"mensaje":"Detalle actualizado con éxito"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{id_orden}/pago")
def actualizar_pago_endpoint(id_orden: int, payload: PatchPago, db: Session = Depends(get_db)):
    try:
        servicio = ServiceOrdenes(db=db)
        nuevo_pago = servicio.actualizar_pago(id_orden=id_orden, nuevo_pago=payload.pago)
        if nuevo_pago == 0:
            raise HTTPException(status_code=404, detail="La orden no existe")
        db.commit()
        nueva_deuda = servicio.actualizar_deuda(id_orden=id_orden)
        return {"mensaje":"Pago actualizado con éxito","deuda": nueva_deuda}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))