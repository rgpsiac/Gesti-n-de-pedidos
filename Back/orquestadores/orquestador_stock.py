from sqlalchemy.orm import Session
from Back.repositories.repositories import RepositoryCatalogoProductos
from Back.models.dtos_tipob import DTOBInventarios
from Back.models.dtos_tipoa import CatalogoProductoRequest, InventarioRequest

class OrquestadorStock:
    def __init__(self, db: Session):
        self.db = db
        self.repo_cat_productos = RepositoryCatalogoProductos(db_session=self.db)
    def procesar_stock(self, dto_inventario: DTOBInventarios):
        try:
            id_producto = self.repo_cat_productos.obtener_id_producto(producto=dto_inventario.producto, detalle=dto_inventario.detalle)
            nuevo_stock = InventarioRequest(producto=dto_inventario.producto,
                                            detalle=dto_inventario.detalle,
                                            cantidad_ingresada=dto_inventario.cantidad,
                                            costo_unitario=dto_inventario.costo_unitario,
                                            fecha_registro=dto_inventario.fecha_registro,
                                            id_producto=id_producto)
            request_inventario = self.repo_cat_productos.agregar_inventario(stock=nuevo_stock)
            request_catalogo = self.repo_cat_productos.agregar_stock(id_producto=id_producto, cantidad=dto_inventario.cantidad)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error guardando en la base de datos: {e}")