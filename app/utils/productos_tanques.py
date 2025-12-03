from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

async def obtener_productos(db: AsyncSession, dbm: int):
    """
    Obtiene la lista de productos desde la base de datos.
    """
    productos = await db.execute(text("""
        SELECT * FROM productos WHERE id_dbm = :dbm ORDER BY CASE
            WHEN LOWER(nombre) REGEXP 'regular|magna|maxima' THEN 1
            WHEN LOWER(nombre) REGEXP 'premium|suprema' THEN 2
            WHEN LOWER(nombre) REGEXP 'diesel' THEN 3
            ELSE 4
        END
    """), {"dbm": dbm})
    rows = productos.mappings().all()
    data = []
    for producto in rows:
        data.append({
            "id_producto": producto.id_producto,
            "nombre": producto.nombre,
            "clase": producto.clase
        })
    return data

async def obtener_productos2(db: AsyncSession, dbm: int):
    """
    Obtiene la lista de productos desde la base de datos.
    """
    productos = await db.execute(text("""
        SELECT * FROM productos WHERE id_dbm = :dbm ORDER BY CASE
            WHEN LOWER(clave_prod_ser) REGEXP '15101514' THEN 1
            WHEN LOWER(clave_prod_ser) REGEXP '15101515' THEN 2
            WHEN LOWER(clave_prod_ser) REGEXP '15101505' THEN 3
            ELSE 4
        END
    """), {"dbm": dbm})
    rows = productos.mappings().all()
    data = []
    for producto in rows:
        data.append({
            "id_producto": producto.id_producto,
            "nombre": producto.nombre,
            "clase": producto.clase,
            "clave_producto": producto.clave_prod_ser,
            "precio": producto.precio
        })
    return data

async def obtener_tanques(db: AsyncSession, dbm: int):
    """
    Obtiene la lista de tanques desde la base de datos.
    """
    tanques = await db.execute(text("""
        SELECT * FROM tanques, productos WHERE productos.id_dbm = :dbm AND tanques.id_producto = productos.id_producto AND productos.clase = 1 AND tanques.id_dbm = :dbm
        ORDER BY CASE
            WHEN LOWER(clave_prod_ser) REGEXP '15101514' THEN 1
            WHEN LOWER(clave_prod_ser) REGEXP '15101515' THEN 2
            WHEN LOWER(clave_prod_ser) REGEXP '15101505' THEN 3
            ELSE 4
        END
    """), {"dbm": dbm})
    rows = tanques.mappings().all()
    data = []
    for tanque in rows:
        data.append({
            "id_tanque": tanque.id_tanque,
            "nombre": tanque.descripcion,
            "producto": tanque.id_producto,
            "clave_prod_ser": tanque.clave_prod_ser,
        })
    return data

