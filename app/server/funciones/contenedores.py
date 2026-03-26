import asyncio
from datetime import datetime, timedelta
from typing import Any

import MySQLdb

from server.database import get_connection


def _validar_telemetria_sync(id: int):
    query = "SELECT nombre_contenedor FROM contenedores WHERE telemetria_id=%s limit 1"
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            conn.commit()
            return data
        finally:
            cursor.close()


async def validar_telemetria(id: int):
    return await asyncio.to_thread(_validar_telemetria_sync, id)


def _actualizar_data_sync(data: dict) -> dict:
    cursor = None
    with get_connection() as conn:
        try:
            data["stateProcess"] = None
            update_old_salary = (
                "UPDATE contenedores SET ultima_fecha = %s ,set_point = %s ,temp_supply_1= %s ,return_air= %s"
                ", ambient_air= %s ,relative_humidity= %s ,avl = %s , defrost_prueba = %s , ripener_prueba = %s , ethylene = %s"
                ", set_point_co2 = %s , co2_reading = %s , humidity_set_point = %s , sp_ethyleno = %s , compress_coil_1 = %s "
                ", power_state = %s , evaporation_coil = %s , controlling_mode = %s , stateProcess = %s ,cargo_1_temp = %s "
                ", condensation_coil = %s , consumption_ph_1 = %s , consumption_ph_2 = %s , consumption_ph_3 = %s ,evaporator_speed = %s "
                ", capacity_load = %s , humidity_control = %s , condenser_speed = %s , line_frequency = %s ,line_voltage = %s "
                ", cargo_2_temp = %s , cargo_3_temp = %s , cargo_4_temp = %s , fresh_air_ex_mode = %s  , o2_reading = %s , set_point_o2 = %s ,imei =%s WHERE estado = 1 AND telemetria_id = %s  "
            )
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                update_old_salary,
                (
                    data["fecha"],
                    data["set_point"],
                    data["temp_supply_1"],
                    data["return_air"],
                    data["ambient_air"],
                    data["relative_humidity"],
                    data["avl"],
                    data["inyeccion_pwm"],
                    data["inyeccion_hora"],
                    data["ethylene"],
                    data["set_point_co2"],
                    data["co2_reading"],
                    data["humidity_set_point"],
                    data["sp_ethyleno"],
                    data["compress_coil_1"],
                    data["power_state"],
                    data["evaporation_coil"],
                    data["controlling_mode"],
                    data["stateProcess"],
                    data["cargo_1_temp"],
                    data["condensation_coil"],
                    data["consumption_ph_1"],
                    data["consumption_ph_2"],
                    data["consumption_ph_3"],
                    data["inyeccion_hora"],
                    data["capacity_load"],
                    data["humidity_control"],
                    data["condenser_speed"],
                    data["line_frequency"],
                    data["line_voltage"],
                    data["cargo_2_temp"],
                    data["cargo_3_temp"],
                    data["cargo_4_temp"],
                    data["fresh_air_ex_mode"],
                    data["o2_reading"],
                    data["set_point_o2"],
                    data["i"],
                    data["telemetria_id"],
                ),
            )
            conn.commit()
        finally:
            if cursor is not None:
                cursor.close()
    return data


async def actualizar_data(data: dict) -> dict:
    return await asyncio.to_thread(_actualizar_data_sync, data)


def _retrieve_contenedores_sync():
    query = "SELECT * FROM contenedores where nombre_contenedor is not null"
    with get_connection() as conn:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            conn.commit()
            return data
        finally:
            cursor.close()


async def retrieve_contenedores():
    return await asyncio.to_thread(_retrieve_contenedores_sync)


def _lista_contenedores_sync(id: int) -> dict:
    validar = ""
    if id != 1:
        query1 = "SELECT empresa_id FROM usuario_empresa WHERE usuario_id=%s limit 1"
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query1, (id,))
                data = cursor.fetchone()
                conn.commit()
            finally:
                cursor.close()
        if data:
            validar = "  and empresa_id =" + str(data[0])
        else:
            return []
    query = "SELECT * FROM contenedores where nombre_contenedor is not null" + validar
    with get_connection() as conn:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            conn.commit()
            return data
        finally:
            cursor.close()


async def lista_contenedores(id: int) -> dict:
    return await asyncio.to_thread(_lista_contenedores_sync, id)


def _lista_contenedores_empresa_sync(id: int) -> dict:
    sub = "SELECT * FROM contenedores where nombre_contenedor is not null and estado=1"
    query = sub if id == 1 else sub + " and empresa_id=" + str(id)
    print(query)
    with get_connection() as conn:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            return data
        finally:
            cursor.close()


