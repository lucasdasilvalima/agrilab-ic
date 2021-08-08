import mcp3008
import agriconsts

#
#    Este script gerencia o retorno dos dados de direcao do vento da estacao
#    o tipo de dado retornado e um JSON => {'angle': 0|45|90|135|180|225|270|315, 'direction': N|S|L|O|NO|SO|SE|NE}
#

def direction():
    
    data = mcp3008.read_data_from_channel (agriconsts.CHANNEL_DIRECTION_WIND)
    voltage = data['voltage']

    orientation_and_direction_wind = {}
    angle = 0
    wind_direction = 'N'

    if (voltage<=0.27):
        angle = 315
        wind_direction = 'NO'
    elif (voltage<=0.32):
        angle = 270
        wind_direction = 'O'
    elif (voltage<=0.38):
        angle = 225
        wind_direction = 'SO'
    elif (voltage<=0.45):
        angle = 180
        wind_direction = 'S'
    elif (voltage<=0.57):
        angle = 135
        wind_direction = 'SE'
    elif (voltage<=0.75):
        angle = 90
        wind_direction = 'E'
    elif (voltage<=1.25):
        angle = 45
        wind_direction = 'NE'
    else:
        angle = 0
        wind_direction = 'N'
    
    orientation_and_direction_wind['angle'] = angle
    orientation_and_direction_wind['direction'] = wind_direction

    return orientation_and_direction_wind
