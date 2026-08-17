from fastapi import FastAPI
from Back.endpoints.endpoint_pipeline_kits import router as webhook_kits

app = FastAPI(
    title="API Gestión de Inventarios",
    description="Backend para procesar kits"
)
app.include_router(webhook_kits)
@app.get('/')
def home():
    return {"mensaje":"Servidor activo"}