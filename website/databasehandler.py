import sqlite3
from random import randint, choice


db_path_data = "db/affald_data.db"
db_path_addr = "db/adresse.db"

def id_henter(adresse):
    conn = sqlite3.connect(db_path_addr)
    cur = conn.cursor()
    try:
        cur.execute(f"""SELECT ID, Type FROM adresser WHERE Adresse LIKE '{adresse}%' LIMIT 4;""")
        return_id = cur.fetchall()
        return return_id
    except Exception as e:
        print("An error has occurred", e)
        conn.rollback()
    finally:
        cur.close()

def adresse_henter(id):
    conn = sqlite3.connect(db_path_addr)
    cur = conn.cursor()
    try:
        cur.execute(f"""SELECT Adresse,Type FROM adresser WHERE ID={id};""")
        return_address_type = cur.fetchall()
        return return_address_type
    except Exception as e:
        print("An error has occurred", e)
        conn.rollback()
    finally:
        cur.close()

def data_henter(adresse):
    conn = sqlite3.connect(db_path_data)
    curs = conn.cursor()
    try:
        id_get = id_henter(adresse)
        curs.execute(f"""SELECT * FROM affald WHERE ID='{id_get[0][0]}' ORDER BY datetime DESC LIMIT 1""")
        return_value1 = curs.fetchall()
        curs.execute(f"""SELECT * FROM affald WHERE ID='{id_get[1][0]}' ORDER BY datetime DESC LIMIT 1""")
        return_value2 = curs.fetchall()
        curs.execute(f"""SELECT * FROM affald WHERE ID='{id_get[2][0]}' ORDER BY datetime DESC LIMIT 1""")
        return_value3 = curs.fetchall()
        curs.execute(f"""SELECT * FROM affald WHERE ID='{id_get[3][0]}' ORDER BY datetime DESC LIMIT 1""")
        return_value4 = curs.fetchall()
        return_value = [return_value1[0][2], return_value2[0][2], return_value3[0][2], return_value4[0][2]]
        return return_value
    except Exception as e:
        print("An error has occurred", e)
        conn.rollback()
    finally:
        curs.close()

def fyld_henter():
    temp = []
    temp2 = []
    conn = sqlite3.connect(db_path_data)
    conn.row_factory = lambda cursor, row: row[0]
    conn2 = sqlite3.connect(db_path_addr)
    curs = conn2.cursor()
    cur = conn.cursor()
    try:
        cur.execute(f"""SELECT ID FROM affald WHERE fyldning>80 ORDER BY datetime DESC""")
        value = list(set(cur.fetchall()))
        for i in value:
            curs.execute(f"""SELECT Adresse,Type from adresser WHERE ID='{i}'""")
            x = curs.fetchall()
            temp.append(x)
        for n in temp:
            temp2.append(n[0][0].replace("\n"," ")+"" +n[0][1])
        return temp2
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        cur.close()

def random_data():
    conn = sqlite3.connect(db_path_data)
    cur = conn.cursor()
    try:
        for n in range(1,1580):
            cur.execute(f"""UPDATE affald SET fyldning={randint(0,100)} WHERE id={n}""")
            conn.commit()
    except:
        conn.rollback()
        pass
    finally:
        cur.close()

def empty():
    conn = sqlite3.connect(db_path_data)
    cur = conn.cursor()
    try:
        cur.execute("""UPDATE affald SET fyldning=0 WHERE fyldning>0""")
        conn.commit()
    except:
        conn.rollback()
        pass
    finally:
        cur.close()

def vaelt_check():
    conn = sqlite3.connect(db_path_data)
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    try:
        temp = []
        temp2 = []
        cur.execute(f"""SELECT ID FROM affald WHERE vaelt="True" ORDER BY datetime DESC""")
        ild = cur.fetchall()
        for n in ild:
            temp.append(adresse_henter(n))
        for i in temp:
            temp2.append(i[0][0].replace("\n","")+", " +i[0][1])
        y = ["""<li class="list-group-item">"""+ s + "</li>" for s in temp2]
        return y
    except:
        conn.rollback()
    finally:
        cur.close()

