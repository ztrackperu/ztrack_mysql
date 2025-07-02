import json
from server.database import conn
import MySQLdb
from datetime import datetime,timedelta


async def validar_telemetria(id:int) :
    query = "SELECT nombre_contenedor FROM contenedores WHERE telemetria_id=%s limit 1"
    cursor = conn.cursor()
    cursor.execute(query, (id,))
    data = cursor.fetchone()
    conn.commit()
    cursor.close()
    return data

async def actualizar_data(data: dict) -> dict:
    #print("????????")
    #print(data)
    #print("????????")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #data['fecha']=datetime.now()
    #print("aqui estan los datos")
    #print(data)
    #print("---------")
    update_old_salary = (
    "UPDATE contenedores SET ultima_fecha = %s ,set_point = %s ,temp_supply_1= %s ,return_air= %s"
    ", ambient_air= %s ,relative_humidity= %s ,avl = %s , defrost_prueba = %s , ripener_prueba = %s , ethylene = %s"
    ", set_point_co2 = %s , co2_reading = %s , humidity_set_point = %s , sp_ethyleno = %s , compress_coil_1 = %s "
    ", power_state = %s , evaporation_coil = %s , controlling_mode = %s , stateProcess = %s ,cargo_1_temp = %s "
    ", condensation_coil = %s , consumption_ph_1 = %s , consumption_ph_2 = %s , consumption_ph_3 = %s ,evaporator_speed = %s "
    ", capacity_load = %s , humidity_control = %s , condenser_speed = %s , line_frequency = %s ,line_voltage = %s "
    ", cargo_2_temp = %s , cargo_3_temp = %s , cargo_4_temp = %s , fresh_air_ex_mode = %s  ,imei =%s WHERE estado = 1 AND telemetria_id = %s  ")
    cursor.execute(update_old_salary, (data['fecha'], data['set_point'],data['temp_supply_1'], data['return_air'],
                                    data['ambient_air'], data['relative_humidity'], data['avl'], data['inyeccion_pwm'], data['inyeccion_hora'], data['ethylene'],
                                    data['set_point_co2'], data['co2_reading'], data['humidity_set_point'], data['sp_ethyleno'],data['compress_coil_1'], 
                                    data['power_state'],data['evaporation_coil'],data['controlling_mode'],data['stateProcess'], data['cargo_1_temp'],
                                    data['condensation_coil'],data['consumption_ph_1'],data['consumption_ph_2'], data['consumption_ph_3'],data['evaporator_speed'],
                                    data['capacity_load'],data['humidity_control'],data['condenser_speed'], data['line_frequency'],data['line_voltage'],                                       
                                    data['cargo_2_temp'],data['cargo_3_temp'], data['cargo_4_temp'], data['fresh_air_ex_mode'], data['i'],data['telemetria_id']  ))
    cursor.close()


    return data



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
        query1 = "SELECT empresa_id FROM usuario_empresa WHERE usuario_id=%s limit 1"
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

async def lista_contenedores_empresa_2xl(id: int,gmt:str) -> dict:
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
    hora_actual_servidor  = datetime.now()
    hora_actual_str_servidor = hora_actual_servidor .strftime("%Y-%m-%d %H:%M:%S")
    hora_actual_str_cliente = hora_actual_servidor .strftime("%Y-%m-%d %H:%M:%S")

    if gmt !="-5" :
        diferencia =int(gmt)+5
        for dat in data :
            print("alterando gmt :)")
            ultima_fecha_str = dat["ultima_fecha"]
            print("----formato de fecha -----")
            print(ultima_fecha_str)
            #ultima_fecha = datetime.strptime(str(ultima_fecha_str), "%Y-%m-%d %H:%M:%S")
            #nueva_fecha = ultima_fecha + timedelta(hours=diferencia)
            nueva_fecha = ultima_fecha_str + timedelta(hours=diferencia)

            nueva_fecha_str = nueva_fecha.strftime("%Y-%m-%d %H:%M:%S")
            dat["ultima_fecha"] = nueva_fecha_str
        # Capturar la hora actual servidor 
        solicitud_cliente = datetime.strptime(ultima_fecha_str, "%Y-%m-%d %H:%M:%S")
        nueva_fecha_solicitud_cliente = solicitud_cliente + timedelta(hours=diferencia)
        hora_actual_str_cliente = nueva_fecha_solicitud_cliente.strftime("%Y-%m-%d %H:%M:%S")
    resultado = {
        "data":data ,
        "hora servidor" :hora_actual_str_servidor ,
        "hora_cliente" :hora_actual_str_cliente,
        "gmt":gmt
    }
    return resultado

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
        if  val['ultima_fecha'] :
            ultimaFech =val['ultima_fecha'].replace('T',' ')
        else :
            ultimaFech=val['ultima_fecha']
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

