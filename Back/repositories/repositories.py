from sqlalchemy.orm import Session
from Back.models.dtos_tipoa import ClienteRequest, OrdenRequest, DetalleOrdenRequest
from Back.models.models import Cliente

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
        pass