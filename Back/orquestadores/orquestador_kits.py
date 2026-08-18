from sqlalchemy.orm import Session
from Back.services.services_kits import FactoryLimpiezaSheets, ServiceLimpiezaSheetsEspecial, ServiceLimpiezaSheetsPiezas, ServiceLimpiezaSheetsCombos, ServiceLimpiezaSheetsKits
from Back.repositories.repositories import RepositoryClientes, RepositoryOrdenes, RepositoryCatalogoProductos
from Back.models.dtos_tipoa import ClienteRequest, OrdenRequest, DetalleOrdenRequest
from Back.models.dtos_tipob import DTOBSheets

class OrquestadorPipelineKits:
    def __init__(self, db: Session):
        self.db = db
        self.repo_cliente = RepositoryClientes(self.db)
        self.repo_ordenes = RepositoryOrdenes(self.db)
        self.repo_catalogo_productos = RepositoryCatalogoProductos(self.db)
    def procesar_pedido(self, webhook_kits: DTOBSheets) -> bool:
        try:
            # Instanciación de la factory y creación de los métodos
            pipeline = FactoryLimpiezaSheets.llamar_servicio(webhook_kits)
            cliente = pipeline.crear_cliente()
            orden = pipeline.crear_orden()
            detalle_orden = pipeline.crear_orden_detalles()

            # Guardado del cliente y asignación del cliente al DTO de la tabla Orden
            send_cliente = self.repo_cliente.crear_cliente(cliente)
            id_cliente_real = send_cliente.id_cliente
            orden.id_cliente = id_cliente_real

            # Cálculo de precios
            precio_total = 0.0
            if orden.tipo_pedido == "Kit":
                precio_base = self.repo_catalogo_productos.obtener_precio_pedidos(tipo_pedido="Kit")
                precio_total = precio_base * 1
            elif orden.tipo_pedido == "Combo":
                precio_base = self.repo_catalogo_productos.obtener_precio_pedidos(tipo_pedido="Combo")
                cantidad = (webhook_kits.numero_kits // 2) if webhook_kits.numero_kits else 0
                precio_combo = precio_base * cantidad if cantidad else 0.0

                precio_kit_extra = 0.0
                if webhook_kits.pregunta_kit_extra and "Sí" in webhook_kits.pregunta_kit_extra:
                    precio_kit_extra = self.repo_catalogo_productos.obtener_precio_pedidos(tipo_pedido="Kit")
                precio_total = precio_combo + precio_kit_extra
            elif orden.tipo_pedido == "Tote bag":
                precio_base = self.repo_catalogo_productos.obtener_precio_piezas(pieza="Bolsa",detalle="Tote")
                precio_total += precio_base

            # Asignación de la orden al DTO de la tabla DetalleOrden
            send_orden = self.repo_ordenes.crear_orden(orden)
            id_orden_real = send_orden.id_orden

            for detalle in detalle_orden:
                detalle.id_orden = id_orden_real
                id_catalogo = self.repo_catalogo_productos.obtener_id_producto(
                    producto=detalle.producto,
                    detalle=detalle.detalle)
                detalle.id_producto = id_catalogo
                if detalle.extra == "Sí" or detalle.tipo_pedido == "Piezas Individuales":
                    precio = self.repo_catalogo_productos.obtener_precio_piezas(pieza=detalle.producto, detalle=detalle.detalle)
                elif detalle.extra == "No":
                    precio = 0.0
                detalle.precio_unitario = precio
                detalle.subtotal = precio * detalle.cantidad
                precio_total += detalle.subtotal

                self.repo_ordenes.crear_detalle_orden(detalle)
            send_orden.precio_total = precio_total
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error guardando datos en la base de datos: {e}")