def ild_check():
    conn = sqlite3.connect(db_path_data)
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    try:
        temp = []
        temp2 = []
        cur.execute(f"""SELECT ID FROM affald WHERE ild="True" ORDER BY datetime DESC""")
        ild = cur.fetchall()
        for n in ild:
            temp.append(adresse_henter(n))
        for i in temp:
            temp2.append(i[0][0].replace("\n","")+", " +i[0][1])
        y = ["""<li class="list-group-item">"""+ s + "</li>" for s in temp2]
        return y
    except:
        conn.rollback()
    finally:
        cur.close()

def batteri_check():
    conn = sqlite3.connect(db_path_data)
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    try:
        temp = []
        temp2 = []
        cur.execute(f"""SELECT ID FROM affald WHERE batteri<20 ORDER BY datetime ASC""")
        ild = cur.fetchall()
        for n in ild:
            temp.append(adresse_henter(n))
        for i in temp:
            temp2.append(i[0][0].replace("\n","")+", " +i[0][1])
        y = ["""<li class="list-group-item">"""+ s + "</li>" for s in temp2]
        return y
    except:
        conn.rollback()
    finally:
        cur.close()

def random_data_ild_vealt_batt():
    conn = sqlite3.connect(db_path_data)
    cur = conn.cursor()
    valg = ["True", "False"]
    try:
        for n in range(1,1580):
            cur.execute(f"""UPDATE affald SET batteri={randint(0,100)} WHERE id={n}""")
            cur.execute(f"""UPDATE affald SET vaelt="{choice(valg)}" WHERE id={n}""")
            cur.execute(f"""UPDATE affald SET ild="{choice(valg)}" WHERE id={n}""")
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)
        pass
    finally:
        cur.close()

def empty_ild_vealt_batt():
    conn = sqlite3.connect(db_path_data)
    cur = conn.cursor()
    try:
        cur.execute("""UPDATE affald SET batteri=100 WHERE batteri>=0 """)
        cur.execute("""UPDATE affald SET vaelt="False" WHERE vaelt="True" """)
        cur.execute("""UPDATE affald SET ild="False" WHERE ild="True" """)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
        pass
    finally:
        cur.close()

def lat_long():
    conn = sqlite3.connect(db_path_addr)
    cur = conn.cursor()
    rest = []
    mad = []
    plast = []
    pap = []
    rest_lat_long = []
    mad_lat_long = []
    plast_lat_long = []
    pap_lat_long = []
    try:
        for n in fyld_henter():
         if "Rest" in n:
            rest.append(n.replace("Rest",""))
         if "Mad" in n:
            mad.append(n.replace("Mad",""))
         if "Plast" in n:
            plast.append(n.replace("Plast",""))
         if "Pap" in n:
            pap.append(n.replace("Pap",""))
        for i in rest:
            cur.execute(f"""SELECT Latitude, Longitude Type FROM adresser WHERE Adresse LIKE '{i.strip()}%' LIMIT 1;""")
            temp = cur.fetchall()
            rest_lat_long.append(temp)
        for i in mad:
            cur.execute(f"""SELECT Latitude, Longitude Type FROM adresser WHERE Adresse LIKE '{i.strip()}%' LIMIT 1;""")
            temp = cur.fetchall()
            mad_lat_long.append(temp)
        for i in plast:
            cur.execute(f"""SELECT Latitude, Longitude Type FROM adresser WHERE Adresse LIKE '{i.strip()}%' LIMIT 1;""")
            temp = cur.fetchall()
            plast_lat_long.append(temp)
        for i in pap:
            cur.execute(f"""SELECT Latitude, Longitude Type FROM adresser WHERE Adresse LIKE '{i.strip()}%' LIMIT 1;""")
            temp = cur.fetchall()
            pap_lat_long.append(temp)
        return rest_lat_long, mad_lat_long, plast_lat_long, pap_lat_long
    except Exception as e:
        print(e)
        conn.rollback()
        pass
    finally:
        cur.close()
