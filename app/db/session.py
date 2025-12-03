# Conexión a la base de datos
# Conexión a la base de datos
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import Request, HTTPException


# Cambia el prefijo a 'mariadb+asyncmy://' para async
DATABASES = {
    "one.monitor-system.tech": {
        "BD1": "mariadb+asyncmy://hfj:Ningun0#@192.168.1.240/DBMuestra",
        "BD2": "mariadb+asyncmy://hfj:Ningun0#@192.168.1.235/DBComer",
        "BD3": "mariadb+asyncmy://hfj:Ningun0#@192.168.1.234/DB_Base"
    },
    "oktan.monitor-system.tech": {
        "BD1": "mariadb+asyncmy://hfj:Ningun0#@192.168.1.235/DBMasterPP"
    },
    "ms_lite.monitor-system.tech": {
        "BD1": "mariadb+asyncmy://hfj:Ningun0#@192.168.1.235/DBMasterPP"
    }
}


# Construcción de engines async (host, db_key) → engine
engine = {
    (host, db_key): create_async_engine(url, future=True, echo=False, pool_size=75, max_overflow=25, pool_timeout=60)
    for host, dbs in DATABASES.items()
    for db_key, url in dbs.items()
}


# Construcción de sesiones async
session = {
    (host, db_key): sessionmaker(bind=eng, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False)
    for (host, db_key), eng in engine.items()
}


# Dependency async para FastAPI
async def get_db(request: Request):
    host = request.headers.get("domain")
    db_name = request.headers.get("x-database")  # Header personalizado

    if not host:
        raise HTTPException(status_code=400, detail="Domain header missing")
    if not db_name:
        raise HTTPException(status_code=400, detail="Database name not provided")

    key = (host, db_name)
    
    # Debug: mostrar qué se está buscando vs qué existe
    available_keys = list(session.keys())
    
    if key not in session:
        raise HTTPException(
            status_code=404, 
            detail=f"Database not found. Looking for: {key}. Available: {available_keys}"
        )

    async with session[key]() as db:
            yield db



# # Conexión a la base de datos
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, Session
# from fastapi import Request, HTTPException

# DATABASES = {
#     "one.monitor-system.tech": {
#         "BD1": "mariadb://hfj:Ningun0#@192.168.1.240/DBMuestra",
#         "BD2": "mariadb://hfj:Ningun0#@192.168.1.235/DBComer",
#         "BD3": "mariadb://hfj:Ningun0#@192.168.1.234/DB_Base"
#     },
#     "oktan.monitor-system.tech": {
#         "BD1": "mariadb://hfj:Ningun0#@192.168.1.235/DBMasterPP"
#     },
# }

# # Construcción de engines (host, db_key) → engine
# engine = {
#     (host, db_key): create_engine(url)
#     for host, dbs in DATABASES.items()
#     for db_key, url in dbs.items()
# }

# # Construcción de sesiones
# session = {
#     (host, db_key): sessionmaker(bind=eng, autocommit=False, autoflush=False)
#     for (host, db_key), eng in engine.items()
# }

# # Dependency para FastAPI
# def get_db(request: Request):
#     host = request.headers.get("domain")
#     db_name = request.headers.get("x-database")  # Header personalizado

#     if not host:
#         raise HTTPException(status_code=400, detail="Host header missing")
#     if not db_name:
#         raise HTTPException(status_code=400, detail="Database name not provided")

#     key = (host, db_name)
#     if key not in session:
#         raise HTTPException(status_code=404, detail=f"Database not found for host={host}, db={db_name}")

#     db: Session = session[key]()
#     try:
#         yield db   # dependency generator
#     finally:
#         db.close()
