import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import sqlite3

DB_NAME = 'sensor_data.db'
TABLE_NAME = 'accelerometer_data'
SMOOTHING_WINDOW = 5
PEAK_HEIGHT = 10
PEAK_DISTANCE = 20

def calculate_steps(df, height_threshold, distance_threshold, smoothing_window):
    """Calculates the number of steps from accelerometer data."""
    if df.empty:
        return 0, np.array([]), []
    df['acc_mag'] = np.sqrt(df['x_axis']**2 + df['y_axis']**2 + df['z_axis']**2)
    df['acc_mag_smooth'] = df['acc_mag'].rolling(window=smoothing_window, min_periods=1).mean().fillna(0)
    peaks, _ = find_peaks(df['acc_mag_smooth'], height=height_threshold, distance=distance_threshold)
    return len(peaks), df['acc_mag_smooth'], peaks

def fetch_new_data(last_timestamp):
    """Fetches new accelerometer data from the database."""
    conn = sqlite3.connect(DB_NAME)
    query = f"SELECT x_axis, y_axis, z_axis, timestamp FROM {TABLE_NAME}"
    if last_timestamp:
        query += " WHERE timestamp > ?"
        df = pd.read_sql_query(query + " ORDER BY timestamp", conn, params=(last_timestamp,))
    else:
        df = pd.read_sql_query(query + " ORDER BY timestamp", conn)
    conn.close()
    return df
