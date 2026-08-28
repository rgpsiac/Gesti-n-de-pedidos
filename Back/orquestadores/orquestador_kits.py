from sqlalchemy.orm import Session
from Back.services.services_kits import FactoryLimpiezaSheets, ServiceLimpiezaSheetsEspecial, ServiceLimpiezaSheetsPiezas, ServiceLimpiezaSheetsCombosCowmpadres, ServiceLimpiezaSheetsKitsPlus
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
            # 1. Instanciación del Factory y creación de los objetos DTO
            pipeline = FactoryLimpiezaSheets.llamar_servicio(webhook_kits)
            cliente = pipeline.crear_cliente()
            orden = pipeline.crear_orden()
            detalle_orden = pipeline.crear_orden_detalles()

            # 2. Guardado del cliente y asignación del ID a la Orden
            send_cliente = self.repo_cliente.crear_cliente(cliente)
            id_cliente_real = send_cliente.id_cliente
            orden.id_cliente = id_cliente_real

            # 3. Cálculo de Precio Base (Solo Combos y Kits regulares)
            precio_total = 0.0
            
            if orden.tipo_pedido in ["Kit básico", "Kit plus"]:
                precio_total = self.repo_catalogo_productos.obtener_precio_pedidos(tipo_pedido=orden.tipo_pedido)
                
            elif orden.tipo_pedido == "Combo cowmpadres":
                precio_base = self.repo_catalogo_productos.obtener_precio_pedidos(tipo_pedido="Combo cowmpadres")
                cantidad = (int(webhook_kits.numero_kits_cowmpadres) // 2) if webhook_kits.numero_kits_cowmpadres else 0
                precio_combo = precio_base * cantidad

                precio_kit_extra = 0.0
                if webhook_kits.pregunta_kit_plus_extra and "Sí" in webhook_kits.pregunta_kit_plus_extra:
                    precio_kit_extra = self.repo_catalogo_productos.obtener_precio_pedidos(tipo_pedido="Kit plus")
                precio_total = precio_combo + precio_kit_extra
                
            elif orden.tipo_pedido == "Combo amigoats":
                precio_base = self.repo_catalogo_productos.obtener_precio_pedidos(tipo_pedido="Combo amigoats")
                cantidad = (int(webhook_kits.numero_kits_amigoats) // 2) if webhook_kits.numero_kits_amigoats else 0
                precio_combo = precio_base * cantidad

                precio_kit_extra = 0.0
                if webhook_kits.pregunta_kit_basico_extra and "Sí" in webhook_kits.pregunta_kit_basico_extra:
                    precio_kit_extra = self.repo_catalogo_productos.obtener_precio_pedidos(tipo_pedido="Kit básico")
                precio_total = precio_combo + precio_kit_extra

            # Nota: Si es Tote Bag o Piezas Individuales, el precio base es 0. 
            # Todo se sumará en el ciclo de detalles inferior para no cobrar doble.

            # 4. Guardar la orden inicial en la base de datos
            send_orden = self.repo_ordenes.crear_orden(orden)
            id_orden_real = send_orden.id_orden

            # 5. Procesamiento de Detalles, Costos Históricos y Precios Extra
            for detalle in detalle_orden:
                detalle.id_orden = id_orden_real
                
                # Traemos el ítem completo en una sola query (Optimización O(1) por item)
                item_catalogo = self.repo_catalogo_productos.obtener_item_catalogo(
                    producto=detalle.producto,
                    detalle=detalle.detalle
                )
                
                # Inyección de datos crudos
                detalle.id_producto = item_catalogo.id_producto
                detalle.costo_unitario = item_catalogo.costo_unitario # Eliminamos el bug del inventario fantasma
                
                # Regla de Negocio: Cobrar solo si es un Extra o si el pedido es explícitamente de Piezas Individuales
                if detalle.extra == "Sí" or detalle.tipo_pedido == "Piezas Individuales":
                    precio = item_catalogo.precio
                else:
                    precio = 0.0
                    
                detalle.precio_unitario = precio
                detalle.subtotal = precio * detalle.cantidad
                
                # Sumamos al gran total de la orden
                precio_total += detalle.subtotal

                self.repo_ordenes.crear_detalle_orden(detalle)
            
            # 6. Actualizamos el objeto en memoria con el precio final y comiteamos
            send_orden.precio_total = precio_total
            self.db.commit()
            
            return True
            
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error guardando datos en la base de datos: {e}")