from sqlalchemy.orm import Session
from Back.repositories.repositories import RepositoryOrdenes, RepositoryClientes
from datetime import datetime
from typing import List
from Back.models.models import Orden, DetalleOrden

class ServiceOrdenes:
    def __init__(self, db: Session):
        self.db = db
        self.repo_ordenes = RepositoryOrdenes(db_session=db)
        self.repo_clientes = RepositoryClientes(db_session=db)

    def actualizar_estado(self, id_orden: int, nuevo_estado: str) -> int:
        """
        Cambia el estado de un pedido de acuerdo a los valores de la lista permitida de Streamlit
        """
        estados = ["Pendiente", "En proceso", "Empacado", "Entregado", "Devuelto por cambios"]
        if nuevo_estado not in estados:
            raise ValueError(f"Estado {nuevo_estado} no está permitido")
        else:
            estado_patch = {}
            estado_patch["estatus"] = nuevo_estado
            fila_afectada = self.repo_ordenes.actualizar_orden(id_orden=id_orden, atributos=estado_patch)
            return fila_afectada

    def actualizar_fecha_entrega(self, id_orden: int, nueva_fecha: str) -> int:
        """
        Actualiza la fecha de entrega (en formato texto) de acuerdo a un número de 
        """
        if not nueva_fecha:
            raise ValueError("La fecha no puede estar vacía")
        else:
            fecha = {}
            fecha["fecha_entrega"] = nueva_fecha
            fila_afectada = self.repo_ordenes.actualizar_orden(id_orden=id_orden, atributos=fecha)
            return fila_afectada

    def actualizar_deuda(self, id_orden: int) -> float:
        """
        Calcula la deuda mediante la diferencia entre el precio_total y la cantidad pagada
        """
        info_cliente = self.repo_ordenes.traer_info_orden(id_orden=id_orden)
        if not info_cliente:
            raise ValueError(f"El cliente con id_orden {id_orden} no existe en la Base de Datos")
        else:
            precio_cliente = info_cliente.precio_total
            pagado_cliente = info_cliente.pagado
            return max(0.0, precio_cliente-pagado_cliente)

    def actualizar_detalles_orden(self, id_detalle: int, detalle_nuevo: str, cantidad_nueva: int) -> int:
        detalles = {"detalle":detalle_nuevo, "cantidad": cantidad_nueva}
        fila_afectada = self.repo_ordenes.actualizar_detalle_orden(id_detalle=id_detalle, items=detalles)
        return fila_afectada

    def actualizar_nombre(self, id_orden: int, nuevo_nombre:str) -> int:
        info_orden = self.repo_ordenes.traer_info_orden(id_orden=id_orden)
        if not info_orden:
            raise ValueError("La orden no existe")
        id_del_cliente = info_orden.id_cliente
        atributos_cliente = {"nombre":nuevo_nombre}
        fila_afectada = self.repo_clientes.actualizar_nombre(id_cliente=id_del_cliente, nombre=atributos_cliente)
        return fila_afectada

    def actualizar_canal(self, id_orden: int, nuevo_canal: str) -> int:
        info_orden = self.repo_ordenes.traer_info_orden(id_orden=id_orden)
        if not info_orden:
            raise ValueError("La orden no existe")
        id_cliente = info_orden.id_cliente
        atributos_cliente = {"canal_entrada": nuevo_canal}
        fila_afectada = self.repo_clientes.actualizar_canal_entrada(id_cliente=id_cliente, canal=atributos_cliente)
        return fila_afectada

    def unir_columnas(self) -> List[dict]:
        ordenes = self.repo_ordenes.traer_ordenes()
        filas = []

        for orden in ordenes:
            orden:Orden
            deuda = max(0.0, orden.precio_total - orden.pagado)
            for detalle in orden.detalle_orden:
                detalle:DetalleOrden
                fila = {
                    "Id Orden": orden.id_orden,
                    "Id Cliente": orden.id_cliente,
                    "Cliente": orden.info_cliente.nombre,
                    "Teléfono": orden.info_cliente.telefono,
                    "Canal": orden.info_cliente.canal_entrada,
                    "Tipo de Pedido": orden.tipo_pedido,
                    "Estatus": orden.estatus,
                    "Fecha de Entrega": orden.fecha_entrega,
                    "Producto": detalle.producto,
                    "Detalle": detalle.detalle,
                    "Cantidad": detalle.cantidad,
                    "Pertenencia": detalle.pertenencia,
                    "Total": orden.precio_total,
                    "Pagado": orden.pagado,
                    "Deuda": deuda,
                    "Id detalles": detalle.id_detalle,
                    "Asignacion Orden": orden.asignacion,
                    "Asignacion Detalles": detalle.asignacion
                }
                filas.append(fila)
        return filas

    def actualizar_pago(self, id_orden: int, nuevo_pago: float) -> int:
        info_orden = self.repo_ordenes.traer_info_orden(id_orden=id_orden)
        if not info_orden:
            raise ValueError("La orden no existe")
        pago = {"pagado":nuevo_pago}
        fila_afectada = self.repo_ordenes.actualizar_orden(id_orden=id_orden, atributos=pago)
        return fila_afectada