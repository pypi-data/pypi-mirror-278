from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.flyweight.model.item_model import ItemModel
from research_framework.pipeline.model.pipeline_model import FilterModel, SimpleInputFilterModel

from typing import Any, Optional
from rich import print
from fastapi.encoders import jsonable_encoder


class FitPredictFlyManager(BaseFlyManager):
    
    @classmethod
    def next_filter_item(cls, filter_model:FilterModel, _, train_item:ItemModel):
        filter_item:ItemModel = cls.fly.item_from_name_and_prev(f'{filter_model.clazz}{jsonable_encoder(filter_model.params)}[Trained]({train_item.hash_code})', train_item)
        filter_model.item = filter_item
    
    @classmethod
    def next_data_item(cls, filter_model:FilterModel, input_filter_model:SimpleInputFilterModel, data_item:ItemModel):
        if not filter_model.item.hash_code in input_filter_model:
            new_train_item = cls.fly.item_from_name_and_prev(f'{data_item.name} -> {filter_model.item.name}', data_item)
            input_filter_model.items[filter_model.item.hash_code] = new_train_item
        else:
            new_train_item = input_filter_model.items[filter_model.item.hash_code] 
        return new_train_item
    
    def __init__(self, wrapper: BaseWrapper, store:bool, overwrite:bool):
        self.wrapper: BaseWrapper = wrapper
        self.filter_item:ItemModel = None
        self.store:bool = store
        self.overwrite:bool = overwrite
        
    def fit(self, filter_item:ItemModel, data:Any):
        print("---------------------[Filter Training]----------------------------")
        print(f"Trained_filter_name -> {filter_item.name}")
        print(f'Trained_filter_hashcode -> {filter_item.hash_code}')
        filter_trained_item = BaseFlyManager.fly.get_item(filter_item.hash_code)
        print(filter_trained_item)
        print("-------------------------------------------------")
        if filter_trained_item is None or self.overwrite:
            self.wrapper.fit(data)
            
            if self.store:
                if filter_trained_item is None:
                    if not BaseFlyManager.fly.set_item(filter_item, self.wrapper.plugin):
                        raise Exception("Couldn't save item")
                else:
                    if not BaseFlyManager.fly.set_item(filter_item, self.wrapper.plugin, self.overwrite):
                        raise Exception("Couldn't save item")
        else:
            self.wrapper = lambda : BaseFlyManager.fly.wrap_plugin_from_cloud(filter_trained_item.params)
            print(f"* Wrapping data -> {filter_item.hash_code}")
        
        filter_item.stored = True
        self.filter_item = filter_item
                
    def predict(self, data_item:ItemModel, data:Any):
        if self.filter_item is None:
            raise Exception("Model not trained, call fit() before calling predict()!")
        else:
            print("-------------------------------------------------")
            print(f"Data_name -> {data_item.name}")
            print(f'Hash_code -> {data_item.hash_code}')
            print(data_item)
            print("-------------------------------------------------")
            stored_item = BaseFlyManager.fly.get_item(data_item.hash_code)
            if stored_item is None or self.overwrite:
                
                if callable(self.wrapper) and self.wrapper.__name__ == "<lambda>":
                    self.wrapper = self.wrapper()
                
                data = self.wrapper.predict(data)
                
                if self.store:
                    if stored_item is None:
                        if not BaseFlyManager.fly.set_item(data_item, data):
                            raise Exception("Couldn't save item")
                    else:
                        if not BaseFlyManager.fly.set_item(data_item, data, self.overwrite):
                            raise Exception("Couldn't save item")
                
            else:
                print(f"* lambda data -> {data_item.hash_code}")
                data = lambda : BaseFlyManager.fly.get_data_from_item(data_item)
                data_item.stored = True
            
            return data

      
