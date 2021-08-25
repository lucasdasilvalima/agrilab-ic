from constants import DEFAULT_AGDATABOX_ROUTES
from dotenv import load_dotenv

import os
import requests
import json

load_dotenv()


class SingletonMeta(type):
   _instances = {}

   def __call__(cls, *args, **kwargs):
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
         'accept': '*/*',
         'Authorization': self.auth_key
      }

   def auth(self, user_payload):
      route = self.routes["authenticate"]
      if route:
         url = self.url_base + route
         response = requests.post(url, json=user_payload, headers=self.headers, verify=False)

         if response.status_code == 200:
            self.auth_key = response.text
            self.headers = {}
            self.headers['accept'] = '*/*'
            self.headers['Authorization'] = self.auth_key
            self.isAtuhenticated = True
            return {"Authorization": response.text}, response.status_code
         return response.json(), response.status_code

      return {"status": "yours environment variables is not be set correctly"}, 301

   def get_sample(self, sample_id):
      route = self.routes["sample"]
      
      if route:
         url = self.url_base + route.replace('id', str(sample_id['id']))
         response = requests.get(url, headers=self.headers, verify=False)

         return response.json(), response.status_code
      
      return {"status": "yours environment variables is not be set correctly"}, 301

   def get_samples(self, sample_id):
      route = self.routes["samples"]

      if route:
         url = self.url_base + route
         response = requests.get(url.replace('id', str(sample_id['id'])), headers=self.headers, verify=False)
         return response.json(), response.status_code

      return {"status": "yours environment variables is not be set correctly"}, 301

   def validate_auth(self):
      route = self.routes["person"]

      if route:
         url = self.url_base + route
         response = requests.get(url, headers=self.headers, verify=False)
      
         if response.status_code == 200:
            self.person = json.loads(response.text)
            return True
      return False
