from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime, timedelta
import asyncio
from app.utils.estaciones import estaciones_zonas
from app.utils.productos_tanques import obtener_productos2
from app.utils.turno import obtener_turnos
from app.db.session import session
from collections import defaultdict

async def get_tanques_precios(db: AsyncSession, host: str, db_name: str):
    fecha_obj = datetime.now() - timedelta(days=1)
    fecha = fecha_obj.strftime("%Y%m%d")
    acumulados = {
        "total_general": 0,
        "zonas": []
    }
    turno_inicial = str(fecha) + "01"
    zonas = (await db.execute(text("SELECT id_zona, zona FROM cat_zonas"))).mappings().all()
    async def procesar_estacion(estacion, zona, acumulados_zona, semaphore):
        async with semaphore:
            async with session[(host, db_name)]() as db_estacion:
                turno_final = await obtener_turnos(db_estacion, estacion.id_dbm, fecha)
                acumulados_estacion = {
                    "message": "the station has connection" if turno_final == "" else "the station has no connection",
                    "turn": turno_final,
                    "id": estacion.id_dbm,
                    "name": estacion.nombre_corto,
                    "last_update": "",
                    "products": [],
                }
                productos = await obtener_productos2(db_estacion, estacion.id_dbm)
                productos = [p for p in productos if p["clase"] == 1]
                #**Precio de compra por producto (carburantes)**
                query_precio_compra = text("""SELECT 
                    t.id_producto,
                    t.descripcion AS nombre_tanque,
                    ROUND(trd.precio_compra, 2) AS precio_compra,
                    p.clave_prod_ser as clave_producto
                FROM tanque_entregas te
                JOIN tanques t 
                    ON te.id_tanque = t.id_tanque AND te.id_dbm = t.id_dbm
                JOIN (
                    SELECT DISTINCT folio_relacion, id_entrega, id_dbm
                    FROM tanque_recepcion_detalle
                    GROUP BY folio_relacion, id_dbm
                ) trd2
                    ON te.id_entrega = trd2.id_entrega AND te.id_dbm = trd2.id_dbm
                JOIN tanque_recepcion_documentos trd 
                    ON trd2.folio_relacion = trd.folio_relacion AND trd2.id_dbm = trd.id_dbm
                JOIN productos p ON p.id_dbm = t.id_dbm AND p.id_producto = t.id_producto 
                WHERE te.id_turno <= :turno_final
                AND te.id_dbm = :id_dbm
                AND te.pemex_registrada = 1
                ORDER BY te.id_entrega DESC, te.id_turno DESC LIMIT :limit;""")
                result = await db_estacion.execute(
                    query_precio_compra,
                    {"id_dbm": estacion.id_dbm, "turno_final": turno_final, "limit": len(productos)}
                )
                precios_compra = result.mappings().all()
                precios_compra_dict = {pc["clave_producto"]: pc["precio_compra"] for pc in precios_compra}
                #**Capacidad y volumen de tanques por producto (carburantes)**
                tanques_capacidad_volumen = text("""SELECT t.descripcion as nombre, t.capacidad as capacidad, t.volumen as volumen, t.Ultima_Actualizacion as ultima_actualizacion, p.clave_prod_ser FROM tanques t JOIN productos p ON t.id_producto = p.id_producto AND t.id_dbm = p.id_dbm WHERE p.id_dbm=:id_dbm""")
                result = await db_estacion.execute(
                    tanques_capacidad_volumen,
                    {"id_dbm": estacion.id_dbm}
                )
                tanques = result.mappings().all()
                # Agrupa los tanques por clave_prod_ser, cada clave puede tener más de 1 tanque
                tanques_dict = defaultdict(list)
                for t in tanques:
                    tanques_dict[t["clave_prod_ser"]].append((t["capacidad"], t["volumen"], t["ultima_actualizacion"]))
                #**Precio de venta por producto (carburantes)**
                query_precios_venta = text("SELECT p.clave_prod_ser as clave, tb.precio as precio FROM productos p JOIN turnos_precio tb ON p.id_producto = tb.id_producto AND p.id_dbm = tb.id_dbm WHERE p.id_dbm=:id_dbm AND tb.id_turno BETWEEN :turno_inicial AND :turno_final ORDER BY tb.id_turno DESC")
                result = await db_estacion.execute(
                    query_precios_venta,
                    {"id_dbm": estacion.id_dbm, "turno_inicial": turno_inicial, "turno_final": turno_final}
                )
                precios_venta = result.mappings().all()
                precios_venta_dict = {}
                for pv in precios_venta:
                    clave = pv["clave"]
                    precio = pv["precio"]
                    if clave not in precios_venta_dict:
                        precios_venta_dict[clave] = precio
                    else:
                        if precios_venta_dict[clave] != precio:
                            # Si ya existe, marca el precio con un asterisco
                            if not isinstance(precios_venta_dict[clave], str) or '*' not in str(precios_venta_dict[clave]):
                                precios_venta_dict[clave] = f"{precios_venta_dict[clave]}*"
                product = []
                for p in productos:
                    precios_compra = precios_compra_dict.get(p["clave_producto"], 0)
                    tanques_info = tanques_dict.get(p["clave_producto"], [])
                    precio_venta = precios_venta_dict.get(p["clave_producto"], 0)
                    precio_venta_utilidad = str(precio_venta).replace('*', '')
                    nombre = "MAGNA" if p["clave_producto"] == "15101514" else "PREMIUM" if p["clave_producto"] == "15101515" else "DIESEL" if p["clave_producto"] == "15101505" else "Otro"
                    try:
                        utilidad = float(precio_venta_utilidad) - float(precios_compra)
                    except:
                        utilidad = -precios_compra
                    product.append({
                        "id_producto": p["id_producto"],
                        "nombre": nombre,
                        "clave_producto": p["clave_producto"],
                        "precio_compra": precios_compra,
                        "precio_venta": precio_venta,
                        "utilidad": round(utilidad, 3),
                        "tanques": [{
                            "capacidad": capacidad,
                            "volumen": volumen,
                            "ultima_actualizacion": ultima_actualizacion
                        } for capacidad, volumen, ultima_actualizacion in tanques_info]
                    })
                acumulados_estacion["last_update"] = tanques_info[0][2] if tanques_info else ""
                acumulados_estacion["products"] = product
                acumulados_zona["stations"].append(acumulados_estacion)
                
    for zona in zonas:
        estaciones = await estaciones_zonas(db, zona["id_zona"])
        acumulados_zona = {
            "id_zona": zona["id_zona"],
            "zona": zona["zona"],
            "total_zona": 0,
            "stations": []
        }
        semaphore = asyncio.Semaphore(75)  # Limitar a 75 conexiones simultáneas
        await asyncio.gather(
            *(procesar_estacion(e, zona, acumulados_zona, semaphore) for e in estaciones)
        )
        #round(acumulados_zona["total_zona"], 2)
        acumulados["zonas"].append(acumulados_zona)
    #round(acumulados["total_general"], 2)
    return acumulados