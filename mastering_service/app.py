from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests

app = FastAPI(title="Mastering Service", version="1.0.0")

# -------------------------------
# MODELO DE DATOS
# -------------------------------
class UserRequest(BaseModel):
    user: str

# Base de datos en memoria
masterizados = []

# -------------------------------
# ENDPOINTS
# -------------------------------

@app.post("/write")
async def masterizar(request: Request):
    """
    Aplica la masterización final para el usuario.
    Simula el proceso de ecualización y compresión.
    """
    data = await request.json()
    user = data.get("user")

    if not user:
        return {"message": "Falta el campo 'user' en la solicitud"}, 400

    resultado = {
        "user": user,
        "status": "mastered",
        "details": {
            "equalization": "balanced",
            "compression": "soft",
            "loudness": -9.0
        }
    }

    masterizados.append(resultado)
    return {"message": f"Track masterizado para {user}", "data": resultado}


@app.post("/cancel")
async def cancelar(request: Request):
    """
    Cancela (revierte) la masterización de un usuario.
    """
    data = await request.json()
    user = data.get("user")

    for registro in masterizados:
        if registro["user"] == user:
            masterizados.remove(registro)
            return {"message": f"Masterización cancelada para {user}"}

    return {"message": "No se encontró masterización para el usuario"}, 


@app.get("/masters")
def ver_masterizaciones():
    """Devuelve todas las masterizaciones registradas."""
    return masterizados


@app.get("/health")
def health_check():
    """Endpoint para monitoreo de Kubernetes."""
    return {"status": "ok"}


# 🆕 NUEVO ENDPOINT: consulta de voces grabadas desde el microservicio de voz
@app.get("/get")
def obtener_voces(user: str):
    """
    Consulta las voces grabadas del servicio de voz (voice-service:5005)
    y las asocia con el usuario actual.
    """
    try:
        # Si estás en Kubernetes → usa el nombre del servicio: voice-service
        # Si estás local → usa localhost:5005
        response = requests.get("http://vocal-recording-service:5005/voices")

        if response.status_code == 200:
            voces = response.json()
            mensaje = f"Las voces grabadas para {user} son: {voces}"
            return {"message": mensaje, "voices": voces}, 200
        else:
            return {"error": "No se pudieron obtener las voces del servicio de voz"}, 500
    except Exception as e:
        return {"error": str(e)}, 500


# -------------------------------
# EJECUCIÓN LOCAL
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5010, reload=True)
