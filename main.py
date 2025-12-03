from fastapi import FastAPI
from fastapi.websockets import WebSocket
from app.api import router

app = FastAPI(title="FastMS API", version="1.0.0")

# Incluir el router principal
app.include_router(router.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Hola, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Conexión WebSocket establecida")
    await websocket.close()