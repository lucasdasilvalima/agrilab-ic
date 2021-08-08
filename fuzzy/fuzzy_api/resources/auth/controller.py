from flasgger import swag_from
from flask_restful import Resource
from flask import request

from fuzzy_api.utils.requests import Req

class Auth(Resource):
  def __init__(self):
    self.reqs = Req()
  
  @swag_from('auth.yml', validation=True)
  def post(self):
    return self.reqs.auth(request.json)
