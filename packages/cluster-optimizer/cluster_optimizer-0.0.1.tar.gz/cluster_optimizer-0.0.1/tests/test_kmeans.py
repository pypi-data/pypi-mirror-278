import unittest

from cluster_optimizer import ClusterOptimizer

import pandas as pd

from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.cluster import KMeans,HDBSCAN

from sklearn.preprocessing import PowerTransformer,OneHotEncoder

from sklearn.datasets import load_iris
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


class TestKMeans(unittest.TestCase):

    def test_kmeans(self):

        # load data
        data = load_iris()
        df_iris = pd.DataFrame(data['data'],columns=data['feature_names'])
        df_iris['target'] = data['target'] 

        target_map   = dict([x for x in enumerate(data['target_names'])])
        target_map_r = dict([(x[1],x[0]) for x in enumerate(data['target_names'])]) 

        # pipeline for preprocessing
        feature_names = data['feature_names']


        numeric_features = ['sepal length (cm)','sepal width (cm)','petal length (cm)','petal width (cm)'] # feature_names
        numeric_transformer = Pipeline(
            steps=[
                ('encoder', PowerTransformer(standardize=True)),
                ]
            )

        categorical_features = []
        categorical_transformer = Pipeline(
            steps=[
                ('encoder', OneHotEncoder(handle_unknown='ignore')),
                ]
            )

        # combine transformers into pipeline
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features),
                ]
            )

        # transform data
        iris_trans = preprocessor.fit_transform(df_iris[feature_names])   

        # setup different cluster setting
        cluster_settings = {
            'kmeans': {
                'clusterer': KMeans(),
                'params':{
                    'n_clusters':                      [2,3,4,5,6,7,8,9,10],
                    'init':                            ['k-means++', 'random'],
                    }
                },
            'hDBScan': {
                'clusterer': HDBSCAN(),
                'params':{
                    'min_cluster_size':          [5,10,15,20,30],
                    'min_samples':               [5,10,15,20,30],
                    'eps':                       [0.1,0.25,0.5,],
                    }
                },
            }

        # cluster all parameters
        cluster_method = 'kmeans'
        # set up ClusterOptimizer
        co = ClusterOptimizer(
            cluster_settings[cluster_method]['clusterer'],
            cluster_settings[cluster_method]['params'],
            scoring=[silhouette_score, davies_bouldin_score, calinski_harabasz_score]
            )
        # run
        co.optimize(iris_trans)
        self.assertTrue(not co.results.empty)
        # print top results
        print(co.results.sort_values('silhouette_score',ascending=False).head())


    
        
if __name__ == '__main__':
    unittest.main()
