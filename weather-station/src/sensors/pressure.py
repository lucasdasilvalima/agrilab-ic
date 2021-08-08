import Adafruit_BMP_BMP085 as sensor_controller

bmp085 = sensor_controller.BMP085()

def temperature():
    data = {}
    temp = bmp085.read_pressure()
    data['temperature'] = temp
    return data