class PassThroughFlyManager(BaseFlyManager):
    
    @classmethod
    def next_filter_item(cls, filter_model:FilterModel, *_):
        filter_item:ItemModel = cls.fly.item_from_name(f'{filter_model.clazz}{jsonable_encoder(filter_model.params)}[-]')
        filter_model.item = filter_item
        
    @classmethod
    def next_data_item(cls, filter_model:FilterModel, input_filter_model:SimpleInputFilterModel, data_item:ItemModel):
        if not filter_model.item.hash_code in input_filter_model:
            new_train_item = cls.fly.item_from_name_and_prev(f'{data_item.name} -> {filter_model.item.name}', data_item)
            input_filter_model.items[filter_model.item.hash_code] = new_train_item
        else:
            new_train_item = input_filter_model.items[filter_model.item.hash_code] 
        return new_train_item
    
    def __init__(self,  wrapper: BaseWrapper, store:bool, overwrite:bool, *args, **kwargs):
        self.wrapper: BaseWrapper = wrapper
        self.hashcode:Optional[str] = None
        self.store:bool = store
        self.overwrite:bool = overwrite
        
    def fit(self, *args, **kwargs): ...
        
    def predict(self, data_item:ItemModel, data):
        print("-------------------------------------------------")
        print(f"Data_name -> {data_item.name}")
        print(f'Hash_code -> {data_item.hash_code}')
        stored_item = BaseFlyManager.fly.get_item(data_item.hash_code)
        print(stored_item)
        print("-------------------------------------------------")
        if stored_item is None or self.overwrite:            
            data = self.wrapper.predict(data)
            
            if self.store:
                if stored_item is None:
                    if not BaseFlyManager.fly.set_item(data_item, data):
                        raise Exception("Couldn't save item")
                else:
                    if not BaseFlyManager.fly.set_item(data_item, data, self.overwrite):
                        raise Exception("Couldn't save item")
                    
        else:
            print(f"* lambda data -> {data_item.hash_code}")
            data = lambda : BaseFlyManager.fly.get_data_from_item(data_item)
            data_item.stored = True
        
        return data
    
class InputFlyManager(BaseFlyManager):
    @classmethod
    def next_filter_item(cls, *_):
        raise NotImplemented("Not apply!")
        
    @classmethod
    def next_data_item(cls, filter_model:FilterModel, input_filter_model:SimpleInputFilterModel, _):
        new_train_item:ItemModel = cls.fly.item_from_name(filter_model.name)
        input_filter_model.item = new_train_item
        #input_filter_model.items.append(new_train_item)
        return new_train_item
    
    
    def __init__(self, wrapper: BaseWrapper, store:bool, overwrite:bool, *args, **kwargs):
        self.wrapper: BaseWrapper = wrapper
        self.store:bool = store
        self.overwrite:bool = overwrite
        
    def fit(self, *args, **kwargs): ...
    
    def predict(self, data_item:ItemModel, *args, **kwargs):
        print("-------------------------------------------------")
        print(f"Data_name -> {data_item.name}")
        print(f'Hash_code -> {data_item.hash_code}')
        stored_item = BaseFlyManager.fly.get_item(data_item.hash_code)
        print(stored_item)
        print("-------------------------------------------------")
        if stored_item is None or self.overwrite:
            data = self.wrapper.predict(None)
            
            if self.store:
                if stored_item is None:
                    if not BaseFlyManager.fly.set_item(data_item, data):
                        raise Exception("Couldn't save item")
                else:
                    if not BaseFlyManager.fly.set_item(data_item, data, self.overwrite):
                        raise Exception("Couldn't save item")
        else:
            data = lambda : BaseFlyManager.fly.get_data_from_item(data_item)
            data_item.stored = True
        
        return data
    
