from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

async def estaciones(db: AsyncSession):
    query = text("""
        SELECT id_dbm, nombre_corto, razon_social, id_estacion, ubicacion, iframe, direccion, coordenadas_x, coordenadas_y, tipo_estacion
        FROM estacion
    """)
    result = await db.execute(query)
    return result.mappings().all()

async def estaciones_zonas(db: AsyncSession, id_zona: int):
    query = text("""
        SELECT id_dbm, nombre_corto, id_zona
        FROM estacion
        WHERE id_zona = :id_zona
        ORDER BY id_dbm
    """)
    result = await db.execute(query, {"id_zona": id_zona})
    return result.all()