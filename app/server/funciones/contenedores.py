import json
from server.database import conn
import MySQLdb

# Recuperar todos los contenedores presentes en la base de datos.
async def retrieve_contenedores():
    usuarios = []
    query = "SELECT * FROM contenedores where nombre_contenedor is not null"
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    #print(data)
    #for registros in  data:
        #print(registros)
        #usuarios.append(registros)
    return data

async def lista_contenedores(id: int) -> dict:
    validar =""
    #buscar relacion con empresa_id
    if id!=1 :
        query1 = "SELECT empresa_id FROM usuario_empresa WHERE usuario_id=%s"
        #cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute(query1, (id,))
        data = cursor.fetchone()
        conn.commit()
        cursor.close()
        if(data):
            validar = "  and empresa_id ="+str(data[0])
            #print(validar)
        else :
            return []
    query = "SELECT * FROM contenedores where nombre_contenedor is not null"+validar
    #print (query)
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    return data

async def lista_contenedores_empresa(id: int) -> dict:
    validar =""
    #buscar relacion con empresa_id
    sub = "SELECT * FROM contenedores where nombre_contenedor is not null and estado=1"
    query = sub if id ==1 else sub+ " and empresa_id="+str(id)
    print (query)
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    data = cursor.fetchall()
    cursor.close()
    return data

async def lista_contenedores_data(id: int) -> dict:
    validar =""
    #buscar relacion con empresa_id
    sub = "SELECT telemetria_id,ultima_fecha FROM contenedores where nombre_contenedor is not null and estado=1"
    query = sub if id ==1 else sub+ " and empresa_id="+str(id)
    print (query)
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    data = cursor.fetchall()
    cursor.close()
    return data

async def contenedor_data(id: str) -> dict:
    validar =""
    #buscar relacion con empresa_id
    sub = "SELECT nombre_contenedor,ultima_fecha FROM contenedores where estado=1 and nombre_contenedor='"
    query = sub+str(id)+ "' order by id desc limit 1"
    print (query)
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    data = cursor.fetchall()
    cursor.close()
    return data

async def contenedor_telemetria(id: int)->dict  :
    validar =""
    #buscar relacion con empresa_id
    sub = "SELECT * FROM contenedores where estado=1 and telemetria_id="
    query = sub+str(id)+ " order by id desc limit 1"
    print (query)
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    data = cursor.fetchall()
    cursor.close()
    return data


async def validar_live(notificacion_data: dict) -> dict:
    #ok 
    #aqui envia el json a mongo y lo inserta
    #notificacion = await notificacion_collection.insert_one(notificacion_data)
    #aqui busca el dato obtenido para mostrarlo como respuesta
    #new_notificacion = await notificacion_collection.find_one({"_id": notificacion.inserted_id})
    #print(notificacion_data.data)  
    pro = notificacion_data.data 
    actualizar =[]
    for val in pro:
        #validaciond de datos internos 
        #print(val['telemetria_id']) 
        ultimaFech =val['ultima_fecha'].replace('T',' ')
        #print(ultimaFech)
        query1 = "SELECT telemetria_id,ultima_fecha,descripcionC,set_point,latitud,longitud,temp_supply_1,return_air,evaporation_coil,condensation_coil"
        query1 +=",compress_coil_1,ambient_air,cargo_1_temp,cargo_2_temp,cargo_3_temp,cargo_4_temp,relative_humidity,avl,line_voltage,line_frequency"
        query1 +=",consumption_ph_1,consumption_ph_2,consumption_ph_3,co2_reading,power_kwh,power_state,humidity_set_point,controlling_mode,set_point_co2"
        query1 += ",defrost_term_temp,defrost_interval,ethylene,sp_ethyleno,extra_1"

        query = "SELECT telemetria_id,ultima_fecha,descripcionC,set_point,latitud,longitud,temp_supply_1,return_air,evaporation_coil,ambient_air"
        query +=",cargo_1_temp,cargo_2_temp,cargo_3_temp,cargo_4_temp,relative_humidity,avl,co2_reading,power_state,humidity_set_point,set_point_co2"
        query +=",ethylene,sp_ethyleno,extra_1,compress_coil_1 "
        query +="FROM contenedores where nombre_contenedor is not null and telemetria_id="+str(val['telemetria_id'])
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        dataz = cursor.fetchone()
        conn.commit()
        cursor.close()
        #print(dataz)
        #print(str(dataz['ultima_fecha']))
        if(str(dataz['ultima_fecha'])!=ultimaFech):
            #print("debemos actualizar los datos")
            actualizar.append(dataz)
    #print(pro[0])
    print(len(actualizar))
    return actualizar

