# -*- coding: utf-8 -*-
from gpiozero import DigitalInputDevice
import Adafruit_BMP.BMP085 as BMP085
import paho.mqtt.client as mqtt
import random, threading, json
import Adafruit_DHT as dht
from time import sleep
import spidev
import math

tempo_sleep = 240

Id_Sensor = 'SensorMet'
#====================================================
# Configurações do MQTT 
MQTT_Broker = "192.168.0.105"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic_Sensor01 = "Sensores/SensorMet"
#====================================================
#coneção com o broker

def on_connect(client, userdata, rc):
    if rc != 0:
        pass
        print ("Unable to connect to MQTT Broker....")
    else:
        print ("Connected with MQTT Broker: " + str(MQTT_Broker))

def on_publish(client, userdata, mid):
    pass

def on_disconnect(client, userdata, rc):
    if rc !=0:
        pass


#===========================================================#
#configuracao Velocidade do vento
count = 0
radius_cm = 14.7    #Radius of the anemometer
interval  = 45       #How often to report speed
ADJUSTMENT = 2.3   #Adjustment of weight of cups
CM_IN_A_KM = 100000.0
SECS_IN_AN_HOUR = 3600

#===========================================================#

#contador MM de chuva
count_mm = 0
#===========================================================#
#atribuicao do sensor BMP180
sensor_bmp = BMP085.BMP085()

#===========================================================#

#Configuracao SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000
canal_dir_vento = 1
canal_sensorUV = 0

