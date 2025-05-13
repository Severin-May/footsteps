import paho.mqtt.client as mqtt
import json
from datetime import datetime
from db_storer import sensor_Data_Handler
import time
import pandas as pd
from footstep_calculate import calculate_steps, fetch_new_data, DB_NAME, SMOOTHING_WINDOW, PEAK_HEIGHT, PEAK_DISTANCE
import asyncio
import websockets

# Global variables
last_processed_timestamp = None
data_buffer = pd.DataFrame()
step_count = 0

# Coroutine to send data via WebSocket
async def send_websocket_data(step_count, timestamp):
    uri = "ws://localhost:8765"  # WebSocket server URL # ipv4 = 152.66.177.48
    try:
        async with websockets.connect(uri) as websocket:
            message = {
                "step_count": step_count,
                "timestamp": timestamp
            }
            await websocket.send(json.dumps(message))
    except Exception as e:
        print(f"WebSocket send failed: {e}")

def mqtt_listen():
    global last_processed_timestamp, data_buffer, step_count

    MQTT_Broker = "broker.hivemq.com"
    MQTT_Port = 1883
    Keep_Alive_Interval = 45
    MQTT_Topic = "ayush/accelerometer/data" # here put your topic

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

        sensor_Data_Handler(msg.topic, json.dumps(json_data))

    def on_subscribe(mosq, obj, mid, granted_qos):
        print(f"Subscribed to topic: {MQTT_Topic} with QoS {granted_qos}")

    mqttc = mqtt.Client()

    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe

    mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

    mqttc.loop_start()

    try:
        while True:
            new_data_df = fetch_new_data(last_processed_timestamp)
            if not new_data_df.empty:
                data_buffer = pd.concat([data_buffer, new_data_df], ignore_index=True)
                step_count, smoothed_acceleration, current_peaks = calculate_steps(
                    data_buffer.copy(), PEAK_HEIGHT, PEAK_DISTANCE, SMOOTHING_WINDOW
                )
                step_count = len(current_peaks)
                last_processed_timestamp = new_data_df['timestamp'].iloc[-1]
                print(f"Calculated step count: {step_count}, New data points: {len(new_data_df)}")

                # Send to WebSocket
                asyncio.run(send_websocket_data(step_count, str(last_processed_timestamp)))
            else:
                print("No new data.")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnected from MQTT Broker.")
        mqttc.loop_stop()

if __name__ == "__main__":
    mqtt_listen()


