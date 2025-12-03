from fastapi import FastAPI
from app.api.router import router as api_router
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Se implementa CORS para permitir solicitudes desde cualquier origen o lista de dominios permitidos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o lista de dominios permitidos
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para verificar la cabecera Host, asegurando que esté presente en cada solicitud
@app.middleware("http")
async def check_host_header(request: Request, call_next):
    host = request.headers.get("domain")
    if not host:
        return JSONResponse(
            status_code=400,
            content={"error": "Host header missing", "code": 1001}
        )
    response = await call_next(request)
    return response

# Middleware para validar el token de autorización, asegurando que esté presente y sea válido
# @app.middleware("http")
# async def validate_token(request: Request, call_next):
#     token = request.headers.get("Authorization")
#     if not token or token != "secret-token":
#         return JSONResponse(status_code=401, content={"error": "Unauthorized"})
#     response = await call_next(request)
#     return response


# Middleware para agregar la cabecera X-Process-Time, midiendo el tiempo de procesamiento de la solicitud
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    process_time = response.headers.get("X-Process-Time")
    if process_time:
        response.headers["X-Process-Time"] = process_time
    return response

# Middleware para manejo de errores
# @app.middleware("http")
# async def handle_errors(request: Request, call_next):
#     try:
#         response = await call_next(request)
#         return response
#     except HTTPException as e:
#         return JSONResponse(
#             status_code=e.status_code,
#             content={"error": e.detail, "code": e.status_code}
#         )
#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"error": str(e), "code": 1000}
#         )

app.include_router(api_router)