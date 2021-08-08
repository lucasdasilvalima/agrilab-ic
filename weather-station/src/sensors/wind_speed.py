from gpiozero import DigitalInputDevice
import agriconsts as agriconsts
import datetime
# Este script gerencia o sensor de velocidade do vento
# para capturar os dados deste sensor impor wind_speed
# Para mudar as configuracoes de portas GPIO mude agriconsts.py

class WindSpeed:
  count = 0
  time_interval_in_seconds = 0
  time_intervals = []

  def __init__(self):
    self.count = 0
    self.time_interval_in_seconds = 0

  def reset_count_and_time(self):
    self.count = 0
    self.time_interval_in_seconds = 0
    self.time_intervals.clear()

  def when_actived(self):
    self.count += 1
    self.time_intervals.append(datetime.datetime.now())

  def calculate_speed(self):
    data = {}

    # Capturar dados do tmepo
    last_index = (len(self.time_intervals) - 1)
    # Operdor ternario
    last_index = 0 if last_index < 0 else last_index
    start_time = self.time_intervals[0]
    end_time = self.time_intervals[last_index]
    # Calculo do intervalo de tempo
    self.time_interval_in_seconds = end_time.second - start_time.second

    # Calcular a distancia percorrida
    # Entenda count como a quantidade de rotacao
    distance = self.count * agriconsts.CIRCUNFERENCE
    # Calcula da velocidade
    speed_wind_m_per_seconds = distance / self.time_interval_in_seconds
    # Aplica um ajuste por causa do peso das conchas
    speed_wind_m_per_seconds *= agriconsts.ADJUSTMENT

    # Populando o objeto
    data['start_time'] = start_time.strftime('%m/%d/%y %H:%M:%S')
    data['end_time'] = end_time.strftime('%m/%d/%y %H:%M:%S')
    data['speed_m_s'] = speed_wind_m_per_seconds
    data['speed_km_h'] = speed_wind_m_per_seconds * 3.6
    return data

