from abc import ABC, abstractmethod
from typing import Any
from research_framework.base.flyweight.base_flyweight import BaseFlyweight
from research_framework.flyweight.model.item_model import ItemModel
from research_framework.pipeline.model.pipeline_model import FilterModel, SimpleInputFilterModel

class BaseFlyManager(ABC):
    fly: BaseFlyweight = None 
    
    @classmethod
    @abstractmethod
    def next_filter_item(cls, filter_model:FilterModel, _, train_item:ItemModel):...
    @classmethod
    @abstractmethod
    def next_data_item(cls, filter_model:FilterModel, input_filter_model:SimpleInputFilterModel, data_item:ItemModel):...
    @abstractmethod
    def fit(self, filter_item:ItemModel, data:Any): ...
    @abstractmethod
    def predict(self, filter_item:ItemModel,  data:Any): ...