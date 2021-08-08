import datetime
from sensors import agriconsts
# Este script gerencia o sensor de preciptacao da chuva
# para capturar os dados deste sensor import pliviometric
# Para mudar as configuracoes de portas GPIO mude agriconsts.py

class Pluviometric:
  count = 0
  start_time = datetime.datetime.now()
  end_time = datetime.datetime.now()

  def __init__(self):
    self.count = 0

  def reset_variables(self):
    self.count = 0
    self.start_time = datetime.datetime.now()
    self.end_time = datetime.datetime.now()

  def when_actived(self):
    if self.count == 0:
      self.start_time = datetime.datetime.now()
    self.count += 0.25


  def calculate_rain_volume(self):
    self.end_time = datetime.datetime.now()

    data = {}

    data['rain_volume'] = self.count
    data['start_time']  = self.start_time.strftime(agriconsts.MASK_TIME)
    data['end_time']  = self.end_time.strftime(agriconsts.MASK_TIME)
    self.reset_variables()
    return data

