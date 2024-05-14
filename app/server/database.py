from bson.objectid import ObjectId
from decouple import config
import MySQLdb
# Database configuration
db_config = {
    'host': config("HOST"),
    'user': config("USER_DB"),
    'passwd': config("PASS_DB"),
    'db': config("DB"),
    'port':  33061,
}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)
#cursor = conn.cursor(MySQLdb.cursors.DictCursor)