#leitura do valor de entrada do MCP3008
def leitura(channel):
    if channel > 7 or channel <0:
        return -1
    r = spi.xfer([1, (8 + channel) << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

#Conversao do valor de entrada do MCP3008
def convertVoltage(bitValue, decimalPlaces):
    voltage = bitValue*(5.0/float(1023))
    voltage = round(voltage, decimalPlaces)
    return voltage


#funcao que retorna a direcao do Vento
def direcao():
    dados = leitura(canal_dir_vento)
    voltagem = convertVoltage(dados,2)
    if (voltagem<=0.27):
        Winddir = 315
        SentidoVento = 'NO'
        return SentidoVento
    elif (voltagem<=0.32):
        Winddir = 270
        SentidoVento = 'O'
        return SentidoVento
    elif (voltagem<=0.38):
        Winddir = 225
        SentidoVento = 'SO'
        return SentidoVento
    elif (voltagem<=0.45):
        Winddir = 180
        SentidoVento = 'S'
        return SentidoVento
    elif (voltagem<=0.57):
        Winddir = 135
        SentidoVento = 'SE'
        return SentidoVento
    elif (voltagem<=0.75):
        Winddir = 90
        SentidoVento = 'E'
        return SentidoVento
    elif (voltagem<=1.25):
        Winddir = 45
        SentidoVento = 'NE'
        return SentidoVento
    else:
        Winddir = 0
        SentidoVento = 'N'
        return SentidoVento

#===========================================================#
#Funcao Calcula o nivel de Radiacao UV
def Calcula_nivel_UV():
    uv_valor=leitura(canal_sensorUV)
    tensao = (uv_valor * 5.0) / float(1023)
    tensao = round(tensao,4)
    tensao = int(tensao*1000)
    
    if 0<= tensao <=50:
        UV_index = 0
        return UV_index
    if 51<= tensao <=226:
        UV_index = 1
        return UV_index
    if 227<= tensao <=317:
        UV_index = 1
        return UV_index
    if 318<= tensao <=407:
        UV_index = 2
        return UV_index
    if 408<= tensao <=502:
        UV_index = 3
        return UV_index
    if 503<= tensao <=603:
        UV_index = 4
        return UV_index
    if 604<= tensao <=695:
        UV_index = 5
        return UV_index
    if 696<= tensao <=794:
        UV_index = 6
        return UV_index
    if 795<= tensao <=880:
        UV_index = 7
        return UV_index
    if 881<= tensao <=975:
        UV_index = 8
        return UV_index
    if 976<= tensao <=1078:
        UV_index = 9
        return UV_index
    if 1079<= tensao <=1169:
        UV_index = 10
        return UV_index
    if tensao >=1170:
        UV_index = 11
        return UV_index


#===========================================================#
# Funcao que calcula a velocidade do vento
def calculate_speed():
    global count
    global tempo_sleep
    circunference_cm = (2 * math.pi) * radius_cm
    rotations = count

    dist_km = (circunference_cm * rotations)/CM_IN_A_KM

    km_per_sec = dist_km / tempo_sleep
    km_per_hour = km_per_sec * SECS_IN_AN_HOUR

    velocidade = km_per_hour * ADJUSTMENT 

    return velocidade

#procedimento que faz a contagem de quantas voltas o sensor de vento deu
def spin():
    global count
    count = count + 1
    print(count)


#===========================================================#
#procedimento que faz a contagem de quantas vezes o sensor de chuva foi acionado
#Cada vez que e acionado e contado 0.25 mm de chuva

def mm():
    global count_mm
    count_mm = count_mm + 0.25
    print(count_mm)
#===========================================================#

def bmp():
    temperatura = sensor_bmp.read_temperature()
    pressao = sensor_bmp.read_pressure()
    altitude = sensor_bmp.read_altitude()
    pressao_Mar = sensor_bmp.read_sealevel_pressure()
    return temperatura, pressao, altitude, pressao_Mar
'''
    
    print ('Temp = {0:0.2f} *C'.format(temperatura)) # Temperature in Celcius
    print ('Pressure = {0:0.2f} Pa'.format(pressao)) # The local pressure
    print ('Altitude = {0:0.2f} m'.format(altitude)) # The current altitude
    print ('Sealevel Pressure = {0:0.2f} Pa'.format(pressao_Mar)) # The sea-level pressure
'''
#===========================================================#
def DHT():
    try:
        h,t = dht.read_retry(dht.DHT22,24)
        return h,t
    except:
        return 0,0
        pass
    #print ('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(t,h))

#===========================================================#

Sensor_chuva = DigitalInputDevice(18)
Sensor_chuva.when_activated = mm
wind_speed_sensor = DigitalInputDevice(21)
wind_speed_sensor.when_activated = spin
#===========================================================#
#inicializando o mqtt
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish


def publish_To_Topic(topic, message):
    mqttc.publish(topic, message)
    print("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
    print ("")


#===========================================================#

#Funcao que publica os dados no servidor
def publish_Sensor_Values_to_MQTT(count_ml):
    temperatura, pressao, altitude, pressao_Mar = bmp()
    hu, temp = DHT()
    velVento = round(calculate_speed(),2)
    
      
    SensorMet_Data = {}
    SensorMet_Data['Sensor_ID'] = Id_Sensor
    SensorMet_Data['VolumeChuva'] = count_ml
    SensorMet_Data['VelocidadeVento'] = velVento
    SensorMet_Data['DirecaoVento'] = direcao()
    SensorMet_Data['NivelRadiacao'] = Calcula_nivel_UV()
    SensorMet_Data['Temperatura'] = temp
    SensorMet_Data['PressaoAr'] = pressao
    SensorMet_Data['Altitude'] = altitude
    SensorMet_Data['PressaoMar'] = pressao_Mar
    SensorMet_Data['Umidade'] = hu
    SensorMet_json_Data = json.dumps(SensorMet_Data)
    print("Publishing Sensor values.... ")
    mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
    publish_To_Topic(MQTT_Topic_Sensor01, SensorMet_json_Data)

#===========================================================#

while True:
    count = 0
    count_mm = 0
    sleep(tempo_sleep)
    try:
        publish_Sensor_Values_to_MQTT(count_mm)
    except IOError as e:
        pass


