# -*- coding: utf-8 -*-
#bXPCSiqPfiUNcVKTJzPz

import unittest
import httplib
import json

from read_series import read_series


headers = {'Content-type':'application/json'}
series = read_series('./test_data/45_series.csv')

def connect():
    #return httplib.HTTPConnection('localhost:5000')
    return httplib.HTTPConnection('backend-ag.mybluemix.net')

class TestBackend(unittest.TestCase):
    def test_centroide_simple(self):
        data = {'pop_size':20,
                'ngen':10,
                'cxpb':0.2,
                'mutpb':0.1,
                'batch_evaluate':False,
                'series':series
        }

        data = json.dumps(data)
        con = connect()
        con.request('POST', '/centroide/simple', data, headers)
        response = con.getresponse()
        resp = json.load(response)

        print resp

        self.assertTrue(response.status == 200)



    def test_centroide_coop(self):
        data = {'pop_size':20,
                'ngen':20,
                'nespecies':3,
                'ngen_intercambio':5,
                'cxpb':0.2,
                'mutpb':0.1,
                'batch_evaluate':False,
                'series':series
        }

        data = json.dumps(data)
        con = connect()
        con.request('POST', '/centroide/coop', data, headers)
        response = con.getresponse()
        resp = json.load(response)

        print resp

        self.assertTrue(response.status == 200)



    def test_kmeans_simple(self):
        params_ag = {'pop_size':10,
                'ngen':10,
                'cxpb':0.2,
                'mutpb':0.1,
                'batch_evaluate':False
        }

        data = {'k':4,
                'n_init':2,
                'max_it':4,
                'params_ag' : params_ag,
                'series':series
        }

        data = json.dumps(data)
        con = connect()
        con.request('POST', '/kmeans/simple', data, headers)
        response = con.getresponse()
        resp = json.load(response)

        print resp

        self.assertTrue(response.status == 200)



    def test_kmeans_coop(self):
        params_ag = {'pop_size':10,
                'nespecies':3,
                'ngen_intercambio':3,
                'ngen':10,
                'cxpb':0.2,
                'mutpb':0.1,
                'batch_evaluate':False
        }

        data = {'k':4,
                'n_init':2,
                'max_it':4,
                'params_ag' : params_ag,
                'series':series
        }

        data = json.dumps(data)
        con = connect()
        con.request('POST', '/kmeans/coop', data, headers)
        response = con.getresponse()
        resp = json.load(response)

        print resp

        self.assertTrue(response.status == 200)



    @staticmethod
    def get_data_nmean(coop):
        params_ag = {'pop_size':10,
                'ngen':10,
                'cxpb':0.2,
                'mutpb':0.1,
                'batch_evaluate':False
        }

        if coop:
            params_ag['nespecies'] = 3
            params_ag['ngen_intercambio'] = 3

        endpoint = '/centroide/simple' if not coop else '/centroide/coop'

        n = len(series)
        cl1 = n/3
        cl2 = 2*n/3
        s1 = series[:cl1]
        s2 = series[cl1:cl2]
        s3 = series[cl2:]

        params_ag['series'] = s1
        data = json.dumps(params_ag)
        con = connect()
        con.request('POST', endpoint, data, headers)
        response = con.getresponse()
        c1 = json.load(response)['centroide']

        params_ag['series'] = s2
        data = json.dumps(params_ag)
        con = connect()
        con.request('POST', endpoint, data, headers)
        response = con.getresponse()
        c2 = json.load(response)['centroide']

        params_ag['series'] = s3
        data = json.dumps(params_ag)
        con = connect()
        con.request('POST', endpoint, data, headers)
        response = con.getresponse()
        c3 = json.load(response)['centroide']

        del params_ag['series']

        data = {'k':4,
                'n_init':2,
                'max_it':4,
                'params_ag' : params_ag,
                'series':series,
                'centroides':[c1,c2,c3]
        }

        return data



    def test_nmeans_simple_crisp(self):
        data = TestBackend.get_data_nmean(False)
        data = json.dumps(data)
        con = connect()
        con.request('POST', '/nmean/simple/crisp', data, headers)
        response = con.getresponse()
        resp = json.load(response)

        print resp

        self.assertTrue(response.status == 200)



    def test_nmeans_simple_fuzzy(self):
        data = TestBackend.get_data_nmean(False)
        data = json.dumps(data)
        con = connect()
        con.request('POST', '/nmean/simple/fuzzy', data, headers)
        response = con.getresponse()
        resp = json.load(response)

        print resp

        self.assertTrue(response.status == 200)



    def test_nmeans_coop_crisp(self):
        data = TestBackend.get_data_nmean(True)
        data = json.dumps(data)
        con = connect()
        con.request('POST', '/nmean/coop/crisp', data, headers)
        response = con.getresponse()
        resp = json.load(response)

        print resp

        self.assertTrue(response.status == 200)



    def test_nmeans_coop_fuzzy(self):
        data = TestBackend.get_data_nmean(True)
        data = json.dumps(data)
        con = connect()
        con.request('POST', '/nmean/coop/fuzzy', data, headers)
        response = con.getresponse()
        resp = json.load(response)

        print resp

        self.assertTrue(response.status == 200)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBackend)
    unittest.TextTestRunner(verbosity=2).run(suite)
