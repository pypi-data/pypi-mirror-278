from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager
from research_framework.base.pipeline.base_pipeline import BasePipeline
from research_framework.container.container import Container
from research_framework.container.model.global_config import GlobalConfig
from research_framework.flyweight.flyweight import FlyWeight, SimpleFlyWeight
from pydantic import BaseModel
from research_framework.pipeline.model.pipeline_model import PipelineModel
from research_framework.base.storage.base_storage import BaseStorage
from research_framework.storage.local_storage import LocalStorage


class PipelineManager:
    
    @staticmethod
    def init_fly(fly):
        if Container.fly is None:
            Container.fly = fly()
        if BaseFlyManager.fly is None:
            BaseFlyManager.fly = Container.fly
    
    @staticmethod
    def start_pipeline(project:str, pl_conf:BaseModel, log:bool=False, store:bool=True, overwrite:bool=False, storage:BaseStorage=LocalStorage('data/cache')):
        PipelineManager.init_fly(SimpleFlyWeight)
        
        Container.storage = storage
        Container.global_config = GlobalConfig(
            log=log,
            overwrite=overwrite,
            store=store
        )
        
        pipeline:BasePipeline = Container.PIPELINES[pl_conf._clazz](pl_conf, project)
        pipeline.init()
        pipeline.start()
        pipeline.log_metrics()
        pipeline.finish()
        return pipeline
    
    @staticmethod
    def fill_pipline_items(config:PipelineModel):
        PipelineManager.init_fly(SimpleFlyWeight)
        print("___________________ FILLING PIPELINE WITH ITEMS ____________________\n")
        print("* Train input")
        train_item = Container.BINDINGS[config.train_input.clazz].manager.next_data_item(config.train_input, config.train_input, None)
        config.train_input.item = train_item
        
        if config.test_input is not None:
            print("* Test input")
            test_item = Container.BINDINGS[config.test_input.clazz].manager.next_data_item(config.test_input, config.test_input, None)
            config.test_input.item = test_item
        
        print("* Filters: ")
        for f_model in config.filters:
            print(f"\t - {f_model.clazz}")
            f_manager:BaseFlyManager = Container.BINDINGS[f_model.clazz].manager
            f_manager.next_filter_item(f_model, config.train_input, train_item)

            train_item = f_manager.next_data_item(f_model, config.train_input, train_item)
            if config.test_input is not None:
                test_item = f_manager.next_data_item(f_model, config.test_input, test_item)
            
        return config