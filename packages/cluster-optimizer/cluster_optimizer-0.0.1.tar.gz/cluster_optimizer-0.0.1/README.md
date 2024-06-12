# Cluster Optimizer

This is a simple object simulating the [GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html) object from [scikit-learn (sklearn)](https://scikit-learn.org), but only for clustering. Instead of estimating predictive performance measures using a test fold, it simply calculates unsupervised scores such as the [silhouette_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html#sklearn.metrics.silhouette_score) or [davies_bouldin_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.davies_bouldin_score.html#sklearn.metrics.davies_bouldin_score). 

The object is instantiated with an sklearn cluster algorithm, e.g. [KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans), [HDBScan](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html#sklearn.cluster.HDBSCAN), or similar from from [sklearn.cluster](https://scikit-learn.org/stable/api/sklearn.cluster.html) and a set of parameter options. Different scoring approaches can be supplied as a list of the scoring functions (silhouette_score, davies_bouldin_score, calinski_harabasz_score  from [sklearn.metrics](https://scikit-learn.org/stable/api/sklearn.metrics.html) ). 

Using the ClusterOptimizer.optimize() method will perform a grid search through the supplied parameter space. The scores for all supplied scoring functions are stored for all parameters. 

The results can be obtained by ClusterOptimizer.results, which should return a [pandas](https://pandas.pydata.org/pandas-docs/stable/index.html) [DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html#dataframe). 

For one or two parameters, the result DataFrame can be used together with [seaborn](https://seaborn.pydata.org) for visualisation. 





