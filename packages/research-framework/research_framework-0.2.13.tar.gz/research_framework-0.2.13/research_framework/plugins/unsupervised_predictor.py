from sklearn.cluster import AgglomerativeClustering, KMeans, AffinityPropagation, Birch, OPTICS, SpectralClustering, SpectralClustering
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import kneighbors_graph
from sklearn.base import clone

from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.container.container import Container
from research_framework.flyweight.flyweight_manager import FitPredictFlyManager
from research_framework.plugins.wrappers import StandardDatasetInOutWrapper

class SkCluster(BasePlugin):
    def __init__(self, clust_clas, refit=False,  **params):
        super().__init__()
        self.model = clust_clas(**params)
        self.trained = False
        self.refit = refit
        
    def fit(self, x, *_):
        self.model = self.model.fit(x)
        Container.MEM[-1]["X_train"] = x
        self.trained = True
        
        
    def predict(self, x, *_):
        if self.refit:
            self.model = self.model.fit(x)
            Container.MEM[-1]["X_train"] = x
            self.trained = True
            
        if self.trained:
            Container.MEM[-1]["X_test"] = x
            return self.model.predict(x).tolist()
        else:
            raise Exception("Model not trained yet!") 
        
    def get_clusters(self):
        if self.trained:
            return self.model.predict(self.x).tolist()
        else:
            raise Exception("Model not trained yet!")
        
    def get__dict__(self):
        return self.model.__dict__


class SkMixture(BasePlugin):
    def __init__(self, mix_clas, refit=False, **params):
        self.model = mix_clas(**params)
        self.refit = refit
        self.trained = False
        self.x = None
        
    def fit(self, x, *_):
        self.x = x
        self.model = self.model.fit(x)
        self.trained = True
        
    def predict(self, x, *_):
        if self.refit:
            self.model = self.model.fit(x)
            self.trained = True
            
        if self.trained:
            return self.model.predict(x).tolist()
        else:
            raise Exception("Model not trained yet!")

    def get_clusters(self):
        if self.trained:
            return self.model.predict(self.x).tolist()
        else:
            raise Exception("Model not trained yet!")
        
    def get__dict__(self):
        return self.model.__dict__

    def clone(self):
        self.trained = False
        self.model = clone(self.model, safe=True)
        return self
    

""" Clases hijo """    
@Container.bind(FitPredictFlyManager, StandardDatasetInOutWrapper)
class Agglomerative(SkCluster):
    config = {
        "name": "Agglomerative",
        "img": "AgglomerativeClustering",
        "params": {
            "n_clusters": 3,
            "compute_full_tree": False,
            "distance_threshold": 0.5,
            "metric":[
                "euclidean", "cityblock", "cosine", "l1", "l2", "manhattan", "braycurtis", "canberra", "chebyshev",
                "correlation", "dice", "hamming", "jaccard", "kulsinski", "mahalanobis", "rogerstanimoto", "russellrao",
                "seuclidean", "sokalmichener", "sokalsneath", "sqeuclidean", "yule"
            ],
            "linkage": ["average", "complete", "simple"],
        }
    }
    
    def __init__(self, params):
        super().__init__(AgglomerativeClustering, params)
        self.params = params
        
    def predict(self, x, *_):
        if self.trained:
            return self.model.labels_
        else:
            raise Exception("Model not trained yet!")
        
    
    def fit(self, x, *_):
        A = kneighbors_graph(x, 20, mode='connectivity', include_self=True, metric='cosine', n_jobs=-1)
        if "n_clusters" in self.params and "distance_threshold" in self.params:
            del self.params["distance_threshold"]
        self.model = AgglomerativeClustering(connectivity=A, **self.params)
        self.model.fit(x)
        self.trained = True
        
@Container.bind(FitPredictFlyManager, StandardDatasetInOutWrapper)
class Gmm(SkMixture):
    config = {
        "name": "Gmm",
        "img": "GaussianMixture",
        "params": {
            "n_components": 3,
            "tol": 0.001,
            "max_iter": 100,
            "n_init": 1,
            "init_params": ["kmeans", "k-means++", "random", "random_from_data"],
            "covariance_type": ["full", "tied", "diag", "spherical"]
        }
    }
    def __init__(self, **kwargs):
        super().__init__(GaussianMixture, **kwargs)

@Container.bind(FitPredictFlyManager, StandardDatasetInOutWrapper)
class Kmeans(SkCluster):
    config = {
        "name": "k-menas",
        "img": "MiniBatchKMeans",
        "params": {
            "n_clusters": 8,
            "init":["k-means++", "random"],
            "algorithm": ["lloyd","elkan", "auto", "full"]
        }
    }
    
    def __init__(self, **params):
        super().__init__(KMeans, **params)

@Container.bind(FitPredictFlyManager, StandardDatasetInOutWrapper)
class AffinityProp(SkCluster):
    config = {
        "name": "AffinityProp",
        "img": "AffinityPropagation",
        "params": {
            "damping": 0.5,
            "random_state": 0
        }
    }
    def __init__(self, **params):
        super().__init__(AffinityPropagation, **params)

@Container.bind(FitPredictFlyManager, StandardDatasetInOutWrapper)
class MaBirch(SkCluster):
    config = {
        "name": "Birch",
        "img": "BIRCH",
        "params": {
            "n_clusters": 3,
        }
    }
    def __init__(self, **params):
        super().__init__(Birch, **params)
        
@Container.bind(FitPredictFlyManager, StandardDatasetInOutWrapper)
class MoPTICS(SkCluster):
    config = {
        "name": "OPTICS",
        "img": "OPTICS",
        "params": {
            "min_samples": 5,
            "xi": 0.1,
            "min_cluster_size": 0.1
        }
    }
    def __init__(self, **params):
        # params["max_eps"] = 100.0
        super().__init__(OPTICS, **params)
        
    def fit(self, x, *_):
        self.trained = True
        
        
    def predict(self, x, *_):
        if self.trained:
            return self.model.fit_predict(x).tolist()
        else:
            raise Exception("Model not trained yet!") 
        
@Container.bind(FitPredictFlyManager, StandardDatasetInOutWrapper)
class Spectral(SkCluster):
    config = {
        "name": "Spectral",
        "img": "SpectralClustering",
        "params": {
            "n_clusters": 8,
            "eigen_solver": ["arpack", "lobpcg", "amg"],
            "affinity": ["nearest_neighbors", "rbf", "precomputed", "precomputed_nearest_neighbors"]
        }
    }
    def __init__(self, **params):
        super().__init__(SpectralClustering, **params)