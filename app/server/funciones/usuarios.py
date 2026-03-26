import asyncio

import MySQLdb

from server.database import get_connection


def _retrieve_usuarios_sync():
    query = "SELECT * FROM usuarios"
    with get_connection() as conn:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            usuarios = []
            for registros in data:
                usuarios.append(registros)
            return usuarios
        finally:
            cursor.close()


async def retrieve_usuarios():
    return await asyncio.to_thread(_retrieve_usuarios_sync)


def _retrieve_usuario_sync(user: str) -> dict:
    query = "SELECT u.* , e.empresa_id FROM usuarios u INNER JOIN usuario_empresa e ON u.id = e.usuario_id  WHERE u.usuario=%s"
    with get_connection() as conn:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(query, (user,))
            data = cursor.fetchone()
            if data is None:
                query = "SELECT * FROM usuarios WHERE usuario=%s"
                cursor.execute(query, (user,))
                data = cursor.fetchone()
            return data
        finally:
            cursor.close()


async def retrieve_usuario(user: str) -> dict:
    return await asyncio.to_thread(_retrieve_usuario_sync, user)


def _add_usuario_sync(item) -> dict:
    query = "INSERT INTO usuarios (usuario, apellidos,nombres,password) VALUES (%s, %s,%s, %s)"
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, (item.usuario, item.apellidos, item.nombres, item.password))
            conn.commit()
        finally:
            cursor.close()
    return "ok"


async def add_usuario(item: dict) -> dict:
    return await asyncio.to_thread(_add_usuario_sync, item)


def _extraer_pass_sync(user: str) -> dict:
    query = "SELECT password  FROM usuarios WHERE usuario=%s"
    with get_connection() as conn:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(query, (user,))
            data = cursor.fetchone()
            return data
        finally:
            cursor.close()


async def extraer_pass(user: str) -> dict:
    return await asyncio.to_thread(_extraer_pass_sync, user)
