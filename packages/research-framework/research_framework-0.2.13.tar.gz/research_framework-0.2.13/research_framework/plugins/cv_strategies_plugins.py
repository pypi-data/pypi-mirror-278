from sklearn.model_selection import ShuffleSplit
from enum import Enum
import wandb
import wandb.sdk
import numpy as np

from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.container.container import Container
from research_framework.dataset.standard_dataset import StandardDataset
from research_framework.pipeline.exceptions.run_exceptions import RunExecutionException
from research_framework.pipeline.model.pipeline_model import FilterModel, WandbRunPipelineModel


class UnsupervisedRun:
    def __init__(self, data, scorer, metrics, dataset):
        self.data = data
        self.scorer = scorer
        self.metrics = metrics
        self.dataset = dataset
        self.out_metrics = {}
    
    def init(self):
        run = wandb.init(reinit=True)
        assert run is not None
        assert type(run) is wandb.sdk.wandb_run.Run
        
    def exec(self):
        config = wandb.config
        
        try:
            x_train:StandardDataset = self.data
            
            for clazz in config.order:
                wrapper:BaseWrapper = Container.get_wrapper(clazz, config[clazz])
                wrapper.fit(x_train)
                
                x_train = wrapper.predict(x_train)

            m_wrapper = Container.get_metric(self.scorer.clazz, self.scorer.params)
            
            self.out_metrics[self.scorer.clazz] = m_wrapper.predict(x_train)
            
            for metric in self.metrics:
                m_wrapper = Container.get_metric(metric.clazz, metric.params)
                
                self.out_metrics[metric.clazz] = m_wrapper.predict(x_train)
        except Exception as ex:
                raise RunExecutionException(ex)
        
    def log_metrics(self):
        wandb.log(self.out_metrics)
    
    def get_pipeline(self, name, config, train_dm):
        
        print(self.metrics)
        pl_conf = WandbRunPipelineModel(
            name=f'CrossValPipeline_{name}',
            train_input=train_dm,
            filters=[FilterModel(clazz=clazz, params=config[clazz]) for clazz in config["order"]],
            metrics=self.metrics
        )

        pipeline = Container.PIPELINES[pl_conf._clazz](pl_conf)

        return pipeline
    
    def finish(self):
        wandb.finish()


"""
TODO Todavía no se cómo tengo que hacer
"""   
class SupervisedRun:
    def __init__(self, train_data, test_data, scorer, metrics, dataset, group_name=None, run_name=None):
        self.train_data = train_data
        self.test_data = test_data
        self.scorer = scorer
        self.metrics = metrics
        self.dataset = dataset
        self.group_name = group_name
        self.run_name = run_name
        self.out_metrics = {}
    
    def init(self):
        run = wandb.init(group=self.group_name, name=self.run_name, reinit=True)
        assert run is not None
        assert type(run) is wandb.sdk.wandb_run.Run
        
    def exec(self):
        try:
            config = wandb.config
            print(f'Config > {config}')
            
            train_data = self.train_data
            test_data = self.test_data
            
            for clazz in config.order:
                wrapper:BaseWrapper = Container.get_wrapper(clazz, config[clazz])
                wrapper.fit(self.train_data)
                
                train_data = wrapper.predict(train_data)
                test_data = wrapper.predict(test_data)

            m_wrapper = Container.get_metric(self.scorer.clazz, self.scorer.params)
            
            self.out_metrics[self.scorer.clazz] = m_wrapper.predict(test_data)
            
            for metric in self.metrics:
                m_wrapper = Container.get_metric(metric.clazz, metric.params)
                self.out_metrics[metric.clazz] = m_wrapper.predict(test_data)
            
        except Exception as ex:
            raise RunExecutionException(ex)
        
    def get_pipeline(self, name, config):
        pipeline = []
        for clazz in config["order"]:
            wrapper:BaseWrapper = Container.get_wrapper(clazz, config[clazz])
            wrapper.fit(self.data)
            pipeline.append(wrapper)
        return pipeline
    
    def log_metrics(self):
        wandb.log(self.metrics)
        
    def finish(self):
        wandb.finish()

class ShuffleCVRun:
    def __init__(self, data, scorer, dataset, metrics=[], n_splits=2, test_size=0.2, random_state=7):
        self.data = data
        self.metrics = metrics
        self.scorer = scorer
        self.dataset = dataset
        self.n_splits = n_splits
        self.test_size = test_size
        self.random_state = random_state
        self.out_metrics = {}
    
    def init(self):
        run = wandb.init(reinit=True)
        assert run is not None
        assert type(run) is wandb.sdk.wandb_run.Run
        
    def exec(self):
        cv = ShuffleSplit(
            n_splits=self.n_splits, 
            test_size=self.test_size, 
            random_state=self.random_state
        )
        
        splits = cv.split(self.data)
    
        for split,(train_idx, test_idx) in enumerate(splits):
            print(f'* Split {split} ->')
            
            train_data = StandardDataset(*self.data[train_idx])
            test_data = StandardDataset(*self.data[test_idx])

            s_run = SupervisedRun(train_data, test_data, dataset=self.dataset, scorer=self.scorer, metrics=self.metrics)
            s_run.exec()
        
        for k,v in s_run.out_metrics.items():
            m_acum = self.out_metrics.get(k, []) 
            m_acum.append(v)
            self.out_metrics[k] = m_acum
            
    def log_metrics(self):
        wandb.log(dict(map(lambda kv: (kv[0],np.mean(kv[1])), self.out_metrics.items())))
    
    def get_pipeline(self, name, config, train_dm):
        pl_conf = WandbRunPipelineModel(
            name=f'CrossValPipeline_{name}',
            train_input=train_dm,
            filters=[FilterModel(clazz=clazz, params=config[clazz]) for clazz in config["order"]],
            metrics=self.metrics
        )
        pipeline = Container.PIPELINES[pl_conf._clazz](pl_conf)
        return pipeline
    
    def finish(self):
        wandb.finish()

class RunEnum(Enum):
    unsupervised = UnsupervisedRun
    superised = SupervisedRun
    shuffle_cv = ShuffleCVRun