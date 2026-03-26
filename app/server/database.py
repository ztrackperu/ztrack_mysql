from contextlib import contextmanager
from decouple import config
import MySQLdb
from dbutils.pooled_db import PooledDB

# Database configuration
db_config = {
    'host': config("HOST"),
    'user': config("USER_DB"),
    'passwd': config("PASS_DB"),
    'db': config("DB"),
    'port': 3306,
    'charset': 'utf8mb4',
}

# Pool de conexiones: evita una sola conexión compartida (no es segura entre peticiones
# concurrentes) y limita el número de conexiones abiertas a MySQL.
_pool = PooledDB(
    creator=MySQLdb,
    maxconnections=32,
    blocking=True,
    **db_config,
)


@contextmanager
def get_connection():
    """Entrega una conexión del pool; devolverla al pool al salir del bloque."""
    conn = _pool.connection()
    try:
        yield conn
    finally:
        conn.close()
