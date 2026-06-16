#!/usr/bin/env python3
"""
IoT Temperature Monitoring System - Python MQTT Publisher
Purpose: Read temperature data from Arduino via Serial and publish to MQTT broker
Author: Temperature Monitoring System
"""

import serial
import json
import time
import sys
import re
from datetime import datetime
import paho.mqtt.client as mqtt
import threading

class TemperatureMQTTPublisher:
    def __init__(self):
        """Initialize the Temperature MQTT Publisher with configuration"""
        
        # Serial Configuration
        self.serial_port = 'COM11'  # Change this to your Arduino port (COM3, COM4, etc on Windows)
        self.serial_baudrate = 9600
        self.serial_timeout = 1
        self.serial_connection = None
        
        # MQTT Configuration
        self.mqtt_broker =  '157.173.101.159'
        self.mqtt_port = 1883
        self.mqtt_topic = 'temperature/readings'
        self.mqtt_client = None
        self.mqtt_connected = False
        
        # Data processing
        self.last_temperature = None
        self.running = True
        
        print("Temperature MQTT Publisher initialized")
        print(f"Serial Port: {self.serial_port}")
        print(f"MQTT Broker: {self.mqtt_broker}:{self.mqtt_port}")
        print(f"MQTT Topic: {self.mqtt_topic}")

    def setup_serial_connection(self):
        """
        Establish serial connection with Arduino
        Returns: True if successful, False otherwise
        """
        try:
            print(f"\nAttempting to connect to Arduino on {self.serial_port}...")
            self.serial_connection = serial.Serial(
                port=self.serial_port,
                baudrate=self.serial_baudrate,
                timeout=self.serial_timeout
            )
            
            # Wait for Arduino to initialize
            time.sleep(2)
            
            print("✓ Serial connection established successfully!")
            return True
            
        except serial.SerialException as e:
            print(f"✗ Serial connection failed: {e}")
            print("Please check:")
            print("1. Arduino is connected to the correct port")
            print("2. Port is not being used by another application")
            print("3. Arduino is properly powered")
            return False
        except Exception as e:
            print(f"✗ Unexpected error during serial setup: {e}")
            return False

    def setup_mqtt_connection(self):
        """
        Establish MQTT connection with broker
        Returns: True if successful, False otherwise
        """
        try:
            print(f"\nAttempting to connect to MQTT broker at {self.mqtt_broker}:{self.mqtt_port}...")
            
            # Create MQTT client
            self.mqtt_client = mqtt.Client(client_id="temperature_publisher")
            
            # Set callback functions
            self.mqtt_client.on_connect = self.on_mqtt_connect
            self.mqtt_client.on_disconnect = self.on_mqtt_disconnect
            self.mqtt_client.on_publish = self.on_mqtt_publish
            
            # Connect to broker
            self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port, 60)
            
            # Start MQTT loop in separate thread
            self.mqtt_client.loop_start()
            
            # Wait for connection
            time.sleep(2)
            
            if self.mqtt_connected:
                print("✓ MQTT connection established successfully!")
                return True
            else:
                print("✗ MQTT connection failed - broker may be unavailable")
                return False
                
        except Exception as e:
            print(f"✗ MQTT connection error: {e}")
            print("Please check:")
            print("1. MQTT broker is running")
            print("2. Broker address and port are correct")
            print("3. Network connectivity")
            return False

    def on_mqtt_connect(self, client, userdata, flags, rc):
        """Callback for MQTT connection events"""
        if rc == 0:
            self.mqtt_connected = True
            print(f"✓ MQTT Connected with result code {rc}")
        else:
            self.mqtt_connected = False
            print(f"✗ MQTT Connection failed with result code {rc}")

    def on_mqtt_disconnect(self, client, userdata, rc):
        """Callback for MQTT disconnection events"""
        self.mqtt_connected = False
        print(f"✗ MQTT Disconnected with result code {rc}")

    def on_mqtt_publish(self, client, userdata, mid):
        """Callback for MQTT publish events"""
        pass  # Could add logging here if needed

    def parse_temperature_data(self, serial_line):
        """
        Parse temperature data from Arduino serial output
        Expected format: TEMP:25.60,TIME:12345
        Returns: temperature value as float, or None if parsing fails
        """
        try:
            # Remove whitespace and convert to string
            line = serial_line.strip()
            
            # Look for temperature pattern
            temp_match = re.search(r'TEMP:([\d.-]+)', line)
            
            if temp_match:
                temperature = float(temp_match.group(1))
                return temperature
            
            return None
            
        except (ValueError, AttributeError) as e:
            # Not a temperature reading - might be debug message
            return None
        except Exception as e:
            print(f"✗ Error parsing temperature data: {e}")
            return None

    def read_serial_data(self):
        """
        Continuously read data from Arduino serial port
        This runs in the main thread
        """
        print("\n🔄 Starting temperature monitoring...")
        print("Waiting for temperature data from Arduino...\n")
        
        while self.running:
            try:
                if self.serial_connection and self.serial_connection.in_waiting > 0:
                    # Read line from serial
                    serial_line = self.serial_connection.readline().decode('utf-8').strip()
                    
                    if serial_line:
                        print(f"📡 Received: {serial_line}")
                        
                        # Try to parse temperature data
                        temperature = self.parse_temperature_data(serial_line)
                        
                        if temperature is not None:
                            self.last_temperature = temperature
                            print(f"🌡️  Temperature: {temperature}°C")
                            
                            # Publish to MQTT
                            self.publish_temperature(temperature)
                        
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
            except serial.SerialException as e:
                print(f"✗ Serial communication error: {e}")
                print("Attempting to reconnect...")
                time.sleep(5)
                if not self.setup_serial_connection():
                    print("Failed to reconnect. Exiting...")
                    break
                    
            except KeyboardInterrupt:
                print("\n🛑 Keyboard interrupt received. Shutting down...")
                self.running = False
                break
                
            except Exception as e:
                print(f"✗ Unexpected error in serial reading: {e}")
                time.sleep(1)

    def publish_temperature(self, temperature):
        """
        Publish temperature data to MQTT broker
        Args:
            temperature: Temperature value as float
        """
        if not self.mqtt_connected:
            print("⚠️  MQTT not connected - skipping publish")
            return
            
        try:
            # Create JSON payload
            payload = {
                'temperature': round(temperature, 2),
                'timestamp': datetime.now().isoformat(),
                'unit': 'celsius',
                'sensor': 'DHT11',
                'location': 'Arduino_Station_1'
            }
            
            # Convert to JSON string
            json_payload = json.dumps(payload)
            
            # Publish to MQTT
            result = self.mqtt_client.publish(self.mqtt_topic, json_payload, qos=1)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"📤 Published to MQTT: {json_payload}")
            else:
                print(f"✗ MQTT publish failed with code: {result.rc}")
                
        except Exception as e:
            print(f"✗ Error publishing to MQTT: {e}")

    def display_status(self):
        """Display current system status"""
        print("\n" + "="*60)
        print("🌡️  TEMPERATURE MONITORING SYSTEM STATUS")
        print("="*60)
        print(f"Serial Connection: {'✓ Connected' if self.serial_connection else '✗ Disconnected'}")
        print(f"MQTT Connection:   {'✓ Connected' if self.mqtt_connected else '✗ Disconnected'}")
        print(f"Last Temperature:  {self.last_temperature}°C" if self.last_temperature else "Last Temperature:  No data")
        print(f"MQTT Topic:        {self.mqtt_topic}")
        print("="*60)

    def shutdown(self):
        """Clean shutdown of connections"""
        print("\n🔄 Shutting down connections...")
        
        self.running = False
        
        # Close serial connection
        if self.serial_connection:
            self.serial_connection.close()
            print("✓ Serial connection closed")
        
        # Disconnect MQTT
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            print("✓ MQTT connection closed")
        
        print("✓ Shutdown complete")

    def run(self):
        """Main execution method"""
        print("🚀 Starting IoT Temperature Monitoring System")
        print("Press Ctrl+C to stop\n")
        
        try:
            # Setup connections
            if not self.setup_serial_connection():
                print("Cannot continue without serial connection. Exiting...")
                return False
            
            if not self.setup_mqtt_connection():
                print("⚠️  Continuing without MQTT (data will only display locally)")
            
            # Display initial status
            self.display_status()
            
            # Start reading data
            self.read_serial_data()
            
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
        finally:
            self.shutdown()
        
        return True

def main():
    """Main entry point"""
    try:
        # Create and run the publisher
        publisher = TemperatureMQTTPublisher()
        publisher.run()
        
    except Exception as e:
        print(f"✗ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()