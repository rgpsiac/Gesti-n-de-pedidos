from pydantic import BaseModel, Field, field_validator, ConfigDict, EmailStr
from typing import Optional, List
from datetime import datetime

class ClienteBase(BaseModel):
    nombre: str = Field(min_length=2)
    telefono: str|None = Field(max_length=15)
    canal_entrada: str|None = Field(default=None)

class ClienteRequest(ClienteBase):
    pass    

class ClienteResponse(ClienteBase):
    id_cliente: int
    model_config = ConfigDict(from_attributes=True)

class OrdenBase(BaseModel):
    tipo_pedido: str
    fecha_pedido: str|None = Field(default=None)
    fecha_entrega: str|None = Field(default=None)
    precio_total: float = Field(ge=0, default=0.0)
    pagado: float = Field(ge=0, default=0.0)
    estatus: str

class OrdenRequest(OrdenBase):
    id_cliente: int

class OrdenResponse(OrdenBase):
    id_orden: int
    id_cliente: int
    model_config = ConfigDict(from_attributes=True)

class DetalleOrdenBase(BaseModel):
    tipo_pedido: str
    producto: str
    detalle: str
    cantidad: int = Field(ge=0, default=0)
    extra: str = Field(default="No")
    pertenencia: str = Field(default="Kit 1")
    precio_unitario: float = Field(default=0.0)
    subtotal: float = Field(default=0.0)

class DetalleOrdenRequest(DetalleOrdenBase):
    id_orden: int
    id_producto: int

class DetalleOrdenResponse(DetalleOrdenBase):
    id_detalle: int
    id_orden: int
    id_producto: int
    model_config = ConfigDict(from_attributes=True)

class InventarioBase(BaseModel):
    producto: str
    detalle: str
    cantidad_ingresada: int = Field(ge=0, default=0)
    costo_unitario: float = Field(ge=0, default=0.0)
    fecha_registro: datetime

class InventarioRequest(InventarioBase):
    id_producto: int

class InventarioResponse(InventarioBase):
    id_registro: int
    id_producto: int
    model_config = ConfigDict(from_attributes=True)

class CatalogoPedidoBase(BaseModel):
    tipo_pedido: str
    precio: float = Field(ge=0, default=0.0)

class CatalogoPedidoRequest(CatalogoPedidoBase):
    pass

class CatalogoPedidoResponse(CatalogoPedidoBase):
    model_config = ConfigDict(from_attributes=True)

class CatalogoProductoBase(BaseModel):
    producto: str
    detalle: str
    precio: float = Field(default=0.0)

class CatalogoProductoRequest(CatalogoProductoBase):
    pass

class CatalogoProductoResponse(CatalogoProductoBase):
    id_producto: int
    model_config = ConfigDict(from_attributes=True)