import json
from server.database import conn
import MySQLdb

# Recuperar todos los USUARIOS presentes en la base de datos.
async def retrieve_usuarios():
    usuarios = []
    query = "SELECT * FROM usuarios"
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    data = cursor.fetchall()
    #print(data)
    for registros in  data:
        #print(registros)
        usuarios.append(registros)
    return usuarios

# Recuperar un USUARIOS con un user coincidente
async def retrieve_usuario(user: str) -> dict:
    query = "SELECT u.* , e.empresa_id FROM usuarios u INNER JOIN usuario_empresa e ON u.id = e.usuario_id  WHERE u.usuario=%s"
    #sql = "SELECT p.*, d.* FROM permisos p INNER JOIN detalle_permisos d ON p.id = d.id_permiso WHERE e.id_usuario = $id_user AND p.nombre = '$permiso'";
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, (user,))
    data = cursor.fetchone()
    if(data==None):
        query= "SELECT * FROM usuarios WHERE usuario=%s"
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (user,))
        data = cursor.fetchone()
    #print(data)
    return data

async def add_usuario(item: dict) -> dict:
    #aqui envia el json a mongo y lo inserta
    query = "INSERT INTO usuarios (usuario, apellidos,nombres,password) VALUES (%s, %s,%s, %s)"
    cursor = conn.cursor()
    cursor.execute(query, (item.usuario, item.apellidos, item.nombres, item.password))
    conn.commit()
    #item.id = cursor.lastrowid
    #cursor.close()
    return "ok"

# Extraer el ultimo  notificacion de la base de datos en base al campo id
async def extraer_pass(user: str)->dict:
    query = "SELECT password  FROM usuarios WHERE usuario=%s"
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, (user,))
    data = cursor.fetchone()
    return data