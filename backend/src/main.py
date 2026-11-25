from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import ADMIN_PASSWORD, APP_NAME, APP_VERSION, CORS_ORIGINS
from src.db.db import Base, engine, SessionLocal
from src.models import Status, Mesa
from src.services.seed_service import seed_database
from src.routes.cadastros import router as cadastros_router
from src.routes.estoque import router as estoque_router
from src.routes.pedidos import router as pedidos_router
from src.routes.relatorios import router as relatorios_router
from src.routes.clientes import router as clientes_router

app = FastAPI(title=APP_NAME, version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if CORS_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    if not ADMIN_PASSWORD:
        raise RuntimeError("ADMIN_PASSWORD must be configured before starting the API")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


@app.get("/", tags=["Sistema"])
def root():
    return {"name": APP_NAME, "docs": "/docs", "health": "/api/health"}


app.include_router(estoque_router, prefix="/api")
app.include_router(cadastros_router, prefix="/api")
app.include_router(pedidos_router, prefix="/api")
app.include_router(relatorios_router, prefix="/api")
app.include_router(clientes_router, prefix="/api")
