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
            # Instanciación de la factory
            pipeline = FactoryLimpiezaSheets.llamar_servicio(webhook_kits)
            # Creación de métodos
            cliente = pipeline.crear_cliente()
            orden = pipeline.crear_orden()
            detalle_orden = pipeline.crear_orden_detalles()
            # Guardado del cliente
            send_cliente = self.repo_cliente.crear_cliente(cliente)
            id_cliente_real = send_cliente.id_cliente
            # Asignación del cliente al DTO de la tabla Orden
            orden.id_cliente = id_cliente_real
            send_orden = self.repo_ordenes.crear_orden(orden)
            # Asignación de la orden al DTO de la tabla DetalleOrden
            id_orden_real = send_orden.id_orden
            for detalle in detalle_orden:
                detalle.id_orden = id_orden_real
                id_catalogo = self.repo_catalogo_productos.obtener_id_producto(
                    producto=detalle.producto,
                    detalle=detalle.detalle)
                detalle.id_producto = id_catalogo
                self.repo_ordenes.crear_detalle_orden(detalle)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error guardando datos en la base de datos: {e}")