import sqlite3 
from geopy import geocoders
from time import sleep
db_path_addr = "db/adresse.db"


def log_affald_data():
    query = """INSERT INTO adresser (ID, Adresse, Type, Latitude, Longitude) VALUES (?, ?, ?, ?, ?)"""
    geolocator = geocoders.GoogleV3(api_key="AIzaSyBoykFM7MaQ1RxYvzCGVVFNX21sQc8TZa4")
    try:
        conn = sqlite3.connect(db_path_addr)
        curs = conn.cursor()
        file1 = open("adresser_fil.txt", "r")
        for line in file1:
            addr = line
            location = geolocator.geocode(addr)
            curs.execute("""SELECT ID FROM Adresser ORDER By ID DESC LIMIT 1""")
            id = curs.fetchone()
            data1 = (str(int(id[0])+1), addr, "Rest", location.latitude, location.longitude)
            data2 = (str(int(id[0])+2), addr, "Mad", location.latitude, location.longitude)
            data3 = (str(int(id[0])+3), addr, "Plast", location.latitude, location.longitude)
            data4 = (str(int(id[0])+4), addr, "Pap", location.latitude, location.longitude)
            curs.execute(query, data1)
            curs.execute(query, data2)
            curs.execute(query, data3)
            curs.execute(query, data4)
            conn.commit()
            sleep(0.1)
    except Exception as e:
        print("Error:", e)
        print("Failed to connect to the database")
        conn.rollback()
    finally:
        curs.close()
log_affald_data()