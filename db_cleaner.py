def drop_table():
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("DROP TABLE IF EXISTS accelerometer_data")
    del dbObj
    print("Table 'accelerometer_data' has been dropped.")