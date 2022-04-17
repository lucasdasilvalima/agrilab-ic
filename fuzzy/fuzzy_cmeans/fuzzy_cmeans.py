from os import replace
from pandas.core.frame import DataFrame
from requests.api import delete
from constants import ALMOST_ZERO
from functools import reduce

import pandas as pd
import numpy as np


class Fuzzy:
    def __init__(self):
        self.zero = ALMOST_ZERO

    def mpe(self, pertinences, qty_of_cluster, sample_size):

        for c in pertinences.columns:
            pertinences[c] = (
                pertinences[c] * np.log10(pertinences[c]) / sample_size)

        mpe = (-1) * pertinences.sum().sum()
        mpe /= np.log10(qty_of_cluster)
        return mpe

    def fpi(self, pertinences, qty_of_cluster, sample_size):

        for c in pertinences.columns:
            pertinences[c] = np.power(pertinences[c], 2)/sample_size

        fpi = 1 - (qty_of_cluster/(qty_of_cluster-1))
        fpi *= (1 - pertinences.sum().sum())
        return fpi

    def fuzzy3(self, data, clusters, qty_of_cluster, sample_size, is_normalize=True):
        arr_fpi = {}
        arr_mpe = {}
        r_fpi = 0
        r_mpe = 0
        flag_ctrl=0
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
               
                pertinences = pertinences.replace(0, self.zero)
                pertinence[columns] = pertinences.sum(axis=1)
                pertinence[columns] = np.power(pertinence[columns], -1.0)

            fpi_index = self.fpi(pertinence, qty_of_cluster, sample_size)
            mpe_index = self.mpe(pertinence, qty_of_cluster, sample_size)

            if flag_ctrl == 0:
                r_fpi = fpi_index
                r_mpe = mpe_index
            if r_mpe > mpe_index:
                r_mpe = mpe_index
            if r_fpi > fpi_index:
                r_fpi = fpi_index
            flag_ctrl += 1
            arr_fpi[flag_ctrl] = str(indice)
            arr_mpe[flag_ctrl] = str(indice)
        
        return arr_fpi, arr_mpe, {'fpi_value': r_fpi, 'mpe_index': r_mpe}


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

    def normalize_data(self, data):
        
        normalize = data

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
            left, right, right_index=True, left_index=True), data)), (reduce(lambda left, right: pd.merge(left, right,
                                                                                                          right_index=True, left_index=True), clusters))

    def extract_data_and_clusters(self, r_data):
        data = r_data["data"]
        clusters = r_data["clusters"]
        return self.extract_data_frame(data), self.extract_clusters(clusters)

    def get_sample(self, data, qty_of_sensors, offset):
        res = []
        sample ={}
        qty_of_sensors += offset
        for i in range(offset, qty_of_sensors):
            
            sample['LAT'] = data[i]['lat']
            sample['LONG'] = data[i]['long']
            for j in data[i]['samples']:
                sample.update(j)
            res.append(sample)
        return res

    def extract_clusters(self, data, qty_of_sensors=3, limit=100):
        samples = []
        for i in range(limit):
            sample = self.get_sample(data, qty_of_sensors, i)
            
            df = pd.DataFrame(sample)
            df.set_index(['LAT', 'LONG'], inplace=True)
            samples.append(df)

        return samples

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
        for _ in range(qty_of_sensors):
            samples_tmp = pd.DataFrame()
            for __ in range(limit):
                samples_tmp = samples_tmp.append(data.iloc[[]])
            samples.append(data.sample(limit, replace=True))

        return samples