class WandbSeepsFlyManager(BaseFlyManager):
    @classmethod
    def next_filter_item(cls, filter_model:FilterModel, _, train_item:ItemModel):
        filter_item:ItemModel = cls.fly.item_from_name_and_prev(f'{filter_model.clazz}{jsonable_encoder(filter_model.params)}[Trained]({train_item.hash_code})', train_item)
        filter_model.item = filter_item
    
    @classmethod
    def next_data_item(cls, filter_model:FilterModel, input_filter_model:SimpleInputFilterModel, data_item:ItemModel):
        if not filter_model.item.hash_code in input_filter_model:
            new_train_item = cls.fly.item_from_name_and_prev(f'{data_item.name} -> {filter_model.item.name}', data_item)
            input_filter_model.items[filter_model.item.hash_code] = new_train_item
        else:
            new_train_item = input_filter_model.items[filter_model.item.hash_code]
        return new_train_item
    
    def __init__(self, wrapper: BaseWrapper, store:bool, overwrite:bool, *args, **kwargs):
        self.wrapper: BaseWrapper = wrapper
        
        self.filter_item:ItemModel = None
        self.store = store
        self.overwrite = overwrite
        
    def fit(self, filter_item:ItemModel, data):
        print("---------------------[Prev data stored?]--------------------------")
        if not filter_item.prev_model.stored:
            if not BaseFlyManager.fly.set_item(filter_item.prev_model, data):
                raise Exception("Couldn't save item")
            
        print("---------------------[Filter Training]----------------------------")
        print(f"Trained_filter_name -> {filter_item.name}")
        print(f'Trained_filter_hashcode -> {filter_item.hash_code}')
        filter_trained_item = BaseFlyManager.fly.get_item(filter_item.hash_code)
        print(filter_trained_item)
        
        if filter_trained_item is None or self.overwrite:
            self.wrapper.fit(filter_item.prev_model, overwrite=True)
            
            if not BaseFlyManager.fly.set_item(filter_item, self.wrapper.plugin):
                raise Exception("Couldn't save item")
            
            self.filter_item = filter_item
        else:
            self.wrapper = BaseFlyManager.fly.wrap_plugin_from_cloud(filter_trained_item.params)
            self.wrapper.fit(filter_item.prev_model, overwrite=False)
            self.filter_item = filter_trained_item
        
    def predict(self, data_item:ItemModel, data):
        if self.filter_item is None:
            raise Exception("Model not trained, call fit() before calling predict()!")
        else:
            print("-------------------------------------------------")
            print(f"Data_name -> {data_item.name}")
            print(f'Hash_code -> {data_item.hash_code}')
            print(data_item)
            print("-------------------------------------------------")
            stored_item = BaseFlyManager.fly.get_item(data_item.hash_code)
            if stored_item is None or self.overwrite:
                
                if callable(self.wrapper) and self.wrapper.__name__ == "<lambda>":
                    self.wrapper = self.wrapper()
                
                data = self.wrapper.predict(data)
                
                if self.store:
                    if stored_item is None:
                        if not BaseFlyManager.fly.set_item(data_item, data):
                            raise Exception("Couldn't save item")
                    else:
                        if not BaseFlyManager.fly.set_item(data_item, data, self.overwrite):
                            raise Exception("Couldn't save item")
                
            else:
                print(f"* lambda data -> {data_item.hash_code}")
                data = lambda : BaseFlyManager.fly.get_data_from_item(data_item)
                data_item.stored = True
            
            return data
        
#TODO testar si hay que implementar el class method next() en estas dos clases       
class DummyFlyManager(BaseFlyManager):
    @classmethod
    def next_filter_item(cls, filter_model:FilterModel, *_):
        filter_item:ItemModel = cls.fly.item_from_name(f'{filter_model.clazz}{jsonable_encoder(filter_model.params)}[Dummy]')
        filter_model.item = filter_item
        
    @classmethod
    def next_data_item(cls, filter_model:FilterModel, input_filter_model:SimpleInputFilterModel, data_item:ItemModel):
        if not filter_model.item.hash_code in input_filter_model:
            new_train_item = cls.fly.item_from_name_and_prev(f'{data_item.name} -> {filter_model.item.name}', data_item)
            input_filter_model.items[filter_model.item.hash_code] = new_train_item
        else:
            new_train_item = input_filter_model.items[filter_model.item.hash_code]
        return new_train_item
    
    def __init__(self, wrapper: BaseWrapper, *args, **kwargs):
        self.wrapper: BaseWrapper = wrapper

    def fit(self, data_item:ItemModel, data):
        self.wrapper.fit(data)
        
        print("-------------------------------------------------")
        print(f"data_hashcode -> {data_item.hash_code}")
        print(f'filter_name -> {data_item.name}')
        print("-------------------------------------------------")
    
    def predict(self, data_item:ItemModel, data):
        data = self.wrapper.predict(data)
        
        print("-------------------------------------------------")
        print(f"data_hashcode -> {data_item.hash_code}")
        print(f'filter_name -> {data_item.name}')
        print("-------------------------------------------------")
        
        return data
      
class OutputFlyManager(BaseFlyManager):
    def __init__(self, wrapper:BaseWrapper):
        self.wrapper: BaseWrapper = wrapper
        
    @classmethod
    def next_filter_item(cls, *_): ...
        
    @classmethod
    def next_data_item(cls, *_): ...
        
    def fit(self, *args, **kwargs): ...
    
    def predict(self, data):
        return self.wrapper.predict(data)

 