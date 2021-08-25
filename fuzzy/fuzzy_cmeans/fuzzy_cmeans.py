from pandas.core.frame import DataFrame
from requests.api import delete
from constants import ALMOST_ZERO
from functools import reduce

import pandas as pd
import numpy as np


class Fuzzy:
    def __init__(self):
        self.zero = ALMOST_ZERO

    def mpe(self, pertinences):
        qty_of_cluster = len(pertinences)
        sample_size = len(pertinences.columns)

        for c in pertinences.columns:
            pertinences[c] = (
                pertinences[c] * np.log10(pertinences[c]) / sample_size)

        mpe = (-1) * pertinences.sum().sum()
        mpe /= np.log10(qty_of_cluster)
        return mpe

    def fpi(self, pertinences):

        qty_of_cluster = len(pertinences)
        sample_size = len(pertinences.columns)

        for c in pertinences.columns:
            pertinences[c] = np.power(pertinences[c], 2)/sample_size

        fpi = 1 - (qty_of_cluster/(qty_of_cluster-1))
        fpi *= (1 - pertinences.sum().sum())
        return fpi

    def fuzzy3(self, data, clusters, qty_sensors=-1):
        arr_fpi = {}
        arr_mpe = {}
        arr_per = {}
        print(len(clusters))
        for indice, cluster in enumerate(clusters):
            dists = pd.DataFrame()
            for indice, row in cluster.iterrows():
                dist = pd.DataFrame()
                for x in data.columns:
                    dist[x] = data[x]-row[x]
                    dist[x] = np.power(dist[x], 2)

                dist = dist.sum(axis=1)
                dist = dist.replace(0, self.zero)
                dists[indice] = np.sqrt(dist)
            pertinence = pd.DataFrame()

            for columns in dists.columns:
                pertinences = pd.DataFrame()
                for columns_aux in dists.columns:
                    pertinences[columns_aux] = np.power(
                        (dists[columns] / dists[columns_aux]), (1.0/3.0))

                pertinence[columns] = pertinences.sum(axis=1)
                pertinence[columns] = np.power(pertinence[columns], -1.0)

            fpi_index = self.fpi(pertinence)
            mpe_index = self.mpe(pertinence)
            arr_per[indice] = pertinence.to_json(orient='records')
            arr_fpi[indice] = fpi_index
            arr_mpe[indice] = mpe_index

        return arr_per, arr_fpi, arr_mpe

    def load_raw_data(self):
        self.data_frame = pd.DataFrame(self.raw_data)

    def read_sample_from_api(self, data):
        if not data:
            return None

        data = {'value': [data['value']], 'geometry': [data['geometry']]}
        df = pd.DataFrame(data)
        df['geometry'] = df['geometry'].str.split(
            'POINT', n=1, expand=True)[1].str[1:-1]
        df.set_index('geometry', inplace=True)
        return df

    def read_samples_from_api(self, data):
        if not data:
            return None

        df = pd.DataFrame(data)
        df = df.get(['value', 'geometry'])
        df['geometry'] = df['geometry'].str.split(
            'POINT', n=1, expand=True)[1].str[1:-1]
        df.set_index('geometry', inplace=True)
        return df

    def normalize_data(self):
        self.load_raw_data()
        normalize = self.data_frame

        array_centroid = []

        for x in normalize.columns:
            max_value = normalize[x].max()
            min_value = normalize[x].min()
            variance = max_value - min_value
            array_centroid.append(
                {'max': max_value, 'min': min_value, 'variance': variance, 'column': x})
            normalize[x] = (normalize[x] - min_value) / (variance)
        return normalize, array_centroid

    def get_data_and_clusters(self, data, clusters):
        return (reduce(lambda left, right: pd.merge(
            left, right, right_index=True, left_index=True), data)), [(reduce(lambda left, right: pd.merge(left, right,
                                                                                                          right_index=True, left_index=True), clusters))]

    def extract_data_and_clusters(self, r_data):
        data = r_data["data"]
        clusters = r_data["clusters"]
        return self.extract_data_frame(data), self.extract_clusters(clusters)

    def extract_clusters(self, data):
        raw_data = []
        for i in data:
            values = {}
            for j in i["samples"]:
                values.update(j)
            raw_data.append(pd.DataFrame(
                values, index=[str(i["lat"]) + ", " + str(i["long"])]))

        return raw_data

    def extract_data_frame(self, data):
        self.raw_data = pd.DataFrame()
        for i in data:
            values = {}
            for j in i["samples"]:
                values.update(j)

            self.raw_data = self.raw_data.append(pd.DataFrame(
                values, index=[str(i["lat"]) + ", " + str(i["long"])]))

        return self.raw_data

    def create_samples(self, data, qty_of_sensors=3, limit=100):
        samples = []
        for _ in range(limit):
            samples.append(data.sample(qty_of_sensors))
        return samples
