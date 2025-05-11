import sqlite3

def db_init():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accelerometer_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x_axis REAL,
            y_axis REAL,
            z_axis REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

    print("✅ SQLite Database is ready!")