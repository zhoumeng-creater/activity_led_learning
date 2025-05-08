import paho.mqtt.client as mqtt
import json

# ----------------------------
# 1. 模拟数据库存储
# ----------------------------
# 使用列表模拟数据库存储接收到的电池数据
database = []

def store_to_database(battery_data):
    """
    模拟将接收到的电池数据存储到数据库中。
    这里使用全局列表 database 模拟数据库存储，并打印存储记录。
    """
    database.append(battery_data)
    print("Store data to a database:", battery_data)

# ----------------------------
# 2. 电池状态分析函数
# ----------------------------
def analyze_battery_status(battery_data):
    """
    分析电池状态：
    - 当电池百分比低于20%时发出低电量预警
    - 当电池百分比低于5%时发出紧急预警
    """
    percentage = battery_data.get("battery_status", {}).get("percentage", 100)
    alerts = []
    if percentage < 20:
        alerts.append("Low battery warning: Battery level below 20 per cent")
    if percentage < 5:
        alerts.append("Emergency Warning: Battery level is below 5%, please maintain immediately!")
    return alerts

# ----------------------------
# 3. MQTT 回调函数
# ----------------------------
def on_connect(client, userdata, flags, rc):
    """
    当客户端成功连接到 MQTT Broker 后，订阅指定的主题。
    """
    if rc == 0:
        print("订阅者成功连接到 MQTT Broker")
        client.subscribe("vehicle/battery")
    else:
        print("Connection to MQTT Broker failed. error code:", rc)

def on_message(client, userdata, msg):
    """
    每当接收到消息时：
      - 解码消息内容并转换为 JSON 数据
      - 分析电池状态，输出预警信息（如有）
      - 模拟将数据存储到数据库
    """
    try:
        payload_str = msg.payload.decode("utf-8")
        print(f"Message {payload_str} received from topic {msg.topic}")
        battery_data = json.loads(payload_str)
        alerts = analyze_battery_status(battery_data)
        for alert in alerts:
            print("warning information:", alert)
        store_to_database(battery_data)
    except Exception as e:
        print("Error processing a message:", e)

# ----------------------------
# 4. MQTT 订阅者主函数
# ----------------------------
def mqtt_subscriber(broker="localhost", port=1883):
    """
    连接到 MQTT Broker 并订阅 "vehicle/battery" 主题，
    持续监听消息，并调用相应回调函数进行数据处理和存储。
    """
    client = mqtt.Client("BatterySubscriber")
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(broker, port, 60)
    except Exception as e:
        print("Unable to connect to MQTT Broker:", e)
        return
    
    # 进入阻塞循环，持续监听消息
    client.loop_forever()

# ----------------------------
# 5. 程序入口
# ----------------------------
if __name__ == "__main__":
    mqtt_subscriber()