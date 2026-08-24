from sqlalchemy.orm import Session
from sqlalchemy import func, case
from Back.models.dtos_tipoa import ClienteRequest, OrdenRequest, DetalleOrdenRequest, DetalleOrdenResponse, OrdenResponse, InventarioRequest, ItemsAsignadosPost
from Back.models.dtos_tipob import DTOBInventarios
from Back.models.models import Cliente, Orden, DetalleOrden, CatalogoProducto, CatalogoPedido, Inventario, ItemsAsignados
from typing import List

# Este archivo almacena las clases que se emplearán en el pipeline de google sheets
# Los patrones de estas clases son Repository.
# Cualquiera de estos Repository se conectará directamente con la bd
# Cualquiera de estas clases recibe como parámetro una clase DTO correspondiente
# con la tabla del ERD (por ejemplo, la tabla cliente tiene 3 DTOs, base, request, response)
# En este archivo se encuentran las clases: RepositoryClientes, RepositoryDetalles_orden y RepositoryOrdenes

class RepositoryClientes():
    def __init__(self, db_session: Session):
                self.db = db_session

    def crear_cliente(self, datos_cliente: ClienteRequest):
        datos_dict = datos_cliente.model_dump()
        nuevo_cliente = Cliente(**datos_dict)
        self.db.add(nuevo_cliente)
        self.db.flush()
        self.db.refresh(nuevo_cliente)
        return nuevo_cliente

    def listar_clientes(self):
        return self.db.query(Cliente).all()

    def ver_cliente(self, id_buscado):
        return self.db.query(Cliente).filter(Cliente.id_cliente == id_buscado).first()

    def actualizar_nombre(self, id_cliente: int, nombre: dict):
        fila_afectada = self.db.query(Cliente).filter(
            Cliente.id_cliente == id_cliente
        ).update(nombre)
        return fila_afectada

    def actualizar_canal_entrada(self, id_cliente: int, canal: dict):
        fila_afectada = self.db.query(Cliente).filter(
            Cliente.id_cliente == id_cliente
        ).update(canal)
        return fila_afectada


class RepositoryOrdenes():
    def __init__(self, db_session: Session):
        self.db = db_session
    def crear_orden(self, datos_orden: OrdenRequest):
        nueva_orden = Orden(**datos_orden.model_dump())
        self.db.add(nueva_orden)
        self.db.flush()
        self.db.refresh(nueva_orden)
        return nueva_orden
    def crear_detalle_orden(self, detalle_orden: DetalleOrdenRequest):
        detalles = DetalleOrden(**detalle_orden.model_dump())
        self.db.add(detalles)
        self.db.flush()
    def traer_ordenes(self) -> List[OrdenResponse]:
        """
        Este método hace una query a la bd para devolver la información sobre la orden, tal como fecha de entrega, pagado, deuda, tipo de pedido, etc.
        """
        return self.db.query(Orden).all()
    def traer_info_orden(self, id_orden: int):
        return self.db.query(Orden).filter(
            Orden.id_orden == id_orden
        ).first()
    def traer_detalle_orden(self, id_orden: int):
        """
        Este método hace una query a la bd para devolver la información detallada de la orden con base en un id_orden, tal como los productos incluidos, sus detalles y cantidades.
        """
        return self.db.query(DetalleOrden).filter(
            DetalleOrden.id_orden == id_orden
        ).all()
    def actualizar_orden(self, id_orden: int, atributos: dict):
        """
        Este método actualiza los atributos de la orden: fecha de entrega, estatus, pagado. Usa un diccionario donde la clave es el atributo y el valor el nuevo valor para actualizarlos por los valores viejos. 
        """
        patch_orden = self.db.query(Orden).filter(
            Orden.id_orden == id_orden
        ).update(atributos)
        return patch_orden
    
    def actualizar_detalle_orden(self, id_detalle: int, items: dict):
        """
        Este método actualiza cualquiera de las siguientes columnas: Producto, Detalle, Cantidad. Es útil para facilitar el cambio en los detalles de una orden cuando el cliente realizó mal un pedido. No permite agregar nuevos items ni quitar los actuales. 
        """
        items_cambiados = self.db.query(DetalleOrden).filter(
            DetalleOrden.id_detalle == id_detalle
        ).update(items)
        return items_cambiados

    def detalles_pendientes(self):
        return self.db.query(DetalleOrden).filter(
            DetalleOrden.asignacion == "Pendiente",
        ).order_by(DetalleOrden.id_detalle.asc()).all()
    def actualizar_asignacion_detalle(self, id_detalle: int):
        query = self.db.query(DetalleOrden).filter(
            DetalleOrden.id_detalle == id_detalle
        ).update({"asignacion":"Asignado"})
        return query
    def evaluacion_asignaciones(self, id_orden: int):
        return self.db.query(DetalleOrden).filter(
            DetalleOrden.id_orden == id_orden
        ).all()
    def actualizar_asignacion_orden(self, id_orden: int, estado: str):
        operacion = self.db.query(Orden).filter(
            Orden.id_orden == id_orden
        ).update({"asignacion":estado})
        return operacion

    def metricas_ordenes(self):
        metricas = self.db.query(
            func.count(Orden.id_orden),
            func.sum(Orden.pagado),
            func.sum(Orden.precio_total) - func.sum(Orden.pagado),
            func.sum(case((Orden.estatus == "Entregado",1), else_=0)),
            func.sum(case((Orden.estatus == "Pendiente",1), else_=0)),
            func.sum(Orden.precio_total)
        ).first()
        return metricas

    def costos_totales(self):
        costo = self.db.query(
            func.sum(DetalleOrden.costo_unitario)
        ).scalar()
        return costo

    def items_faltantes(self):
        items = self.db.query(
            DetalleOrden.producto,
            DetalleOrden.detalle,
            func.sum(DetalleOrden.cantidad)
        ).filter(
            DetalleOrden.asignacion == "Pendiente"
        ).group_by(
            DetalleOrden.producto,
            DetalleOrden.detalle
        ).all()
        return items

    def items_cubiertos(self):
        items = self.db.query(
            func.sum(case((DetalleOrden.asignacion == "Asignado",1), else_=0)),
            func.sum(case((DetalleOrden.asignacion == "Pendiente",1), else_=0))
        ).first()
        return items

    def estatus_pedidos(self):
        pedidos = self.db.query(
            func.sum(case((Orden.asignacion == "Pendiente",1),else_=0)),
            func.sum(case((Orden.asignacion == "Parcialmente Asignado",1),else_=0)),
            func.sum(case((Orden.asignacion == "Asignado",1),else_=0))
        ).first()
        return pedidos


