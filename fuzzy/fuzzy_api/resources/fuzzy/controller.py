from fuzzy_api.utils.requests import Req
from flask_restful  import Resource
from flasgger       import swag_from
from flask          import request

from fuzzy_cmeans import fuzzy_cmeans

class Fuzzy(Resource):
    def __init__(self):
        self.reqs = Req()
        self.fuzzy_method = fuzzy_cmeans.Fuzzy()

    @swag_from('fuzzy.yml', validation=True)
    def post(self):
        if not self.reqs.isAtuhenticated:
            return {"error": "You need singin first!"}, 500
        if not self.reqs.validate_auth():
            return {"error": "Your token is invalid!"}, 500

        r = request.json
        
        data, clusters = self.fuzzy_method.extract_data_and_clusters(r)
        
        try:
            fpi, mpe = self.fuzzy_method.fuzzy3(data, clusters)
            return {"fpi": fpi, "mpe": mpe}
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500