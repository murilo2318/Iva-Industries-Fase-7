from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente (.env)
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="IVA Industries - API Fase 7",
    description="API de gestão industrial com sensores, máquinas, predições e manutenção.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode restringir depois
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    from routers.machines import router as machines_router
    from routers.sensors import router as sensors_router
    from routers.readings import router as readings_router
    from routers.predictions import router as predictions_router
    from routers.maintenance import router as maintenance_router
    from routers.logs import router as logs_router
except Exception as e:
    logger.error("Erro ao carregar módulos de rotas: %s", e)

app.include_router(machines_router, prefix="/machines", tags=["Machines"])
app.include_router(sensors_router, prefix="/sensors", tags=["Sensors"])
app.include_router(readings_router, prefix="/readings", tags=["Readings"])
app.include_router(predictions_router, prefix="/predictions", tags=["Predictions"])
app.include_router(maintenance_router, prefix="/maintenance", tags=["Maintenance"])
app.include_router(logs_router, prefix="/logs", tags=["System Logs"])


@app.get("/", tags=["Healthcheck"])
def root():
    return {
        "status": "online",
        "message": "IVA Industries API funcionando com sucesso.",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True
    )
