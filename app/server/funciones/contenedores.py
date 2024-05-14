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
    return data

async def lista_contenedores_empresa(id: int) -> dict:
    validar =""
    #buscar relacion con empresa_id
    sub = "SELECT * FROM contenedores where nombre_contenedor is not null and estado=1"
    query = sub if id ==1 else sub+ " and empresa_id="+str(id)
    print (query)
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    data = cursor.fetchall()
    return data

