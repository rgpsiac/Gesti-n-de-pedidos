from sqlalchemy.orm import Session
from Back.models.dtos_tipoa import ClienteRequest, OrdenRequest, DetalleOrdenRequest, DetalleOrdenResponse, OrdenResponse
from Back.models.models import Cliente, Orden, DetalleOrden, CatalogoProducto, CatalogoPedido
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
    def traer_detalle_orden(self, id_orden: int):
        """
        Este método hace una query a la bd para devolver la información detallada de la orden con base en un id_orden, tal como los productos incluidos, sus detalles y cantidades.
        """
        pass
    def actualizar_orden(self, id_orden: int, atributos: dict):
        """
        Este método actualiza los atributos de la orden: fecha de entrega, estatus, pagado. Usa un diccionario donde la clave es el atributo y el valor el nuevo valor para actualizarlos por los valores viejos. 
        """
        pass
    def actualizar_detalle_orden(self, id_orden: int):
        """
        Este método actualiza cualquiera de las siguientes columnas: Producto, Detalle, Cantidad. Es útil para facilitar el cambio en los detalles de una orden cuando el cliente realizó mal un pedido. No permite agregar nuevos items ni quitar los actuales. 
        """
        pass


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