import sqlite3
from datetime import datetime
from time import sleep
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

mqtt_remote_broker  = "<MQTT REMOTE BROKER>"  
mqtt_remote_topic   = "affald/data" 
mqtt_local_broker   = "192.168.137.67"
mqtt_local_topic    = "internal/affald"
db_path             = "db/affald_data.db"

def create_table():
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
    query = """INSERT INTO affald (id, datetime, fyldning, batteri, vaelt, ild) VALUES (?,?,?,?,?,?)"""
    msg_str = message.payload.decode("utf-8")

    if msg_str.count("|") != 5:
        print("Dataen er ikke korrekt. Dataen skal være på formen: id|dato|fyldning|batteri|vaelt|ild")
        return 
    
    id, dato, fyldning, batteri, vaelt, ild = msg_str.split("|") 
    data = (id, dato, fyldning, batteri, vaelt, ild)

    if data[5] == True or data[5] == "True" or data[5] == "1": 
        print("Der er ild !!!! Dataen sendes til Azure med det samme")
        send_string = f"{data[0]}|{data[1]}|{data[2]}|{data[3]}|{data[4]}|{data[5]}" 
        try:
            publish.single(mqtt_remote_topic, str(send_string), hostname=mqtt_remote_broker) 
        except Exception as e:
            print("Error:", e)
            print("Failed to send data to Azure")

    print(f"Data to be inserted: {data}")
    print()

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
        subscribe.callback(log_affald_data, mqtt_local_topic, hostname=mqtt_local_broker) 
    except Exception as e:
        print("Error:", e)
    except KeyboardInterrupt:
        print("Program stopped by the user")

start_logging()