import sqlite3
import paho.mqtt.publish as publish
import schedule
import time

mqtt_broker_ip      = "52.178.210.165"
mqtt_remote_topic   = "affald/data"

print("Starting program: Get last update and send to MQTT")

def send_updates():
    print("Send updates data to MQTT broker")
    db_path = "/home/jvolpe/Desktop/IOT2/db/affald_data.db"
    try:
        conn = sqlite3.connect(db_path)
        curs = conn.cursor()

        query = """
        SELECT id, MAX(datetime), fyldning, batteri, vaelt, ild
        FROM affald
        GROUP BY id
        ORDER BY datetime DESC;
        """ 
        curs.execute(query)
        results = curs.fetchall()

        for row in results:
            print(f"Content: {row}") 
            send_string = f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}|{row[5]}" 
            print(f"Formatted string: {send_string} '\n'") 
            publish.single(mqtt_remote_topic, str(send_string), hostname=mqtt_broker_ip) 

    except Exception as e:
        print("Error:", e)
        print("Failed to connect to the database")

    finally:
        curs.close()
        conn.close()

schedule.every().day.at("06:00").do(send_updates)
schedule.every().day.at("12:00").do(send_updates)
schedule.every().day.at("18:00").do(send_updates)

while True:
    schedule.run_pending()
    time.sleep(1)