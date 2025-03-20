import paho.mqtt.client as mqtt
import json
import time

BROKER = "broker.hivemq.com"
PORT = 1883
vehicle_id = "vehicle01"
TOPIC = f"server/alert/{vehicle_id}"
CLIENT_ID = "subscriber_alert_01"

# Connection callback function
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected successfully to topic '{TOPIC}', return code: {rc}")
        client.subscribe(TOPIC)
    else:
        print(f"Connection failed, return code: {rc}")

# Message callback function
def on_message(client, userdata, msg):
    print(f"\n[ALERT RECEIVED at {time.strftime('%Y-%m-%d %H:%M:%S')}]")
    process_alert_message(msg.payload.decode())

# Function to process and visualize alert messages
def process_alert_message(message):
    try:
        alert = json.loads(message)
        alert_type = alert.get('alert_type', 'Unknown')
        value = alert.get('value', 'N/A')
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(alert.get('timestamp', time.time())))
        
        print(f"Alert Type   : {alert_type}")
        print(f"Value        : {value}")
        print(f"Alert Time   : {timestamp}")

    except json.JSONDecodeError:
        print(f"Received non-JSON message: {message}")

# Main program
def main():
    client = mqtt.Client(client_id=CLIENT_ID, callback_api_version=mqtt.CallbackAPIVersion.VERSION1)

    client.on_connect = on_connect
    client.on_message = on_message

    print("Connecting to Broker...")
    try:
        client.connect(BROKER, PORT, 60)
    except Exception as e:
        print(f"Connection failed, error: {e}")
        return

    print("Waiting for alert messages...")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Program terminated by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.disconnect()
        print("Disconnected")

if __name__ == "__main__":
    main()
