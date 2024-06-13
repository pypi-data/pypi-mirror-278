from typing import Any
from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.base.utils.method_overload import methdispatch
import pandas as pd
from research_framework.dataset.standard_dataset import StandardDataset

class DummyWrapper(BaseWrapper):
    def fit(self, *args, **kwargs):
        return self.plugin.fit(*args, **kwargs)
    
    def predict(self, *args, **kwargs):
        return self.plugin.predict(*args, **kwargs)


class PullWrapper(BaseWrapper):
    @methdispatch
    def fit(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
    
    @methdispatch
    def predict(self, x):
        raise TypeError(f"Wrong input type {type(x)}")

    @fit.register
    def _(self, x:pd.DataFrame) -> BasePlugin:
        return self.plugin.fit(x)
    
    @predict.register
    def _(self, x:pd.DataFrame) -> pd.DataFrame:
        return self.plugin.predict(x)
    
    @fit.register
    def _fit(self, x:StandardDataset):
        return self.plugin.fit(x)
    
    @predict.register
    def _predict(self, x:StandardDataset):
        return self.plugin.predict(x)
    
    @fit.register
    def _(self, x:type(lambda:0)):
        x = x()
        return self.fit(x)
    
    @predict.register
    def _(self, x:type(lambda:0)):
        x = x()
        return self.predict(x)
    
# Este es para los plugins que transforman texto
class DataFrameInOutWrapper(BaseWrapper):
    @methdispatch
    def fit(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
    
    @methdispatch
    def predict(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
    
    @fit.register
    def _(self, x:pd.DataFrame) -> BasePlugin:
        return self.plugin.fit(x, None)
    
    @fit.register
    def _(self, x:type(lambda:0)):
        x = x()
        return self.fit(x)
    
    @predict.register
    def _(self, x:pd.DataFrame) -> pd.DataFrame:
        out = self.plugin.predict(x)
        if type(out) != pd.DataFrame:
            raise TypeError("Wrong return type: Plugin should retreive type pd.DataFrame")
        
        return out

    @predict.register
    def _(self, x:type(lambda:0)):
        x = x()
        return self.predict(x)
    
    
# Este es para los plugins que transforman texto en vectores
# y para los clasificadores que trabajan directamente con textos
class DataFrameInStandardDatasetOutWrapper(BaseWrapper):
    @methdispatch
    def fit(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
    
    @methdispatch
    def predict(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
    
    @fit.register
    def _fit(self, x:pd.DataFrame) -> BasePlugin:
        if 'label' in x:
            label = x.label.to_list()
        else:
            label = None
        return self.plugin.fit(x, label)
    
    @fit.register
    def _(self, x:type(lambda:0)):
        x = x()
        return self.fit(x)
    
    @predict.register
    def _pred(self, x:pd.DataFrame) -> StandardDataset:
        return StandardDataset(x, self.plugin.predict(x))
    
    @predict.register
    def _(self, x:type(lambda:0)):
        x = x()
        return self.predict(x)
    
    
# Este es para los plugins que Transforman vectores en vectores
# y para los clasificadores que trabajan con textos
class StandardDatasetInOutWrapper(BaseWrapper):
    @methdispatch
    def fit(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
    
    @methdispatch
    def predict(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
    
    @fit.register
    def _fit(self, x:StandardDataset) -> BasePlugin:
        if 'label' in x.df:
            label = x.df.label.to_list()
        else:
            label = None
        return self.plugin.fit(x.vectors, label)
    
    @fit.register
    def _(self, x:type(lambda:0)):
        x = x()
        return self.fit(x)
        
    @predict.register
    def _pred(self, x:StandardDataset) -> StandardDataset:
        return StandardDataset(x.df, self.plugin.predict(x.vectors))
    
    @predict.register
    def _(self, x:type(lambda:0)):
        x = x()
        return self.predict(x)
    
    
# Este es para las métricas que a veces les llegan pd.DataFrame
# y otras StandardDataset
class MetricWrapper(BaseWrapper):
    def fit(self, *args, **kwargs):
        return self.plugin.fit(*args, **kwargs)
        
    @methdispatch
    def predict(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
    
        
    @predict.register
    def _pred(self, x:StandardDataset) -> Any:
        return self.plugin.predict(x.df.label.to_list(), x.vectors)
    
    @predict.register
    def _(self, x:type(lambda:0)):
        x = x()
        return self.predict(x)
    
    
class EarlyMetricWrapper(BaseWrapper):
    def fit(self, *args, **kwargs):
        return self.plugin.fit(*args, **kwargs)
        
    @methdispatch
    def predict(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
        
    @predict.register
    def _pred(self, x:StandardDataset) -> Any:
        return self.plugin.predict(x.df.label.to_list(), x.df['count'].to_list(), x.vectors)
    
    @predict.register
    def _(self, x:type(lambda:0)):
        x = x()
        return self.predict(x)
    

class CoherenceMetricWrapper(BaseWrapper):
    def fit(self, *args, **kwargs):
        return self.plugin.fit(*args, **kwargs)
        
    @methdispatch
    def predict(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
    
        
    @predict.register
    def _pred(self, x:StandardDataset) -> Any:
        return self.plugin.predict(x.df, x.vectors)
    
    @predict.register
    def _(self, x:type(lambda:0)):
        x = x()
        return self.predict(x)