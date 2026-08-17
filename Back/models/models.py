from sqlalchemy import Column, Integer, String, Float, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "clientes"
    id_cliente = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    canal_entrada = Column(String, nullable=False)
    info_orden = relationship("Orden", back_populates="info_cliente")

class Orden(Base):
    __tablename__ = "ordenes"
    id_orden = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    tipo_pedido = Column(String, nullable=False)
    fecha_pedido = Column(String)
    fecha_entrega = Column(String)
    precio_total = Column(Float, nullable=False)
    pagado = Column(Float, nullable=False, default=0.0)
    estatus = Column(String, nullable=False, default="Pendiente")
    info_cliente = relationship("Cliente", back_populates="info_orden")
    detalle_orden = relationship("DetalleOrden", back_populates="info_orden")

class DetalleOrden(Base):
    __tablename__ = "detalles_orden"
    id_detalle = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    id_orden = Column(Integer, ForeignKey("ordenes.id_orden"))
    id_producto = Column(Integer, ForeignKey("catalogo_productos.id_producto"))
    tipo_pedido = Column(String, ForeignKey("catalogo_pedidos.tipo_pedido"))
    producto = Column(String, nullable=False)
    detalle = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    extra = Column(String, nullable=False)
    pertenencia = Column(String, nullable=False)
    info_orden = relationship("Orden", back_populates="detalle_orden")
    cat_producto = relationship("CatalogoProducto", back_populates="detalle_orden")
    cat_pedido = relationship("CatalogoPedido", back_populates="detalle_orden")

class Inventario(Base):
    __tablename__ = "inventario"
    id_registro = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    id_producto = Column(Integer, ForeignKey("catalogo_productos.id_producto"))
    producto = Column(String, nullable=False)
    detalle = Column(String, nullable=False)
    cantidad_ingresada = Column(Integer, nullable=False)
    costo_unitario = Column(Float, nullable=False)
    fecha_registro = Column(DateTime)
    cat_producto = relationship("CatalogoProducto", back_populates="info_inventario")

class CatalogoPedido(Base):
    __tablename__ = "catalogo_pedidos"
    tipo_pedido = Column(String, primary_key=True, nullable=False)
    precio = Column(Float, nullable=False)
    detalle_orden = relationship("DetalleOrden", back_populates="cat_pedido")
    

class CatalogoProducto(Base):
    __tablename__ = "catalogo_productos"
    id_producto = Column(Integer, primary_key=True, unique=True, nullable=False)
    producto = Column(String, nullable=False)
    detalle = Column(String, nullable=False)
    detalle_orden = relationship("DetalleOrden", back_populates="cat_producto")
    info_inventario = relationship("Inventario", back_populates="cat_producto")