from sqlalchemy.orm import Session
from Back.repositories.repositories import RepositoryCatalogoProductos, RepositoryOrdenes
from Back.models.dtos_tipob import DTOBInventarios
from Back.models.dtos_tipoa import CatalogoProductoRequest, InventarioRequest

class OrquestadorStock:
    def __init__(self, db: Session):
        self.db = db
        self.repo_cat_productos = RepositoryCatalogoProductos(db_session=self.db)
        self.repo_ordenes = RepositoryOrdenes(db_session=self.db)

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

    def asignar_items(self):
        try:
            items_pendientes = self.repo_ordenes.detalles_pendientes()
            stock_actual = self.repo_cat_productos.stock_to_dict()
            ordenes_afectadas = set()

            for pendiente in items_pendientes:
                id_producto = pendiente.id_producto

                if stock_actual.get(id_producto,0) > 0:
                    if stock_actual[id_producto] >= pendiente.cantidad:
                        stock_actual[id_producto] -= pendiente.cantidad

                        self.repo_cat_productos.asignar_items(
                            id_producto=id_producto,
                            id_detalle=pendiente.id_detalle,
                            cantidad=pendiente.cantidad
                        )

                        self.repo_ordenes.actualizar_asignacion_detalle(
                            id_detalle=pendiente.id_detalle
                        )

                        self.repo_cat_productos.actualizar_stock(
                            id_producto=id_producto,
                            cantidad=stock_actual[id_producto]
                        )

                        ordenes_afectadas.add(pendiente.id_orden)
                    else:
                        pass

            for orden in ordenes_afectadas:
                items_cubiertos = [item.asignacion for item in self.repo_ordenes.evaluacion_asignaciones(id_orden=orden)]

                if "Pendiente" in items_cubiertos:
                    self.repo_ordenes.actualizar_asignacion_orden(
                        id_orden=orden,
                        estado="Parcialmente Asignado"
                    )
                else:
                    self.repo_ordenes.actualizar_asignacion_orden(
                        id_orden=orden,
                        estado="Asignado"
                    )

            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            raise e