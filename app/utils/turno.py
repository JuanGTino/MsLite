from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

async def obtener_turnos(db: AsyncSession, dbm: int, id_turno: int):
    query = text("SELECT * FROM turnos WHERE id_dbm = :dbm and id_turno like :id_turno ORDER BY id_turno DESC LIMIT 1")
    #print(f"Ejecutando consulta para obtener turno final: dbm={dbm}, id_turno={id_turno}")
    result = await db.execute(query, {"dbm": dbm, "id_turno": f"%{id_turno}%"})
    row = result.first()
    turno_final = row.id_turno if row else 0
    return turno_final

