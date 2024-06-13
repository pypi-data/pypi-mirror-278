from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.container.container import Container
from research_framework.flyweight.flyweight_manager import OutputFlyManager
from research_framework.plugins.wrappers import MetricWrapper

from sklearn.metrics import davies_bouldin_score, silhouette_score, calinski_harabasz_score, \
    adjusted_rand_score, rand_score, normalized_mutual_info_score, homogeneity_score, completeness_score, \
    v_measure_score, homogeneity_completeness_v_measure, precision_score, recall_score, f1_score
    
@Container.bind(OutputFlyManager, MetricWrapper)
class Silhouette(BasePlugin):
    def fit(self, *args, **kwargs): ...
    def predict(self, _, predicted):
        print("FUCKING SILHOUETTE!!!")
        print(Container.MEM)
        X = Container.MEM[-1]["X_test"]
        print(predicted)
        return silhouette_score(X, predicted)

@Container.bind(OutputFlyManager, MetricWrapper)
class NMI(BasePlugin):

    def fit(self, x, y=None):...
    def predict(self, y, predicted ):
        return normalized_mutual_info_score(y, predicted)
    
@Container.bind(OutputFlyManager, MetricWrapper)
class ARI(BasePlugin):

    def fit(self, x, y=None):...
    def predict(self, y, predicted ):
        return adjusted_rand_score(y, predicted)
    
@Container.bind(OutputFlyManager, MetricWrapper)
class RI(BasePlugin):

    def fit(self, x, y=None):...
    def predict(self, y, predicted ):
        return rand_score(y, predicted)
    
@Container.bind(OutputFlyManager, MetricWrapper)
class Homogeneity(BasePlugin):

    def fit(self, x, y=None):...
    def predict(self, y, predicted ):
        return homogeneity_score(y, predicted)

@Container.bind(OutputFlyManager, MetricWrapper)
class Completeness(BasePlugin):

    def fit(self, x, y=None):...
    def predict(self, y, predicted ):
        return completeness_score(y, predicted)

@Container.bind(OutputFlyManager, MetricWrapper)
class VMeasure(BasePlugin):

    def fit(self, x, y=None):...
    def predict(self, y, predicted ):
        return  v_measure_score(y, predicted)
    
@Container.bind(OutputFlyManager, MetricWrapper)
class HoCoV(BasePlugin):

    def fit(self, x, y=None):...
    def predict(self, y, predicted ):
        return  homogeneity_completeness_v_measure(y, predicted)
    
@Container.bind(OutputFlyManager, MetricWrapper)
class F1(BasePlugin):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def fit(self, *args, **kwargs): ...
    def predict(self, y, predicted):
        return f1_score(y, predicted, zero_division=0.0, **self.kwargs)

@Container.bind(OutputFlyManager, MetricWrapper)
class Precision(BasePlugin):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def fit(self, *args, **kwargs): ...
    def predict(self, y, predicted):
        return precision_score(y, predicted, zero_division=0.0, **self.kwargs)

@Container.bind(OutputFlyManager, MetricWrapper)
class Recall(BasePlugin):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def fit(self, *args, **kwargs): ...
    def predict(self, y, predicted):
        return recall_score(y, predicted, zero_division=0.0, **self.kwargs)