async def lista_contenedores_empresa(id: int) -> dict:
    return await asyncio.to_thread(_lista_contenedores_empresa_sync, id)


def _lista_contenedores_empresa_2xl_sync(id: int, gmt: str) -> dict:
    sub = "SELECT * FROM contenedores where nombre_contenedor is not null and estado=1"
    query = sub if id == 1 else sub + " and empresa_id=" + str(id)
    print(query)
    with get_connection() as conn:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
        finally:
            cursor.close()
    hora_actual_servidor = datetime.now()
    hora_actual_str_servidor = hora_actual_servidor.strftime("%Y-%m-%d %H:%M:%S")
    hora_actual_str_cliente = hora_actual_servidor.strftime("%Y-%m-%d %H:%M:%S")

    if gmt != "-5":
        diferencia = int(gmt) + 5
        for dat in data:
            print("alterando gmt :)")
            ultima_fecha_str = dat["ultima_fecha"]
            print("----formato de fecha -----")
            print(ultima_fecha_str)
            nueva_fecha = ultima_fecha_str + timedelta(hours=diferencia)

            nueva_fecha_str = nueva_fecha.strftime("%Y-%m-%d %H:%M:%S")
            dat["ultima_fecha"] = nueva_fecha_str
        nueva_fecha_solicitud_cliente = hora_actual_servidor + timedelta(hours=diferencia)
        hora_actual_str_cliente = nueva_fecha_solicitud_cliente.strftime("%Y-%m-%d %H:%M:%S")
    resultado = {
        "data": data,
        "hora servidor": hora_actual_str_servidor,
        "hora_cliente": hora_actual_str_cliente,
        "gmt": gmt,
    }
    return resultado


async def lista_contenedores_empresa_2xl(id: int, gmt: str) -> dict:
    return await asyncio.to_thread(_lista_contenedores_empresa_2xl_sync, id, gmt)


def _lista_contenedores_data_sync(id: int) -> dict:
    sub = "SELECT telemetria_id,ultima_fecha FROM contenedores where nombre_contenedor is not null and estado=1"
    query = sub if id == 1 else sub + " and empresa_id=" + str(id)
    print(query)
    with get_connection() as conn:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            return data
        finally:
            cursor.close()


async def lista_contenedores_data(id: int) -> dict:
    return await asyncio.to_thread(_lista_contenedores_data_sync, id)


def _contenedor_data_sync(id: str) -> dict:
    sub = "SELECT nombre_contenedor,ultima_fecha FROM contenedores where estado=1 and nombre_contenedor='"
    query = sub + str(id) + "' order by id desc limit 1"
    print(query)
    with get_connection() as conn:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            return data
        finally:
            cursor.close()


async def contenedor_data(id: str) -> dict:
    return await asyncio.to_thread(_contenedor_data_sync, id)


def _contenedor_telemetria_sync(id: int) -> dict:
    sub = "SELECT * FROM contenedores where estado=1 and telemetria_id="
    query = sub + str(id) + " order by id desc limit 1"
    print(query)
    with get_connection() as conn:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            return data
        finally:
            cursor.close()


async def contenedor_telemetria(id: int) -> dict:
    return await asyncio.to_thread(_contenedor_telemetria_sync, id)


def _validar_live_sync(notificacion_data) -> dict:
    pro = notificacion_data.data
    actualizar = []
    with get_connection() as conn:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            for val in pro:
                if val["ultima_fecha"]:
                    ultimaFech = val["ultima_fecha"].replace("T", " ")
                else:
                    ultimaFech = val["ultima_fecha"]
                query = (
                    "SELECT telemetria_id,ultima_fecha,descripcionC,set_point,latitud,longitud,temp_supply_1,return_air,evaporation_coil,ambient_air"
                    ",cargo_1_temp,cargo_2_temp,cargo_3_temp,cargo_4_temp,relative_humidity,avl,co2_reading,power_state,humidity_set_point,set_point_co2"
                    ",ethylene,sp_ethyleno,extra_1,compress_coil_1 "
                    "FROM contenedores where nombre_contenedor is not null and telemetria_id="
                    + str(val["telemetria_id"])
                )
                cursor.execute(query)
                dataz = cursor.fetchone()
                conn.commit()
                if str(dataz["ultima_fecha"]) != ultimaFech:
                    actualizar.append(dataz)
        finally:
            cursor.close()
    print(len(actualizar))
    return actualizar


async def validar_live(notificacion_data: Any) -> dict:
    return await asyncio.to_thread(_validar_live_sync, notificacion_data)
