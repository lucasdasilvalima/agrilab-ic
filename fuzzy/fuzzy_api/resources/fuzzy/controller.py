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
        _request = request.json

        api_key = request.headers.get("Authorization")

        if not self.reqs.validate_auth(auth_key):
            return {"error": "Your token is invalid!"}, 401


        clusters = []
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

        qty_sensors = _request["qty_sensors"]
        limit = _request["limit"]
        samples = self.fuzzy_method.create_samples(clusters, qty_of_sensors=qty_sensors, limit=limit)
        try:
            per, fpi, mpe = self.fuzzy_method.fuzzy3(data, samples)#clusters)
            return {"pertinencias": per, "fpi": fpi, "mpe": mpe}
        except Exception as e:
            
            return {"error": str(e)}, 500


class Fuzzy(Resource):
    def __init__(self):
        self.reqs = Req()
        self.fuzzy_method = fuzzy_cmeans.Fuzzy()

    @swag_from('fuzzy.yml', validation=True)
    def post(self):
        api_key = request.headers.get("Authorization")
        
        #if not self.reqs.validate_auth(api_key):
        #    return {"error": "Your token is invalid!"}, 401

        r = request.json
        clusters = r['clusters']
        data = r['data']
        limit = r['limit']
        qty_sensors = r['qty_sensors']
        samples = clusters[0]['samples']

        if limit >= len(clusters)/qty_sensors:
            return {"error_msg": "The quantity of clusters divided by qty_of_sensors must be less or equal than limit"}
        
        _data, _clusters = self.fuzzy_method.extract_data_frame(data), self.fuzzy_method.extract_clusters(clusters, qty_of_sensors=qty_sensors, limit=limit)
        
        try:
            fpi, mpe, r_value = self.fuzzy_method.fuzzy3(_data, _clusters, qty_sensors, limit, is_normalize=True)
            return {'values': r_value, "local_by_fpi": fpi, "local_by_mpe": mpe}
        except Exception as e:
            
            return {"error": str(e)}, 501 
