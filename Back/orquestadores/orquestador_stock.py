from sqlalchemy.orm import Session
from Back.repositories.repositories import RepositoryCatalogoProductos, RepositoryOrdenes
from Back.models.dtos_tipob import DTOBInventarios
from Back.models.dtos_tipoa import CatalogoProductoRequest, InventarioRequest, DetalleOrdenRequest

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

            print(f"DEBUG. Pendientes encontrados: {len(items_pendientes)}")
            print(f"DEBUG. Stock actual en BD: {stock_actual}")

            for pendiente in items_pendientes:
                id_producto = pendiente.id_producto

                if stock_actual.get(id_producto,0) > 0:
                    print(f"DEBUG. Hay stock para producto: {id_producto}")
                    cantidad_asignar = min(stock_actual[id_producto], pendiente.cantidad)
                    faltante = pendiente.cantidad - cantidad_asignar
                    stock_actual[id_producto] -= cantidad_asignar

                    self.repo_cat_productos.asignar_items(
                        id_producto=id_producto,
                        id_detalle=pendiente.id_detalle,
                        cantidad=cantidad_asignar
                    )

                    if faltante > 0:
                        print(f"DEBUG. Stock insuficiente para {id_producto}. Realizando split (entregando: {cantidad_asignar}, deuda: {faltante})")
                        self.repo_ordenes.actualizar_detalle_orden(
                            id_detalle=pendiente.id_detalle,
                            items={
                                "cantidad": cantidad_asignar,
                                "subtotal": pendiente.precio_unitario * cantidad_asignar,
                                "asignacion": "Asignado"
                            }
                        )

                        nuevo_detalle = DetalleOrdenRequest(
                            id_orden=pendiente.id_orden,
                            id_producto=pendiente.id_producto,
                            tipo_pedido=pendiente.tipo_pedido,
                            producto=pendiente.producto,
                            detalle=pendiente.detalle,
                            cantidad=faltante,
                            extra=pendiente.extra,
                            pertenencia=pendiente.pertenencia,
                            precio_unitario=pendiente.precio_unitario,
                            subtotal=pendiente.precio_unitario * faltante,
                            asignacion="Pendiente",
                            costo_unitario=pendiente.costo_unitario
                        )
                        self.repo_ordenes.crear_detalle_orden(nuevo_detalle)
                    else:
                        self.repo_ordenes.actualizar_detalle_orden(
                            id_detalle=pendiente.id_detalle,
                            items= {"asignacion":"Asignado"}
                        )

                    self.repo_cat_productos.actualizar_stock(
                        id_producto=id_producto,
                        cantidad=cantidad_asignar
                    )
                    ordenes_afectadas.add(pendiente.id_orden)

            if ordenes_afectadas:
                self.repo_ordenes.actualizar_stock_masivo(ordenes_id=ordenes_afectadas)

            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            raise e