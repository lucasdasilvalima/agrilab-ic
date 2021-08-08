#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sensors import (bmp180, dht22, uv_level)
from mqtt.mqtt_server import mqtt_publisher
from dotenv import load_dotenv

from time import sleep

def publish_data(topic, data):
    # When the data is recive need format that data 
    mqtt_publisher("agristation/{}".format(topic), str(data))

if __name__ == "__main__":
    load_dotenv()
    bmp = bmp180.bmp180(0x77)
    dht = dht22.Dht22()
    while(True):
        sleep(300)
        uv  = {"uv_level": uv_level.uv_level()}
        publish_data("uv_level", uv)

        dht_data = dht.get_data()
        
        temp = {"temperature": dht_data["temperature_c"]}
        publish_data("temperature", temp)

        humidity = { "humidity": dht_data["humidity"] }
        publish_data("umidity")
        
        bmp_data = bmp.get_data()
        
        pressure = { "atm_pressure": bpm_data["pressure"] }
        publish_data("atm_pressure", pressure )
    
        # Sim temos daddos redundantes!
        temperature = { "temperature": bpm_data["temperature"] }
        publish_data("temperature", bpm_data["temperature"])

        altitude = { "altitude": bpm_data["altitude"] }
        publish_data("altitude", altitude)
