import paho.mqtt.client as mqtt
import random
import json
import time
from datetime import datetime

# ----------------------------
# 1. 电池电量数据模拟类
# ----------------------------
class BatterySimulator:
    """
    模拟电池电量下降过程：
    - 初始电压为4.2V（满电状态）
    - 最低电压设定为3.0V
    - 根据当前电压计算电池百分比（线性映射）
    """
    def __init__(self, initial_voltage=4.2):
        self.voltage = initial_voltage  # 初始电压
        self.min_voltage = 3.0           # 最低工作电压

    def drain_battery(self):
        """
        模拟电池电压下降：
        - 每次随机降低一定电压（范围：0.005V~0.02V）
        - 保证电压不会低于最小值
        - 根据电压计算电池百分比
        """
        drop = random.uniform(0.005, 0.02)
        self.voltage = max(self.min_voltage, self.voltage - drop)
        percentage = int((self.voltage - self.min_voltage) / (4.2 - self.min_voltage) * 100)
        return round(self.voltage, 2), percentage

# ----------------------------
# 2. MQTT 消息发布函数
# ----------------------------
def mqtt_publisher(broker="localhost", port=1883, topic="vehicle/battery", publish_interval=5):
    """
    连接到 MQTT Broker，并定时发布电池状态数据
    参数：
      broker - MQTT Broker 地址（默认localhost）
      port - 端口（默认1883）
      topic - 发布主题（默认"vehicle/battery"）
      publish_interval - 发布间隔秒数（默认5秒）
    """
    # 创建 MQTT 客户端实例
    client = mqtt.Client("BatteryPublisher")
    try:
        client.connect(broker, port, 60)
    except Exception as e:
        print("Unable to connect to MQTT Broker:", e)
        return

    # 实例化电池模拟器
    simulator = BatterySimulator(initial_voltage=4.2)

    # 循环模拟并发布数据
    while True:
        voltage, percentage = simulator.drain_battery()
        battery_status = {
            "device_id": "Bike123",  # 设备唯一标识
            "battery_status": {
                "voltage": voltage,         # 当前电压
                "percentage": percentage,   # 电池百分比
                "charging": False,          # 模拟环境中不检测充电状态
                "timestamp": datetime.utcnow().isoformat() + "Z"  # UTC时间戳
            }
        }
        # 将数据转换为 JSON 格式
        message = json.dumps(battery_status)
        # 通过 MQTT 发布消息
        result = client.publish(topic, message)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Message has been posted:{message}")
        else:
            print("Message posting failed. error code:", result.rc)
        # 按设定间隔等待后再次发布
        time.sleep(publish_interval)

# ----------------------------
# 3. 程序入口
# ----------------------------
if __name__ == "__main__":
    mqtt_publisher()