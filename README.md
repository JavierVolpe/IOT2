
# Smart Skraldespande -- Intelligent Waste Monitoring
## 🎓 About This Project

This project was developed as part of the **IT-Teknologi** programme at **KEA – Copenhagen School of Design and Technology**.  
It was completed during the **2nd semester (1st year)** by students in the spring of 2024, as a practical group assignment combining embedded systems, networking, databases, and web development.

**Smart Skraldespande** is an IoT-based waste monitoring system designed to improve waste management efficiency in urban environments. It uses ESP32 microcontrollers with various sensors to measure bin fill levels, battery status, tilt detection (fall), and flame presence. All data is sent via MQTT to a Raspberry Pi, which logs it into a local database and optionally forwards it to a cloud broker for external integration.

The project also features a user-friendly Flask web interface for real-time monitoring, route planning, status alerts, and user login.

---

## 🎯 Main Features

### Embedded Devices (ESP32)

- **Ultrasonic Sensors**: Measures bin fill levels.

- **IMU Sensor (MPU6050)**: Detects if bins have been tilted or fallen over.

- **Flame Sensor**: Detects fire inside bins.

- **Battery Monitoring**: Converts ADC readings to battery percentages.

- **Deep Sleep**: Saves power between measurements.

- **MQTT Communication**: Sends formatted data to broker.

### Raspberry Pi

- **MQTT Bridge**: Receives data from bins and logs to SQLite.

- **Scheduled Tasks**: Periodically sends latest updates to a cloud MQTT broker (Azure-ready).

- **Local Database**: Stores historic waste events (`affald_data.db`).

### Web Dashboard (Flask)

- **User Authentication**: Register/login with Flask-Login and SQLite.

- **Status Pages**: Check fire alerts, battery health, and bin tilt.

- **Interactive Maps**: Route planning based on waste levels.

- **Real-Time Visualisation**: Plot current fill levels and status.

- **Admin Actions**: Simulate or reset data for development/demo.

---

## 🧱 Project Structure

```
javiervolpe-iot2/
├── NeoPixel Controller/    # ESP32 client with NeoPixel visual feedback
├── Raspberry Pi/           # MQTT logger and scheduler scripts
├── Skraldespande/          # Main ESP32 waste bin firmware
├── website/                # Flask-based dashboard with templates, static files, DB
└── README.md               # This file
```




---

## 💡 How It Works

1\. **ESP32 devices** wake up, take measurements, and send data like:

id|datetime|fill%|battery%|tilted|fire



2\. **Raspberry Pi** logs this data in an SQLite database and optionally forwards critical messages (like fire) to a remote MQTT broker.

3\. **Web interface** shows the current state of bins, critical alerts, and routes for collection based on waste levels.

---

## 📦 Installation

### Raspberry Pi

```bash

cd Raspberry\ Pi/

pip install -r requirements.txt

python log_affald.py
```

Flask Web Interface

```bash
cd website/

pip install -r requirements.txt

python app.py
```

ESP32 firmware should be flashed using Thonny or ampy; MicroPython is required.

## 👥 Authors

IT-Teknologi - F24 - 2. semester - Gruppe 3B

Emil Fabricius Schlosser

Javier Alejandro Volpe

Morten Hamborg Johansen

## 📅 Deadline

March 24, 2024

## 📜 License

MIT License --- free to use, modify and distribute.

## ✨ Acknowledgements

Rui Santos -- Random Nerd Tutorials (MQTT & ESP32)

KEA IT-Teknologi Instructors:

Bo Hansen, Kevin Lindemark Holm, Malene Hasse, Per Fogt, Tahseen Uddin
