from fastapi import FastAPI
from Back.endpoints.endpoint_pipeline_kits import router as webhook_kits
from Back.models.models import Base
from Back.repositories.bd import engine
import Back.models.models
from Back.endpoints.endpoint_ordenes import router as router_ordenes
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Gestión de Inventarios",
    description="Backend para procesar kits"
)
app.include_router(webhook_kits)
app.include_router(router_ordenes)
@app.get('/')
def home():
    return {"mensaje":"Servidor activo"}

origenes_permitidos = []
app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)