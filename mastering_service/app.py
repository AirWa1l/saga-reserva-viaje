from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Mastering Service")

# Lista temporal para almacenar los tracks masterizados
mastered_tracks = []

@app.post("/write")
async def master_track(request: Request):
    data = await request.json()
    user = data.get("user")
    track = data.get("track")

    if not user or not track:
        return JSONResponse({"message": "Faltan campos requeridos (user o track)"}, status_code=400)

    mastered = {
        "user": user,
        "original_track": track,
        "mastered_track": f"Mastered version of '{track}'"
    }
    mastered_tracks.append(mastered)
    return JSONResponse({"message": f"Track masterizado para {user}", "data": mastered}, status_code=200)

@app.post("/erase")
@app.post("/cancel")
async def erase_track(request: Request):
    data = await request.json()
    user = data.get("user")

    for t in mastered_tracks:
        if t["user"] == user:
            mastered_tracks.remove(t)
            return JSONResponse({"message": f"Track masterizado eliminado para {user}"}, status_code=200)

    return JSONResponse({"message": "Track no encontrado"}, status_code=404)

@app.get("/tracks")
async def get_tracks():
    return JSONResponse(mastered_tracks, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5010)
