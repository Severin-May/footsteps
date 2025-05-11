import paho.mqtt.client as mqtt
import json
import time

MQTT_Broker = "test.mosquitto.org"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "aichurok/accelerometer/data"

mqttc = mqtt.Client()
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

# Sample data to send
data = {
    "x": 1.23,
    "y": 2.34,
    "z": 3.45,
    "timestamp": "2025-05-11 10:30:00"
}

while True:
    json_data = json.dumps(data)
    mqttc.publish(MQTT_Topic, json_data)
    print(f"Published: {json_data} to Topic: {MQTT_Topic}")
    time.sleep(5)  # Publish every 5 seconds
