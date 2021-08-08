# a Biblioteca board nos fornece as constants para os canas GPIO do raspberry
import board
import math as MATH

# Canais dos sensores ligados ao mcp3008
# O canal do mcp3008 varia de 0 - 7, sao ao todo 8 canais e, neste caso, usamos apenas 3
CHANNEL_SENSOR_UV       =   0
CHANNEL_DIRECTION_WIND  =   1


# Canais dos sensores ligados ao GPIO do raspberry
CHANNEL_SPEED_WIND    = board.D21
CHANNEL_PLUVIOMETRIC  = board.D18

# Configuracao para o MQTT Publisher
MQTT_BROKER         =   "192.168.0.105"
MQTT_PORT           =   1883
KEEP_ALIVE_INTERVAL =   45
MQTT_MAIN_TOPIC     =   "agrisstation/"

# Configuracoes para o sensor de velocidade do vento (wind speed)
RADIUS_IN_M   = .147
CIRCUNFERENCE = 2 * MATH.pi * RADIUS_IN_M
INTERVAL_OF   = 45
ADJUSTMENT    = 2.3

# Tempo de espera em segundos
TIME_WAIT_WIND_SPEED = 10
MASK_TIME = '%m/%d/%y %H:%M:%S'
