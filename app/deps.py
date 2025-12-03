# Dependencias
from fastapi import Request, HTTPException, Depends
#Esta dependencia permite obtener la sesión de la base de datos según el host

# Import or define the session dictionary/object
from app.db.session import session

#Se define una funcion para obtener la sesion de la base de datos
from fastapi import Request, HTTPException


# Versión asíncrona de get_db
async def get_db(request: Request):
    host = request.headers.get("host")
    db_name = request.headers.get("x-database")

    if not host:
        raise HTTPException(status_code=400, detail="Host header missing")
    if not db_name:
        raise HTTPException(status_code=400, detail="Database name not provided")

    key = (host, db_name)
    if key not in session:
        raise HTTPException(status_code=404, detail="Database not found")

    async with session[key]() as db:
            yield db



# # Dependencias
# from fastapi import Request, HTTPException, Depends
# #Esta dependencia permite obtener la sesión de la base de datos según el host
# from app.db.session import get_db
# from sqlalchemy.orm import Session

# # Import or define the session dictionary/object
# from app.db.session import session

# #Se define una funcion para obtener la sesion de la base de datos
# from fastapi import Request, HTTPException, Depends
# from sqlalchemy.orm import Session

# def get_db(request: Request):
#     host = request.headers.get("host")
#     db_name = request.headers.get("x-database")

#     if not host:
#         raise HTTPException(status_code=400, detail="Host header missing")
#     if not db_name:
#         raise HTTPException(status_code=400, detail="Database name not provided")

#     key = (host, db_name)
#     if key not in session:
#         raise HTTPException(status_code=404, detail="Database not found")

#     db: Session = session[key]()
#     try:
#         yield db   # 👈 Dependency generator
#     finally:
#         db.close()
