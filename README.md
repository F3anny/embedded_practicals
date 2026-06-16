# 🌡️ IoT Temperature Monitoring System

A real-time IoT system that reads temperature from a DHT11 sensor using Arduino, processes the data using Python, sends it via MQTT, and displays it on a live web dashboard.

---

## 🚀 Project Overview

This project demonstrates a complete IoT pipeline:

- 📟 Arduino reads temperature from DHT11 sensor
- 💻 Python reads serial data from Arduino
- 📡 Python publishes data to MQTT broker
- 🌐 Web dashboard displays live temperature updates

---

## 🏗️ System Architecture


DHT11 Sensor
↓
Arduino UNO
↓ (Serial Communication)
Python Script
↓ (MQTT Publish)
MQTT Broker (broker.benax.rw)
↓ (WebSocket Connection)
Web Dashboard (HTML/CSS/JS)


---

## 🧠 How It Works

1. **Arduino**
   - Reads temperature from DHT11 sensor
   - Sends data via Serial (USB)

2. **Python Application**
   - Reads serial data from Arduino
   - Parses temperature values
   - Converts data into JSON format
   - Publishes data to MQTT topic:
     ```
     temperature/readings
     ```

3. **MQTT Broker**
   - Receives temperature data
   - Distributes it to subscribed clients

4. **Web Dashboard**
   - Subscribes to MQTT topic using WebSockets
   - Displays live temperature updates
   - Updates UI in real time

---

## 📂 Project Structure


iot-dashboard/
│
├── index.html # Web dashboard UI
├── style.css # Dashboard styling
├── app.js # MQTT connection & logic
│
├── python/
│ └── publisher.py
│
└── arduino/
└── sensor_code.ino


---

## ⚙️ Technologies Used

- Arduino UNO
- DHT11 Sensor
- Python (pyserial, paho-mqtt)
- MQTT Protocol
- HTML, CSS, JavaScript
- MQTT.js (WebSocket client)

---

## 📡 MQTT Details

- **Broker:** broker.benax.rw  
- **Port:** 1883 (Python)  
- **WebSocket Port:** 9001 (Browser)  
- **Topic:** temperature/readings  

---

## 📊 Features

- 🌡️ Real-time temperature monitoring
- 📡 Live MQTT data streaming
- 🌐 Web-based dashboard
- 💾 JSON structured data
- 🔄 Continuous sensor updates

---

## 🧪 Example Data Format

```json
{
  "temperature": 26.2,
  "timestamp": "2026-06-16T10:24:31",
  "unit": "celsius",
  "sensor": "DHT11",
  "location": "Arduino_Station_1"
}
🚀 How to Run
1. Arduino

Upload code to Arduino and connect DHT11 sensor.

2. Python

Run:

python publisher.py
3. Web Dashboard

Open:

index.html

OR deploy using GitHub Pages.

🌐 Live Demo
https://your-username.github.io/iot-dashboard/
👨‍💻 Author

Student IoT Project — Temperature Monitoring System

📌 Future Improvements
Add humidity sensor
Add live graphs
Mobile dashboard version
Cloud database storage

---

# 🧠 2. SYSTEM ARCHITECTURE DIAGRAM (VISUAL)

Here is a **clean diagram you can paste in README (Markdown version)**:


+------------------+
| DHT11 Sensor |
+--------+---------+
|
v
+------------------+
| Arduino UNO |
| (Reads Temp) |
+--------+---------+
|
| Serial USB
v
+------------------+
| Python Script |
| (Parser + MQTT) |
+--------+---------+
|
| MQTT Publish
v
+---------------------------+
| MQTT Broker |
| broker.benax.rw |
+-----------+--------------+
|
| WebSocket
v
+---------------------------+
| Web Dashboard |
| HTML + JS + MQTT.js |
| Live Temperature UI |
+---------------------------+


---

# 🌟 3. OPTIONAL (EVEN BETTER DIAGRAM)

If you want a cleaner “report version”, use this:


[Sensor DHT11]
↓
[Arduino UNO]
↓ Serial
[Python MQTT Publisher]
↓ MQTT Protocol
[MQTT Broker]
↓ WebSocket
[Web Dashboard UI]