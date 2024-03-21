import sqlite3
from datetime import datetime
from time import sleep
import paho.mqtt.subscribe as subscribe

db_path     = "db/affald_data.db"
mqtt_topic  = "affald/data"
mqtt_server = "52.178.210.165"

def create_table():
    """
    This function creates a new table in the SQLite database if it doesn't already exist.
    """
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='affald' LIMIT 1;")
    if curs.fetchone():
        print("Table already exists. Starting program...")
    else:
        query = """CREATE TABLE affald (id TEXT, datetime TEXT, fyldning REAL, batteri REAL, vaelt TEXT, ild TEXT)"""
        try:
            curs.execute(query)
            conn.commit()
            print("Table created successfully")
        except Exception as e:
            print("Error:", e)
            print("Failed to connect to the database")
            conn.rollback()
        finally:
            curs.close()

def log_affald_data(client, userdata, message):
    """
    This function logs the fyldning and batteri data to the SQLite database.

    Args:
        client: The MQTT client instance for this callback
        userdata: The private user data as set in Client() or userdata_set()
        message: An instance of MQTTMessage. This is a class with members topic, payload, qos, retain.
    """
    query = """INSERT INTO affald (id, datetime, fyldning, batteri, vaelt, ild) VALUES (?, ?, ?,?, ?, ?)"""

    msg_str = message.payload.decode("utf-8")

    if msg_str.count("|") != 5:
        print("Dataen er ikke korrekt. Dataen skal være på formen: id|dato|fyldning|batteri|vaelt|ild")
        return 
    
    id, dato, fyldning, batteri, vaelt, ild = msg_str.split("|")
    data = (int(id), dato, fyldning, batteri, vaelt, ild)

    if data[5] == True or data[5] == "True": 
        print("Der er ild !!!! Pas på :) ")


    print(f"Data to be inserted: {data}")

    try:
        conn = sqlite3.connect(db_path)
        curs = conn.cursor()
        curs.execute(query, data)
        conn.commit()
    except Exception as e:
        print("Error:", e)
        print("Failed to connect to the database")
        conn.rollback()
    finally:
        curs.close()
    sleep(0.5)

def start_logging():
    """
    This function starts the logging process.
    """
    try:
        create_table()
        subscribe.callback(log_affald_data, mqtt_topic, hostname=mqtt_server)
    except Exception as e:
        print("Error:", e)
    except KeyboardInterrupt:
        print("Program stopped by the user")

start_logging()