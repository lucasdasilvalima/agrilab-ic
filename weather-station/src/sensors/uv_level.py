#!/usr/bin/python3
from . import mcp3008

def uv_level():

    data = mcp3008.read_data_from_channel (2)
    voltage_in_milli = data['voltage'] * 0.01
    
    if voltage_in_milli < 50:
        UV_index = 0
    elif voltage_in_milli <=317:
        UV_index = 1
    elif voltage_in_milli <=407:
        UV_index = 2
    elif voltage_in_milli <=502:
        UV_index = 3
    elif voltage_in_milli <=603:
        UV_index = 4
    elif voltage_in_milli <=695:
        UV_index = 5
    elif voltage_in_milli <=794:
        UV_index = 6
    elif voltage_in_milli <=880:
        UV_index = 7
    elif voltage_in_milli <=975:
        UV_index = 8
    elif voltage_in_milli <=1078:
        UV_index = 9
    elif voltage_in_milli <=1169:
        UV_index = 10
    elif voltage_in_milli >=1170:
        UV_index = 11
    return UV_index
