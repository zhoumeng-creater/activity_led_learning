import paho.mqtt.client as mqtt
import json

BROKER = "broker.hivemq.com"  # Broker address
PORT = 1883  # Port
vehicle_id = "vehicle01"
TOPIC = f"vehicle/{vehicle_id}/data/gps"    # Topic to subscribe(统一topic格式)
CLIENT_ID = "subscriber_01"  # Client ID to distinguish clients
USERNAME = False  # Username
PASSWORD = False  # Password

# Connection callback function
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected successfully, return code: {rc}")
        # Subscribe to topic
        client.subscribe(TOPIC)
    else:
        print(f"Connection failed, return code: {rc}")
        # Handle connection failure, e.g., retry

# Message callback function
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")
    visualize_message(msg.payload.decode())

# Function to visualize messages
def visualize_message(message):
    try:
        message_dict = json.loads(message)
        print("Visualization result:")
        for key, value in message_dict.items():
            print(f"{key}: {value}")
    except json.JSONDecodeError:
        print(f"Message content: {message}")

# Main program
def main():
    client = mqtt.Client(
        client_id=CLIENT_ID,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION1)

    # Set username and password
    if USERNAME and PASSWORD:
        client.username_pw_set(USERNAME, PASSWORD)

    # Set connection and message callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to Broker
    print("Connecting to Broker...")
    try:
        client.connect(BROKER, PORT, 60)
    except Exception as e:
        print(f"Connection failed, error: {e}")
        return

    # Start network loop to receive messages
    print("Waiting for messages...")
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

