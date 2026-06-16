# 🌡️ IoT Temperature Monitoring System
### Real-Time Sensor Data Pipeline with Arduino, MQTT & WebSocket Dashboard

> **Course:** SPEES402 — Embedded Systems Software Integration  
> **Level:** TVET Level 4 | Software Programming and Embedded Systems  
> **Institution:** Rwanda Coding Academy — Nyabihu  

---

## 📌 Project Overview

This project implements a **complete end-to-end IoT pipeline** that reads live temperature data from a DHT11 sensor, transmits it wirelessly over MQTT, and displays it in real time on a browser-based dashboard — all without refreshing the page.

The system demonstrates integration of embedded hardware (Arduino), serial communication (UART), IoT messaging (MQTT), and real-time web technology (WebSocket) into a single working solution.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HARDWARE LAYER                               │
│                                                                     │
│   ┌──────────────┐    10kΩ pull-up    ┌────────────────────────┐   │
│   │   DHT11      │ ───────────────── │     Arduino UNO         │   │
│   │  Sensor      │  DATA (Digital 2) │                         │   │
│   │              │ ───────────────── │  - Reads temp & humidity│   │
│   │  VCC → 5V    │  VCC              │  - Formats JSON payload │   │
│   │  GND → GND   │  GND              │  - Sends via Serial USB │   │
│   └──────────────┘                   └────────────┬───────────┘   │
│                                                    │               │
└────────────────────────────────────────────────────│───────────────┘
                                                     │ USB / UART
                                                     │ 9600 baud
┌────────────────────────────────────────────────────│───────────────┐
│                     SOFTWARE LAYER (PC)             │               │
│                                                     ▼               │
│                                        ┌────────────────────────┐  │
│                                        │   Python Script        │  │
│                                        │   (publisher.py)       │  │
│                                        │                        │  │
│                                        │  - Reads serial port   │  │
│                                        │  - Parses temperature  │  │
│                                        │  - Formats JSON        │  │
│                                        │  - Publishes to MQTT   │  │
│                                        └────────────┬───────────┘  │
│                                                     │              │
└─────────────────────────────────────────────────────│──────────────┘
                                                      │ MQTT Publish
                                                      │ Port 1883
                                                      │ Topic: spees402/temperature/name
┌─────────────────────────────────────────────────────│──────────────┐
│                      NETWORK LAYER (VPS)             │               │
│                                                      ▼               │
│                                        ┌────────────────────────┐   │
│                                        │    MQTT Broker         │   │
│                                        │  broker.benax.rw       │   │
│                                        │  IP: 157.173.101.159   │   │
│                                        │                        │   │
│                                        │  Port 1883 → MQTT      │   │
│                                        │  Port 9001 → WebSocket │   │
│                                        └────────────┬───────────┘   │
│                                                     │               │
└─────────────────────────────────────────────────────│───────────────┘
                                                      │ WebSocket
                                                      │ Port 9001
┌─────────────────────────────────────────────────────│───────────────┐
│                   PRESENTATION LAYER (Browser)       │               │
│                                                      ▼               │
│                                        ┌────────────────────────┐   │
│                                        │   Web Dashboard        │   │
│                                        │   (index.html)         │   │
│                                        │                        │   │
│                                        │  - Subscribes via WS   │   │
│                                        │  - Live temperature UI │   │
│                                        │  - Auto-updates        │   │
│                                        └────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Summary

```
DHT11 Sensor
    │
    │  analog/digital reading
    ▼
Arduino UNO
    │
    │  Serial UART — 9600 baud
    │  format: {"temperature": 25.3, "humidity": 60.1}
    ▼
Python Publisher (publisher.py)
    │
    │  MQTT Publish — TCP Port 1883
    │  topic: spees402/temperature/candidate_name
    ▼
MQTT Broker (broker.benax.rw : 157.173.101.159)
    │
    │  WebSocket — Port 9001
    ▼
Web Dashboard (index.html)
    │
    │  renders live data in browser
    ▼
User sees real-time temperature updates
```

---

## 📂 Project Structure

```
iot-temperature-monitor/
│
├── README.md                  ← this file
│
├── arduino/
│   └── sensor_code.ino        ← Arduino sketch (DHT11 + Serial output)
│
├── python/
│   └── publisher.py           ← reads serial, publishes to MQTT broker
│
├── dashboard/
│   ├── index.html             ← live web dashboard UI
│   ├── style.css              ← dashboard styling
│   └── app.js                 ← WebSocket + MQTT.js logic
│
└── docs/
    └── wiring_diagram.png     ← hardware wiring reference
```

---

## ⚙️ Hardware Components

| Component | Model | Connection |
|---|---|---|
| Microcontroller | Arduino UNO | USB to PC |
| Temperature & Humidity Sensor | DHT11 | Digital pin 2 |
| Pull-up resistor | 10kΩ | Between DATA and VCC |
| USB cable | Type-B | Arduino to PC serial |

