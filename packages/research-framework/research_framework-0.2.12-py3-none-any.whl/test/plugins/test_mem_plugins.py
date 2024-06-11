from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.container.container import Container
from research_framework.flyweight.flyweight_manager import DummyFlyManager
from research_framework.plugins.wrappers import StandardDatasetInOutWrapper
from test.metrics.test_metrics import FIT_TEST_STRING, PREDICT_TEST_STRING


@Container.bind(DummyFlyManager, StandardDatasetInOutWrapper)
class MeMFilterTester(BasePlugin):
    def fit(self, x, y):
        Container.MEM[-1]["X"] = FIT_TEST_STRING
        return x
    
    def predict(self, x):
        Container.MEM[-1]["X2"] = PREDICT_TEST_STRING
        return x