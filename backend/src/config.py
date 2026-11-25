import os

APP_NAME = "Lanchonete Sabor & Cia API"
APP_VERSION = "1.0.0"
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@lanchonete.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "*").split(",")
    if origin.strip()
]
