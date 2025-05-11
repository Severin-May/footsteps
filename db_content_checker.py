import sqlite3
import pandas as pd
# Connect to SQLite DB
conn = sqlite3.connect('sensor_data.db')
# cursor = conn.cursor()
# cursor.execute("DROP TABLE IF EXISTS accelerometer_data;")s

df = pd.read_sql("SELECT * FROM accelerometer_data", conn)

print(df)

conn.close()
