#!/usr/bin/python3
import time
import board
import adafruit_dht
import logging

class Dht22:

    def __init__(self, digital_pin = board.D18):
        # Initial the dht device, with data pin connected to:
        self.dhtDevice = adafruit_dht.DHT22(digital_pin)
    
    def get_temperature_fahrenheit(self):
        temperature_c = self.get_temperature_celsius()
        temperature_f = (temperature_c if (temperature_c != None) else 0) * (9 / 5) + 32
        return temperature_f

    def get_temperature_celsius(self):
        try:
            temperature_c = self.dhtDevice.temperature
            return temperature_c
        except RuntimeError as error:
            logging.error(error)
            return None
    
    def get_humidity(self):
        try:
            humidity = self.dhtDevice.humidity
            return humidity
        except RuntimeError as error:
            logging.error(error)
            return None

    def get_data(self):
        temperature_c = self.get_temperature_celsius()
        temperature_f = self.get_temperature_fahrenheit()
        humidity = self.get_humidity()
        data = { "temperature_f": temperature_f, "temperature_c": temperature_c, "humidity": humidity }
        return data