from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.container.container import Container
from research_framework.flyweight.flyweight_manager import OutputFlyManager
from research_framework.plugins.wrappers import MetricWrapper


FIT_TEST_STRING = "MEMORY MANAGEMENT FIT TEST"
PREDICT_TEST_STRING = "MEMORY MANAGEMENT PREDICT TEST"

@Container.bind(OutputFlyManager, MetricWrapper)
class MeMMetricTester(BasePlugin):
    def fit(self, *args, **kwargs): ...
    def predict(self, _, predicted):
        print("FUCKING SILHOUETTE!!!")
        X = Container.MEM[-1]["X"]
        X2 = Container.MEM[-1]["X2"]
        
        assert X == FIT_TEST_STRING
        assert X2 == PREDICT_TEST_STRING
        
        return X, X2