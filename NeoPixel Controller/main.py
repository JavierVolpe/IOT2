from time import sleep
from umqttsimple import MQTTClient
from machine import Pin, reset
from neopixel import NeoPixel

# Configuration
mqtt_server = "192.168.137.67"
topic_sub = b"internal/affald"
np_pin = 4 
np_count = 12 
skraldespande_id = "0001"
subscriber_id = "0001_1"

# Objects
np = NeoPixel(Pin(np_pin, Pin.OUT), np_count) 

# Functions
def percent(percent):
    for i in range(np_count):
        np[i] = (0, 100, 0)
    np.write()
    if percent < 0 or percent > 100:
        print("Percenten skal være mellem 0 og 100")
        return
    np_to_light = int((percent / 100) * np_count)
    for i in range(np_to_light):
        np[i] = (100, 0, 0)
    np.write()

def ild_true(): 
    for i in range(np_count):
        np[i] = (100, 100, 0)
    np.write()
    print("Det er ild i skraldespanden")

def besked_ind(topic, msg):
    print((topic, msg))
    percent(100)
    msg_str = msg.decode("utf-8") 

    if msg_str.count("|") != 5:
        print("Dataen er ikke korrekt. Dataen skal være på formen: id|dato|fyldning|batteri|vaelt|ild")
        return  

    sender, dato, fyldning, batteri, vaelt, ild = msg_str.split("|") 

    if sender == skraldespande_id:
        if ild != "0":
            ild_true()
        else:
            print(f"Fyldning: {fyldning} %")
            percent(int(fyldning))


def connect_and_subscribe():
    global subscriber_id, mqtt_server, topic_sub
    client = MQTTClient(subscriber_id, mqtt_server)
    client.set_callback(besked_ind)
    client.connect()
    client.subscribe(topic_sub)
    print("Forbundet til %s MQTT broker, subscribed til %s topic" % (mqtt_server, topic_sub)
    return client

def restart_and_reconnect():
    print("Fejl i forbindelsen til MQTT brokeren. Genstarter og prøver igen i 10 sekunder ...")
    sleep(10)
    reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        client.check_msg()
    except OSError as e:
        restart_and_reconnect()
    except Exception as e:
        print(e)