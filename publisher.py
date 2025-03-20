import paho.mqtt.client as mqtt
import time
import json
import random

# MQTT Broker configuration
BROKER = "broker.hivemq.com"
PORT = 1883
vehicle_id = "vehicle01"
TOPIC = f"vehicle/{vehicle_id}/data/gps"
CLIENT_ID = "publisher_01"

# Initial GPS data
latitude = 22.543096
longitude = 114.057865

# Connect to MQTT Broker
mqtt_client = mqtt.Client(client_id=CLIENT_ID)

print("Connecting to Broker...")
try:
    mqtt_client.connect(BROKER, PORT, 60)
except Exception as e:
    print(f"Connection failed, error: {e}")
    exit()

print("Starting to publish GPS and vibration data...")
mqtt_client.loop_start()

while True:
    latitude += random.uniform(-0.0001, 0.0001)
    longitude += random.uniform(-0.0001, 0.0001)
    vibration_level = round(random.uniform(0, 10), 2)  # Simulate vibration data

    gps_data = {
        "latitude": round(latitude, 6),
        "longitude": round(longitude, 6),
        "vibration_level": vibration_level,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        mqtt_client.publish(TOPIC, json.dumps(gps_data))
        print(f"Published GPS and vibration data: {gps_data}")
    except Exception as e:
        print(f"Error publishing data: {e}")

    time.sleep(5)
