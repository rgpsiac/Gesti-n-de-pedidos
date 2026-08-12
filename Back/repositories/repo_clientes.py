from sqlalchemy.orm import Session
from Back.repositories.dtos import ClienteBase, ClienteRequest,  ClienteResponse
from Back.repositories.models import Cliente

class RepositoryClientes:
    def __init__(self, db_session: Session):
        self.db = db_session

    def crear_cliente(self, datos_cliente: ClienteRequest):
            try:
                  datos_dict = datos_cliente.model_dump()
                  nuevo_cliente = Cliente(**datos_dict)
                  self.db.add(nuevo_cliente)
                  self.db.commit()
                  self.db.refresh(nuevo_cliente)
                  return nuevo_cliente
            except Exception as e:
                  self.db.rollback()
                  raise e

    def listar_clientes(self):
            return self.db.query(Cliente).all()

    def ver_cliente(self, id_buscado):
          return self.db.query(Cliente).filter(Cliente.id_cliente ==id_buscado).first()
    