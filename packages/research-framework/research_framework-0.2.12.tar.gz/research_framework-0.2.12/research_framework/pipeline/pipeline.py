from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager
from research_framework.base.pipeline.base_pipeline import BasePipeline
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.container.container import Container
from research_framework.flyweight.mem_manager import FILTER_VARS
from research_framework.pipeline.exceptions.pipeline_exceptions import PipelineExecutionException
from research_framework.pipeline.model.pipeline_model import FilterModel, InputFilterModel, PipelineModel, WandbRunPipelineModel
from research_framework.base.utils.grid_seach import generate_combis
from research_framework.flyweight.flyweight import SimpleFlyWeight
from rich import print

from research_framework.pipeline.pipeline_manager import PipelineManager
from research_framework.storage.local_storage import LocalStorage

import wandb

@Container.register_pipeline
class WandbRunPipeline(BasePipeline):
    def __init__(self, doc:WandbRunPipelineModel):
        self.pipeline:WandbRunPipelineModel = doc
        self.pipeline_wrappers = []

    def init(self):
        Container.un_freeze_wandb_logger()
        
    def start(self):
        train_input = self.pipeline.train_input
        test_input = self.pipeline.test_input
        
        try:
            train_f = self.fit(train_input)
            
            if test_input is not None:
                test_f = self.predict(test_input)
            else:
                test_f = train_f
                
            for idx, metric in enumerate(self.pipeline.metrics):
                    m_wrapper = Container.get_metric(metric.clazz, metric.params)
                    metric.value = m_wrapper.predict(test_f)
                    self.pipeline.metrics[idx] = metric

        except Exception as ex:
            raise PipelineExecutionException(ex)

    def fit(self, train_input:InputFilterModel):
        train_w = Container.get_wrapper(train_input.clazz, train_input.params)
        train_f = train_w.predict(None)
        
        for _, filter_model in enumerate(self.pipeline.filters):
            wrapper:BaseWrapper = Container.get_wrapper(filter_model.clazz, filter_model.params)
            wrapper.fit(train_f)

            self.pipeline_wrappers.append(wrapper)
            
            train_f = wrapper.predict(train_f)
            
        return train_f
                
    def predict(self, test_input: InputFilterModel):
        test_w = Container.get_wrapper(test_input.clazz, test_input.params)
        test_f = test_w.predict(None)
        
        for wrapper in self.pipeline_wrappers:
            test_f = wrapper.predict(test_f)

        return test_f
        
    def log_metrics(self) -> None:
        print(self.pipeline.metrics)
        for metric in self.pipeline.metrics:
            Container.send_to_logger(message={metric.clazz: metric.value})

    def finish(self) -> None:
        if Container.logger is not None:
            Container.logger.finish()

