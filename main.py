from fastapi import FastAPI
import os

app = FastAPI(title="Servicio de Autenticación")

# Variable de entorno para verificar la conexión con Docker Compose
MONGO_URL = os.getenv("MONGO_URL", "No definida")

@app.get("/")
def read_root():
    """
    Endpoint raíz que saluda al usuario.
    """
    return {"message": "Bienvenido al Servicio de Autenticación (auth-service)"}

@app.get("/health")
def health_check():
    """
    Endpoint simple de chequeo de salud.
    """
    return {"status": "ok", "mongo_url_conectado": MONGO_URL}