
import paho.mqtt.client as mqtt
import json

BROKER = "lbe50b88.ala.cn-hangzhou.emqxsl.cn"  # Broker address
PORT = 8883  # Port
TOPIC = "vehicle/gps"  # Topic to subscribe
CLIENT_ID = "subscriber_01"  # Client ID to distinguish clients
USERNAME = "admin"  # Username
PASSWORD = "public"  # Password

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
    client = mqtt.Client(client_id=CLIENT_ID)

    # Set username and password
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

