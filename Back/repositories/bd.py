import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import NullPool
from sqlalchemy import text

class DatabaseManager:
    def __init__(self):
        load_dotenv()
        url =  os.getenv("DATABASE_URL")
        if not url: 
            raise ValueError("DATABASE_URL no encontrada") 
        self.engine= create_engine(url, poolclass=NullPool)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

if __name__ == "__main__": 
    try:
        db_manager = DatabaseManager()
        session = db_manager.get_session()
        resultado = session.execute(text('SELECT 1')).scalar()
        print(f"Conexión exitosa. Resultado del ping: {resultado}")
        session.close()
    except Exception as e:
        print(f"Error: {e}")