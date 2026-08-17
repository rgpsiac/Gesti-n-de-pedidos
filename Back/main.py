from fastapi import FastAPI
from Back.endpoints.endpoint_pipeline_kits import router as webhook_kits
from Back.models.models import Base
from Back.repositories.bd import engine
import Back.models.models


Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="API Gestión de Inventarios",
    description="Backend para procesar kits"
)
app.include_router(webhook_kits)
@app.get('/')
def home():
    return {"mensaje":"Servidor activo"}