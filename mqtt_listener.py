import paho.mqtt.client as mqtt
import json
from datetime import datetime
from db_storer import sensor_Data_Handler

def mqtt_listen():
    MQTT_Broker = "test.mosquitto.org"
    MQTT_Port = 1883
    Keep_Alive_Interval = 45
    MQTT_Topic = "aichurok/accelerometer/data"

    def on_connect(mosq, obj, flags, rc):
        print("Connected to MQTT Broker with result code " + str(rc))
        mqttc.subscribe(MQTT_Topic, 0)

    def on_message(mosq, obj, msg):
        print("MQTT Data Received...")
        print("MQTT Topic: " + msg.topic) 
        json_data = json.loads(msg.payload.decode('utf-8'))
        print("Data: " + str(json_data)) 

        if 'timestamp' not in json_data:
            json_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sensor_Data_Handler(msg.topic,  json.dumps(json_data))

    def on_subscribe(mosq, obj, mid, granted_qos):
        print(f"Subscribed to topic: {MQTT_Topic} with QoS {granted_qos}")

    mqttc = mqtt.Client()

    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe

    mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

    mqttc.loop_start()

    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnected from MQTT Broker.")
        mqttc.loop_stop()
