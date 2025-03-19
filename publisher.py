import paho.mqtt.client as mqtt
import time
import json

# MQTT Broker configuration
BROKER = "lbe50b88.ala.cn-hangzhou.emqxsl.cn"  # Broker address
PORT = 8883  # Port
TOPIC = "vehicle/gps"  # Topic
CLIENT_ID = "publisher_01"  # Client ID to distinguish clients
USERNAME = "admin"  # Username
PASSWORD = "public"  # Password

# Predefined GPS data
gps_data = {
    "latitude": 22.543096,  # Example latitude
    "longitude": 114.057865,  # Example longitude
    "altitude": 10.0,  # Example altitude
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")  # Current time
}

# Connect to MQTT Broker
mqtt_client = mqtt.Client(client_id=CLIENT_ID)

# Set username and password
mqtt_client.username_pw_set(USERNAME, PASSWORD)

# Connect to Broker
print("Connecting to Broker...")
try:
    mqtt_client.connect(BROKER, PORT, 60)
except Exception as e:
    print(f"Connection failed, error: {e}")
    exit()

print("Starting to publish GPS data...")
mqtt_client.loop_start()  # Start MQTT loop

while True:
    try:
        # Update timestamp
        gps_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        # Send data to MQTT Broker
        mqtt_client.publish(TOPIC, json.dumps(gps_data))
        print(f"Published GPS data: {gps_data}")
    except Exception as e:
        print(f"Error publishing GPS data: {e}")

    time.sleep(5)  # Send data every 5 seconds