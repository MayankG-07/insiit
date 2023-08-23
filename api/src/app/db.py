import json
import psycopg2
from psycopg2 import connection

with open(r"../../db/db-config.json", "r") as db_config_file:
    db_config = json.load(db_config_file)
    db_credentials = db_config["credentials"]


def connect() -> connection:
    con = psycopg2.connect(
        host=db_credentials["host"],
        port=db_credentials["port"],
        user=db_credentials["username"],
        password=db_credentials["password"],
        database=db_credentials["database"],
    )

    return con


def disconnect(con: connection):
    con.close()