class RepositoryCatalogoProductos:
    def __init__(self, db_session: Session):
        self.db = db_session
    def obtener_id_producto(self, producto: str, detalle: str) -> int:
        resultado = self.db.query(CatalogoProducto).filter(
            CatalogoProducto.producto == producto,
            CatalogoProducto.detalle == detalle
        ).first()
        if not resultado:
            raise ValueError(f"El producto {producto} {detalle} no se encuentra en la base de datos")
        return resultado.id_producto
    def obtener_precio_pedidos(self, tipo_pedido: str) -> float:
        resultado = self.db.query(CatalogoPedido).filter(
            CatalogoPedido.tipo_pedido == tipo_pedido,
        ).first()
        if not resultado:
            return 0.0
        return resultado.precio
    def obtener_precio_piezas(self, pieza: str, detalle: str) -> float:
        resultado = self.db.query(CatalogoProducto).filter(
            CatalogoProducto.producto == pieza,
            CatalogoProducto.detalle == detalle
        ).first()
        if not resultado:
            return 0.0
        return resultado.precio
    def agregar_inventario(self, stock: InventarioRequest):
        datos_dto = stock.model_dump()
        stock = Inventario(**datos_dto)
        self.db.add(stock)
        self.db.flush()
        self.db.refresh(stock)
        return stock
    def traer_stock(self):
        return self.db.query(CatalogoProducto).all()
    def agregar_stock(self, id_producto: int, cantidad: int):
        nuevo_stock = self.db.query(CatalogoProducto).filter(
            CatalogoProducto.id_producto == id_producto
        ).update({"disponibles":CatalogoProducto.disponibles + cantidad})
        return nuevo_stock

    def stock_to_dict(self) -> dict:
        query = self.db.query(CatalogoProducto).all()
        diccionario = {key.id_producto: key.disponibles for key in query}
        return diccionario
    def actualizar_stock(self, id_producto: int, cantidad: int):
        query = self.db.query(CatalogoProducto).filter(
            CatalogoProducto.id_producto == id_producto
        ).update({"disponibles":CatalogoProducto.disponibles- cantidad})
        return query
    def asignar_items(self, id_producto: int, id_detalle: int, cantidad: int):
        asignacion = ItemsAsignados(
            id_producto=id_producto,
            id_detalle=id_detalle,
            cantidad_asignada=cantidad
        )
        self.db.add(asignacion)
        self.db.flush()
        self.db.refresh(asignacion)
        return asignacion