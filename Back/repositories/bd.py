import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import NullPool
from sqlalchemy import text

load_dotenv()
url = os.getenv("DATABASE_URL")
if not url:
    raise ValueError("DATABASE URL no encontrado")
engine = create_engine(url, poolclass=NullPool)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()