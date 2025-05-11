from db_initializer import db_init
from mqtt_listener import mqtt_listen

def main():
    print("Program started...")
    db_init()
    mqtt_listen()
    print("Program ended!")

if __name__ == "__main__":
    main()
