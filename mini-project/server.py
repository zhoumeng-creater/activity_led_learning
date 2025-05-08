
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
车辆防盗与追踪系统 - 服务器端程序（连接云端 Broker 版）

功能：
1. 订阅车辆端发布的GPS/震动数据
2. 若震动值超过阈值，向 server/alert/<vehicle_id> 发布告警
3. 订阅用户端指令，并将其转发给 server/command/<vehicle_id>

注意事项：
- 替换 BROKER_HOST / BROKER_PORT 为实际云端地址和端口
- 若需TLS/SSL或认证，参考 main() 中相关配置
"""

import json
import time
import re
import paho.mqtt.client as mqtt
import ssl

# MQTT Broker 云端配置
BROKER_HOST = "broker.hivemq.com"
BROKER_PORT = 1883
BROKER_USERNAME = False
BROKER_PASSWORD = False

USE_TLS = False
CA_CERTS_PATH = "ca.crt"

VEHICLE_DATA_TOPIC = "vehicle/+/data/#"
USER_COMMAND_TOPIC = "client/command/#"

VIBRATION_THRESHOLD = 7

SERVER_CLIENT_ID = "ServerSubscriberCloud"

def on_connect(client, userdata, flags, rc):
    """连接到Broker后的回调，订阅必要的Topic"""
    if rc == 0:
        print("[SERVER] Connected to Cloud MQTT Broker!")
    else:
        print(f"[SERVER] Failed to connect. Return code={rc}")

    client.subscribe(VEHICLE_DATA_TOPIC)
    print(f"[SERVER] Subscribed to topic: {VEHICLE_DATA_TOPIC}")

    client.subscribe(USER_COMMAND_TOPIC)
    print(f"[SERVER] Subscribed to topic: {USER_COMMAND_TOPIC}")

def on_message(client, userdata, msg):
    """收到消息后的回调，根据Topic进行相应处理"""
    topic = msg.topic
    payload_str = msg.payload.decode('utf-8', errors='ignore')

    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        print(f"[SERVER] Invalid data on {topic}: {payload_str}")
        return

    if topic.startswith("vehicle/"):
        handle_vehicle_data(client, topic, payload)
    elif topic.startswith("client/command/"):
        handle_user_command(client, topic, payload)

def handle_vehicle_data(client, topic, payload):
    """处理车辆数据，超出震动阈值时发送告警"""
    match = re.match(r"^vehicle/([^/]+)/data/.+$", topic)
    if not match:
        print(f"[SERVER] Could not extract vehicle_id from topic: {topic}")
        return

    vehicle_id = match.group(1)
    print(f"[SERVER] <Vehicle={vehicle_id}> Payload={payload}")

    if payload.get("vibration_level", 0) > VIBRATION_THRESHOLD:
        alert_topic = f"server/alert/{vehicle_id}"
        alert_msg = {
            "alert_type": "high_vibration",
            "value": payload["vibration_level"],
            "timestamp": time.time()
        }
        client.publish(alert_topic, json.dumps(alert_msg))
        print(f"[SERVER] -> Published ALERT to {alert_topic}: {alert_msg}")

def handle_user_command(client, topic, payload):
    """处理用户端命令并转发到相应的车辆"""
    match = re.match(r"^client/command/([^/]+)$", topic)
    if not match:
        print(f"[SERVER] Could not extract vehicle_id from topic: {topic}")
        return

    vehicle_id = match.group(1)
    forward_topic = f"server/command/{vehicle_id}"
    client.publish(forward_topic, json.dumps(payload))
    print(f"[SERVER] -> Forwarded command to {forward_topic}: {payload}")

def main():
    """主程序入口，连接云端Broker，启用TLS/SSL及认证"""
    client = mqtt.Client(
        client_id=SERVER_CLIENT_ID,         
        callback_api_version=mqtt.CallbackAPIVersion.VERSION1)             # 修复回调函数参数问题

    if BROKER_USERNAME and BROKER_PASSWORD:
        client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)

    if USE_TLS:
        client.tls_set(ca_certs=CA_CERTS_PATH, tls_version=ssl.PROTOCOL_TLS)
        print("[SERVER] TLS/SSL enabled.")

    client.on_connect = on_connect
    client.on_message = on_message

    print(f"[SERVER] Connecting to Cloud Broker at {BROKER_HOST}:{BROKER_PORT} ...")
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    client.loop_forever()

if __name__ == "__main__":
    main()