#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from paho.mqtt import publish
from dotenv import load_dotenv

load_dotenv()
mqtt_username = os.getenv("MQTT_USERNAME")
mqtt_password = os.getenv("MQTT_PASSWORD")
mqtt_broker_ip = os.getenv("MQTT_IP")

authentication={"username": mqtt_username, "password": mqtt_password}

def mqtt_publisher(topic, data):
    publish.single(topic, data, hostname=mqtt_broker_ip, port=1883, auth=authentication, transport="tcp")