### DHT11 Wiring

| DHT11 Pin | Arduino Pin | Wire Color |
|---|---|---|
| VCC | 5V | Red |
| DATA | Digital 2 | Yellow |
| GND | GND | Black |
| (10kΩ resistor) | DATA → 5V | — |

---

## 🛠️ Software & Libraries

| Component | Technology | Version |
|---|---|---|
| Microcontroller code | Arduino C++ | Arduino IDE 2.x |
| Sensor library | DHT sensor library (Adafruit) | Latest |
| Serial communication | UART — 9600 baud | — |
| PC script | Python 3 | 3.8+ |
| Serial reading | pyserial | pip install pyserial |
| MQTT client (Python) | paho-mqtt | pip install paho-mqtt |
| Browser dashboard | HTML5 / CSS3 / JavaScript | — |
| MQTT client (browser) | MQTT.js | CDN |
| Messaging protocol | MQTT | v3.1.1 |

---

## 📡 MQTT Configuration

| Setting | Value |
|---|---|
| Broker address | broker.benax.rw |
| Broker IP | 157.173.101.159 |
| MQTT port (Python) | 1883 |
| WebSocket port (browser) | 9001 |
| Topic | spees402/temperature/candidate_name |
| QoS level | 0 |
| Retain | false |

---

## 📊 Data Format

Data is published to the MQTT broker in JSON format:

```json
{
  "temperature": 26.2,
  "humidity": 58.4,
  "unit": "celsius",
  "sensor": "DHT11",
  "location": "Arduino_Station_1",
  "timestamp": "2026-06-16T10:24:31"
}
```

Serial format sent from Arduino to PC:
```
TEMP:26.2,HUM:58.4
```

---

## 🚀 How to Run

### Step 1 — Set up the hardware
Connect DHT11 to Arduino following the wiring table above.  
Do not forget the 10kΩ pull-up resistor on the DATA pin.

### Step 2 — Upload Arduino code
Open `arduino/sensor_code.ino` in Arduino IDE.  
Select board: **Arduino UNO**  
Select the correct port (e.g. COM3 on Windows or /dev/ttyUSB0 on Linux)  
Click Upload.

### Step 3 — Install Python dependencies
```bash
pip install pyserial paho-mqtt
```

### Step 4 — Run the Python publisher
```bash
cd python
python publisher.py
```

You should see output like:
```
Connected to MQTT broker
Reading from serial port...
Published: {"temperature": 25.3, "humidity": 60.1, ...}
```

### Step 5 — Open the dashboard
Open `dashboard/index.html` in any browser.  
The dashboard connects to the broker via WebSocket and displays live data.

---

## 🔐 Communication Protocols Used

| Protocol | Used For | Layer |
|---|---|---|
| UART (Serial) | Arduino → Python (USB cable) | Hardware |
| MQTT | Python → Broker (publish) | Network |
| WebSocket | Broker → Browser (subscribe) | Application |
| HTTP | Serving dashboard files | Application |

---

## 🧪 Testing & Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| DHT11 reads NaN | Missing pull-up resistor | Add 10kΩ between DATA and VCC |
| Serial not found | Wrong port name | Check Device Manager (Windows) or `ls /dev/tty*` (Linux) |
| MQTT not connecting | Wrong broker IP or port | Verify IP is 157.173.101.159 and port is 1883 |
| Dashboard not updating | Wrong WebSocket port | Use port 9001 for browser connections |
| Temperature reading too slow | Reading too fast | DHT11 needs minimum 2000ms between reads |

---

## 📌 Key Concepts Demonstrated

- **Embedded firmware** — Arduino reads sensor using DHT library
- **Serial communication (UART)** — Arduino sends data to PC at 9600 baud
- **MQTT publish/subscribe** — Python publishes, browser subscribes
- **WebSocket** — persistent connection for real-time browser updates
- **JSON data formatting** — structured payload for easy parsing
- **IoT pipeline** — full stack from physical sensor to browser dashboard

---

## 🔮 Future Improvements

- [ ] Add live temperature graph using Chart.js
- [ ] Store readings in a database (SQLite or Firebase)
- [ ] Add mobile-responsive dashboard layout
- [ ] Add threshold alerts (email or SMS when temperature too high)
- [ ] Add multiple sensor stations with location tracking
- [ ] Implement MQTT over TLS (port 8883) for secure transmission
- [ ] Add humidity display alongside temperature

---

## 👨‍💻 Author

**Student IoT Project — SPEES402 Embedded Systems Software Integration**  
Rwanda Coding Academy — Nyabihu | Term III | 2025–2026  

---

## 📄 License

This project was created for educational purposes as part of the SPEES402 course at Rwanda Coding Academy.