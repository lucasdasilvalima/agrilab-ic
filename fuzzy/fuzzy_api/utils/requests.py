from constants import DEFAULT_AGDATABOX_ROUTES
from dotenv import load_dotenv

import os
import requests
import json

load_dotenv()

class SingletonMeta(type):
   _instances = {}

   def __call__(cls, *args, **kwargs):
      """
      Possible changes to the value of the `__init__` argument do not affect
      the returned instance.
      """
      if cls not in cls._instances:
         instance = super().__call__(*args, **kwargs)
         cls._instances[cls] = instance
      return cls._instances[cls]


class Req(metaclass=SingletonMeta):
   def __init__(self):
      self.auth_key = ""
      self.isAtuhenticated = False
      self.url_base = os.getenv('URL_API')

      self.routes = DEFAULT_AGDATABOX_ROUTES
      self.headers = {
         'content-type': 'application/json',
         'HOST': 'adb.md.utfpr.edu.br',
         'accept': '*/*'
      }
      self.headers = {}

      self.headers['Authorization'] = self.auth_key

   def auth(self, user_payload):
      url = self.url_base + self.routes["authenticate"]

      response = requests.post(
         url, json=user_payload, headers=self.headers, verify=False)

      if response.status_code == 200:
         self.auth_key = response.text
         self.headers = {}
         self.headers['accept'] = '*/*'
         self.headers['Authorization'] = self.auth_key
         self.isAtuhenticated = True

      return {"Authorization": response.text}, response.status_code

   def validate_auth(self):
      url = self.url_base + self.routes["person"]

      response = requests.get(
         url, headers=self.headers, verify=False)
      if response.status_code == 200:
         self.person = json.loads(response.text)
         return True
      return False
