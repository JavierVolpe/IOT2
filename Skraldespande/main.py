from umqttsimple import MQTTClient
from machine import Pin, I2C, reset, deepsleep
from hcsr04 import HCSR04
from adc_sub import ADC_substitute
from time import sleep, time
from mpu6050 import MPU6050 
import utime
import esp32
import ntptime

# Pins
pin_us_trigger1 	= 32
pin_us_echo1 		= 35
pin_us_trigger2 	= 18
pin_us_echo2 		= 19
pin_battery 		= 34
pin_flame_sensor 	= 14
pin_postmelder      = 15

# Config
max_distance 		= 17
skraldespande_id    = "0001"
deepsleep_activated = True
deepsleep_tid 		= 21600000
gmt_adjust 			= 3600

# MQTT
mqtt_server = "192.168.137.67"
topic_pub   = b"internal/affald"

# Objects
sensor1 = HCSR04(pin_us_trigger1, pin_us_echo1)
sensor2 = HCSR04(pin_us_trigger2, pin_us_echo2)
flame_sensor = Pin(pin_flame_sensor, Pin.IN)
postmelder = Pin(pin_postmelder, Pin.IN, Pin.PULL_UP)
batttery = ADC_substitute(pin_battery)
i2c = I2C(1)
imu = MPU6050(i2c) 

if deepsleep_activated == True:
    esp32.wake_on_ext0(pin = flame_sensor, level = esp32.WAKEUP_ANY_HIGH)

def update_time():
    try:
        ntptime.settime()

    except Exception as e:
        update_time()
update_time()

try:
    client = MQTTClient(skraldespande_id, mqtt_server)
    client.connect()

except OSError as e:
    print("Der var et problem med at forbinde til MQTT brokeren. Genstarter om 10 sekunder...")
    sleep(10)
    reset()

def get_battery_percentage(): 
    adc_at_0_percent = 1509
    adc_at_100_percent = 2165
    min_battery_voltage = 3.0
    max_battery_voltage = 4.2
    adc_value = batttery.read_adc()

    voltage_range_per_unit_adc = (max_battery_voltage - min_battery_voltage) / (
        adc_at_100_percent - adc_at_0_percent)

    voltage = (adc_value - adc_at_0_percent) * voltage_range_per_unit_adc + min_battery_voltage

    battery_percentage = ((voltage - min_battery_voltage) / (max_battery_voltage - min_battery_voltage)) * 100
    battery_percentage = round(int(battery_percentage))
    if battery_percentage < 0:
        battery_percentage = 0
    elif battery_percentage > 100:
        battery_percentage = 100
    return battery_percentage

def send_update(skraldespande_id, date_time_str, send_percent, batery_level, imudata, flame_detected):
    msg = f"{skraldespande_id}|{date_time_str}|{send_percent}|{batery_level}|{imudata}|{flame_detected}"
    client.publish(topic_pub, msg) 

while True:
    batery_level = get_battery_percentage()
    postmelder_status = postmelder.value()
    flame_detected = flame_sensor.value()
    sensor_value_1 = round(float(sensor1.distance_cm()))
    sleep(0.5)
    sensor_value_2 = round(float(sensor2.distance_cm()))
    sensor_average = round(((sensor_value_1 + sensor_value_2) / 2))
    fri_plads = max_distance - sensor_average
    send_percent = int(fri_plads / max_distance * 100)
    
    if send_percent >= 100:
        print(f"Error: send_percent > 100  ({send_percent}) / Distance: ({sensor_average})")
        send_percent = 100
    elif send_percent < 0:
        send_percent = 0

    try: 
            imu_data = imu.get_values()
            imudata = imu_data.get("acceleration z")
            if abs(imudata) <= 14000:
                imudata = True
            else:
                imudata = False
    except Exception as e: 
            print(f"Failed to execute IMU Sensor: {e}")
            imudata = None

    current_time = utime.time()
    current_time = utime.localtime(current_time + gmt_adjust) 
    date_time_str = "{:02d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(
        current_time[2],
        current_time[1],
        current_time[0] % 100,
        current_time[3],
        current_time[4],
        current_time[5],
    )

    sleep(0.5)
    print()
    print(f"ID: {skraldespande_id}, Time: {date_time_str}, Fyldning: {send_percent}, Battery: {batery_level}, Væltet: {imudata}, Flame: {flame_detected}")

    if flame_detected == 1:
        print("Flame detected: sending update to MQTT nu")
        flame_detected = True
        send_update(skraldespande_id, date_time_str, send_percent, batery_level, imudata, flame_detected)

    elif postmelder_status == 0:
        print("skraldespand åben: sender ikke data til MQTT")
    else:
        try:
            send_update(skraldespande_id, date_time_str, send_percent, batery_level, imudata, flame_detected)

            if deepsleep_activated == True:
                print("Going to sleep in 10 sek")
                sleep(10)
                print("Sleeping now..")
                deepsleep(deepsleep_tid) 

        except OSError as e:
            print("Failed to send data to MQTT broker. Resetting in 10 sec...")
            sleep(10)
            reset()