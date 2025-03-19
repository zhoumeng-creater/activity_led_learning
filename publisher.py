import paho.mqtt.client as mqtt
import time
import json
import random

# MQTT Broker configuration
BROKER = "lbe50b88.ala.cn-hangzhou.emqxsl.cn"  # Broker address
PORT = 8883  # Port
vehicle_id = "vehicle01"
TOPIC = f"vehicle/{vehicle_id}/data/gps"  # Topic to publish（统一topic格式）
CLIENT_ID = "publisher_01"  # Client ID to distinguish clients
USERNAME = "admin"  # Username
PASSWORD = "public"  # Password

# Predefined GPS data

# 初始值
latitude = 22.543096
longitude = 114.057865

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
    # 模拟经纬度小范围随机变化
    latitude += random.uniform(-0.0001, 0.0001)
    longitude += random.uniform(-0.0001, 0.0001)
    
    gps_data = {
        "latitude": round(latitude, 6),
        "longitude": round(longitude, 6),
        "altitude": round(10 + random.uniform(-0.5, 0.5), 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        # Send data to MQTT Broker
        mqtt_client.publish(TOPIC, json.dumps(gps_data))
        print(f"Published GPS data: {gps_data}")
    except Exception as e:
        print(f"Error publishing GPS data: {e}")

    time.sleep(5)  # Send data every 5 seconds