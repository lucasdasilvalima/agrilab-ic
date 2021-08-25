from fuzzy_api.utils.requests import Req
from flask_restful import Resource
from flasgger import swag_from
from flask import request

from fuzzy_cmeans import fuzzy_cmeans


class FuzzyById(Resource):
    def __init__(self):
        self.reqs = Req()
        self.fuzzy_method = fuzzy_cmeans.Fuzzy()

    @swag_from('fuzzy_id.yml', validation=True)
    def post(self):
        if not self.reqs.isAtuhenticated:
            return {"error": "You need singin first!"}, 401
        if not self.reqs.validate_auth():
            return {"error": "Your token is invalid!"}, 401

        _request = request.json

        clusters = []
        qty_sensors = _request["qty_sensors"]
        if qty_sensors > len(_request['clusters']):
            for _ in range(qty_sensors):
                for sample_id in _request["clusters"]:
                    response, status = self.reqs.get_sample(sample_id)
                    if status != 200:
                        return response
                    clusters.append(self.fuzzy_method.read_sample_from_api(response))
        else:
            for sample_id in _request["clusters"]:
                    response, status = self.reqs.get_sample(sample_id)
                    if status != 200:
                        return response
                    clusters.append(self.fuzzy_method.read_sample_from_api(response))

        data = []
        for sample_id in _request["data"]:
            response, status = self.reqs.get_samples(sample_id)
            if status != 200:
                return response
            data.append(self.fuzzy_method.read_samples_from_api(response))

        data, clusters = self.fuzzy_method.get_data_and_clusters(
            data, clusters)
        # Necessario se ao inves de passar os clusters quiser que eles sejam gerados automatixamente 
        # obsoleto por enquanto
        limit = _request["limit"]
        

        try:
            fpi, mpe = self.fuzzy_method.fuzzy3(data, clusters)
            return {"fpi": fpi, "mpe": mpe}
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500


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
        print(f"clusters: {clusters}")
        try:
            fpi, mpe = self.fuzzy_method.fuzzy3(data, clusters)
            return {"fpi": fpi, "mpe": mpe}
        except Exception as e:
            print(e)
            return {"error": str(e)}, 501
