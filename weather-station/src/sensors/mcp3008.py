#!/usr/bin/python3
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import sys

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

def read_data_from_channel(channel):
    data = {}
    if channel < 0 or channel > 7:
        error = "O valor {} nao e um canal valido!\n Indique um valor entre 0 e 7 (Inclusive)".format(channel)
        raise Exception(error)
    data['id'] = channel
    result = AnalogIn(mcp, channel)
    data['adc'] = result.value
    data['voltage'] = result.voltage
    return data

