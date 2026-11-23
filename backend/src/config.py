import os

APP_NAME = "Lanchonete Sabor & Cia API"
APP_VERSION = "1.0.0"

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "*").split(",")
    if origin.strip()
]
