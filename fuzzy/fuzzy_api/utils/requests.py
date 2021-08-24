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
      self.auth_key = "eyJhbGciOiJIUzUxMiJ9.eyJwZXJtcyI6e30sImlkIjoiMTk3IiwiZXhwIjoxNjI5OTAwNjQwfQ.froSAbbvG6sv5wnzs0HJRzhbPijhXWGKt5xnSVJ3o2zNOwxJ1EgH2f_gC-a5YIGPBMeK-y6sI1HGsLMSg_nz5A"
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

   def get_sample(self, sample_id):

      url = self.url_base + self.routes["sample"]

      response = requests.get(url.replace('id', str(sample_id['id'])), headers=self.headers, verify=False)
      if response.status_code == 200:
         try:
            return response.json()
         except:
            return {"warn": "response not valid"}

      return {"error": response.text}

   def get_samples(self, sample_id):

      url = self.url_base + self.routes["samples"]
      
      response = requests.get(url.replace('id', str(sample_id['id'])), headers=self.headers, verify=False)
      if response.status_code == 200:
         try:
            return response.json()
         except:
            return {"warn": "response not valid"}

      return {"error": response.text}

   def validate_auth(self):
      url = self.url_base + self.routes["person"]

      response = requests.get(
         url, headers=self.headers, verify=False)
      if response.status_code == 200:
         self.person = json.loads(response.text)
         return True
      return False