@Container.register_pipeline
class SimpleFitPredictPipeline(BasePipeline):
    def __init__(self, doc:PipelineModel, project:str):
        Container.fly = SimpleFlyWeight()
        self.pipeline: PipelineModel = doc
        self.config = {'dataset': self.pipeline.train_input.name}
        
        for f in self.pipeline.filters:
            self.config[f.clazz] = f.params
            
        self.project_hash = Container.fly.hashcode_from_name("->".join(list(map(lambda x: f'({x.clazz}:{x.params})', self.pipeline.filters))))
        
        Container.global_config.dataset = self.pipeline.train_input.name
        Container.global_config.project_name = project
        Container.global_config.run_name = self.pipeline.train_input.name+"->("+self.project_hash+")"
        
        self.pipeline_filters = []
        
    
    def init(self):
        Container.init_wandb_logger(
            project=Container.global_config.project_name, 
            name=Container.global_config.run_name,
            config=self.config
        )
        Container.send_to_logger(message={"dataset": Container.global_config.dataset})
        
        
    def start(self):
        train_input = self.pipeline.train_input
        test_input = self.pipeline.test_input
        
        try:
            train_f = self.fit(train_input)
            
            if test_input is not None:
                test_f = self.predict(test_input)
            else:
                test_f = train_f
                
            for idx, metric in enumerate(self.pipeline.metrics):
                    m_wrapper = Container.get_metric(metric.clazz, metric.params)
                    metric.value = m_wrapper.predict(test_f)
                    self.pipeline.metrics[idx] = metric
        
        except Exception as ex:
            raise PipelineExecutionException(ex)
        
    def fit(self, train_input:InputFilterModel):
        train_m = Container.get_filter_manager(train_input.clazz, train_input.params)
        
        train_item = train_m.next_data_item(train_input, train_input, None)
        train_f = train_m.predict(data_item=train_item)
        
        for filter_model in self.pipeline.filters:
            filter_manager:BaseFlyManager = Container.get_filter_manager(
                filter_model.clazz, 
                filter_model.params | filter_model.alt_params, 
                filter_model.overwrite, 
                filter_model.store
            )
            
            filter_manager.next_filter_item(filter_model, train_input, train_item)
            
            Container.MEM[filter_model.item.hash_code] = FILTER_VARS(filter_model.item.hash_code, Container.storage, Container.MEM.overwrite)
            
            filter_manager.fit(filter_model.item, train_f)
            
            train_item = filter_manager.next_data_item(filter_model, train_input, train_item)
            
            train_f = filter_manager.predict(train_item, train_f)
            
            self.pipeline_filters.append(filter_manager)
            
        return train_f
                
    def predict(self, test_input: InputFilterModel):
        test_m = Container.get_filter_manager(test_input.clazz, test_input.params)
        
        test_item = test_m.next_data_item(test_input, test_input, None)
        test_f = test_m.predict(data_item=test_item)
        
        for filter_manager, filter_model in zip(self.pipeline_filters, self.pipeline.filters):
            test_item = filter_manager.next_data_item(filter_model, test_input, test_item)
            test_f = filter_manager.predict(test_item, test_f)
            
        return test_f
        
    def log_metrics(self) -> None:
        print(self.pipeline.metrics)
        for metric in self.pipeline.metrics:
            Container.send_to_logger(message={metric.clazz: metric.value})
            

    def finish(self) -> None:
        if not Container.logger is None:
            Container.logger.finish()
            
@Container.register_pipeline
class FitPredictPipeline(BasePipeline):
    def __init__(self, doc:PipelineModel, project:str):
        print("\n* Pipeline: ")
        self.pipeline:PipelineModel = PipelineManager.fill_pipline_items(doc) 
        print(self.pipeline)
        self.project = project
        self.config = {'dataset': self.pipeline.train_input.name}
        for f in self.pipeline.filters:
            self.config[f.clazz] = f.params
            
        self.project_hash = Container.fly.hashcode_from_name("->".join(list(map(lambda x: f'({x.clazz}:{x.params})', self.pipeline.filters))))
        
        self.pipeline_filters = []
        
        
    
    def init(self):
        Container.global_config.project_name = self.project
        Container.global_config.run_name = self.pipeline.train_input.name+"->("+self.project_hash+")"
        Container.init_wandb_logger(
            project=self.project, 
            name=self.pipeline.train_input.name+"->("+self.project_hash+")",
            config=self.config
        )
        Container.send_to_logger(message={"dataset": self.pipeline.train_input.name})
        
    def start(self) -> None:
        try:
            train_input = self.pipeline.train_input
            test_input = self.pipeline.test_input
            
            train_f = Container.get_filter_manager(train_input.clazz, train_input.params).predict(data_item=train_input.item)
            if test_input is not None:
                test_f = Container.get_filter_manager(test_input.clazz, test_input.params).predict(data_item=test_input.item)
            
            for f_idx, filter_model in enumerate(self.pipeline.filters):
                filter_manager:BaseFlyManager = Container.get_filter_manager(
                    filter_model.clazz, 
                    filter_model.params, 
                    filter_model.overwrite, 
                    filter_model.store
                )
                
                filter_manager.fit(filter_model.item, train_f)
                
                self.pipeline_filters.append(filter_manager)
                
                train_f = filter_manager.predict(train_input.items[f_idx], train_f)
                if test_input is not None:
                    test_f = filter_manager.predict(test_input.items[f_idx], test_f)

            if test_input is None:
                test_f = train_f

            for idx, metric in enumerate(self.pipeline.metrics):
                m_wrapper = Container.get_metric(metric.clazz, metric.params)
                metric.value = m_wrapper.predict(test_f)
                self.pipeline.metrics[idx] = metric
                
        except Exception as ex:
            raise PipelineExecutionException(ex)
         
        
    def log_metrics(self) -> None:
        print(self.pipeline.metrics)
        for metric in self.pipeline.metrics:
            Container.send_to_logger(message={metric.clazz: metric.value})

    def finish(self) -> None:
        if not Container.logger is None:
            Container.logger.finish()
