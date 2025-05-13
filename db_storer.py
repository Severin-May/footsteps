import json
import sqlite3

DB_Name = "sensor_data.db"

class DatabaseManager():
    def __init__(self):
        self.conn = sqlite3.connect(DB_Name)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()
        
    def add_del_update_db_record(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def __del__(self):
        self.cur.close()
        self.conn.close()

def accelerometer_data_handler(jsonData):
    json_Dict = json.loads(jsonData)
    Data_and_Time = json_Dict['timestamp']
    x_axis = json_Dict['x']
    y_axis = json_Dict['y']
    z_axis = json_Dict['z']
    
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("INSERT INTO accelerometer_data (timestamp, x_axis, y_axis, z_axis) VALUES (?, ?, ?, ?)", [Data_and_Time, x_axis, y_axis, z_axis])
    del dbObj
    print("Inserted Accelerometer Data into Database.")
    print("")

def sensor_Data_Handler(Topic, jsonData):
    if Topic == "ayush/accelerometer/data":
        accelerometer_data_handler(jsonData)