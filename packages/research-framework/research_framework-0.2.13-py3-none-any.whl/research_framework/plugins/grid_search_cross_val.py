from typing import Any, List
from sklearn.model_selection import ShuffleSplit, StratifiedShuffleSplit, StratifiedKFold
from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager
from research_framework.base.plugin.base_plugin import BaseFilterPlugin
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.container.container import Container

from rich import print
from research_framework.base.utils.grid_seach import generate_combis, generate_sweep_config
from research_framework.dataset.standard_dataset import StandardDataset
from research_framework.flyweight.flyweight_manager import PassThroughFlyManager, WandbSeepsFlyManager
from research_framework.flyweight.model.item_model import ItemModel
from research_framework.pipeline.model.pipeline_model import MetricModel

import json
import torch
import numpy as np
import pandas as pd
import wandb
from tqdm import tqdm

from research_framework.plugins.data_ingestion_plugins import SaaSPlugin


@Container.bind()
class CrossValGridSearch(BaseFilterPlugin):
    split_algorithms={
        "ShuffleSplit":ShuffleSplit,
        "StratifiedShuffleSplit":StratifiedShuffleSplit,
        "StratifiedKFold":StratifiedKFold
    }
    def __init__(self, split_alg='ShuffleSplit', n_splits=3, test_size=0.3, random_state=43, scorers=[MetricModel(clazz='F1')], refit=True, filters=[]):
        self.n_splits = n_splits
        self.test_size = test_size
        self.random_state = random_state
        self.filters = filters
        self.scorers = scorers
        self.refit = refit
        self.alg = CrossValGridSearch.split_algorithms[split_alg]
        self.best_pipeline:List[BaseWrapper] = []
        self.best_config:str = None

    def get_params(self, _: bool = True) -> dict:
        return json.loads(self.best_config)
    
    def fit(self, x):
        if callable(x) and x.__name__ == "<lambda>":
            x = x()

        print("\n--------------------[CrossValGridSearch]-----------------------\n")
        print(self.filters)
        print("\n---------------------------------------------------------------\n")
        cv = self.alg(
            n_splits=self.n_splits, 
            test_size=self.test_size, 
            random_state=self.random_state
        )

        print(self.filters)
        pbar = tqdm(generate_combis(self.filters), position=0)
        pbar.set_description(f'Processing combinations...')

        combi_dict = {}
        results = {}
        for combi in pbar:
            combi_str = json.dumps(combi)
            combi_dict[combi_str] = combi
            
            for train, test in cv.split(x):
                if type(x) == pd.DataFrame:
                    x_train = x.iloc[train]
                    x_test = x.iloc[test]
                elif type(x) == StandardDataset:
                    x_train = StandardDataset(*x[train])
                    x_test = StandardDataset(*x[test])
                else:
                    x_train = x[train]
                    x_test = x[test]

                
                for clazz, params in combi.items():
                    wrapper:BaseWrapper = Container.get_wrapper(clazz, params)
                    wrapper.fit(x_train)
                    
                    x_train = wrapper.predict(x_train)
                    x_test = wrapper.predict(x_test)
                    
                for metric in self.scorers:
                    m_wrapper = Container.get_metric(metric.clazz)
                    result = results.get(combi_str, [])
                    result.append(m_wrapper.predict(x_test))
                    results[combi_str] = result
        
        print("- Results:")
        print(results)
        print("- Results Means: ")
        results_means = dict(map(lambda x: (x[0], np.mean(x[1])), results.items()))
        print(results_means)
        print("- Max values: ")
        config, value = max(results_means.items(), key=lambda x: x[1])
        print(f'Max Combination –> {config}')
        print(f'Max value       –> {value}')
        print("\n-------------------------------------------\n")
        print("- Refit of best model: ")
        self.best_config = config
        if wandb.run is not None:
            wandb.config.update(self.best_config)
                    
        for clazz, params in combi_dict[config].items():
            wrapper:BaseWrapper = Container.get_wrapper(clazz, params)
            wrapper.fit(x)
            
            self.best_pipeline.append(wrapper)
            x = wrapper.predict(x)
                                    
    
    def predict(self, x): 
        if callable(x) and x.__name__ == "<lambda>":
            x = x()
        
        for wrapper in self.best_pipeline:
            x = wrapper.predict(x)
        
        return x

@Container.bind()
class WandbSeepsAgent(BaseFilterPlugin):
    
    def __init__(self, scorer=MetricModel(clazz='F1'), refit=True, sweep_id=None, metrics=[], filters=[]):
        self.filters = filters
        self.scorer = scorer
        self.metrics = metrics
        self.refit = refit
        self.best_pipeline:WandbSeepsRun = None
        self.best_config:str = None
        self.sweep_id = sweep_id

    def get_params(self, _: bool = True) -> dict:
        return json.loads(self.best_config)
    
    def fit(self, item:ItemModel, overwrite:bool=False):
        dataset = item
        while dataset.prev_model != None:
            dataset = dataset.prev_model
            
        sweep_config = generate_sweep_config(self.filters)
        sweep_config['method'] = 'grid'
        sweep_config['metric'] = {
            'name': self.scorer.clazz,
            'goal': 'maximize' if self.scorer.higher_better else 'minimize'
        }
        if self.sweep_id is None:
            wandb.login()
            sweep_id = wandb.sweep(sweep_config, project=Container.global_config.project_name)
            self.sweep_id = sweep_id
        
        Container.freeze_wandb_logger()
        
        sweep_run = WandbSeepsRun(
            run_id=Container.freeze_id,
            dataset=dataset.name,
            sweep_id=self.sweep_id,
            scorer=self.scorer,
            metrics=self.metrics,
            n_splits=3,
            test_size=0.3,
            random_state=43,
            count=None
        )

        sweep_run.fit(item)
        
        self.best_pipeline = sweep_run
    
        Container.un_freeze_wandb_logger()
        Container.logger.config["Sweep"] = self.sweep_id
        Container.send_to_logger({"Sweep": self.sweep_id}) 
    
    def predict(self, x):
        if self.best_pipeline is None:
            raise Exception("Model not trained")
        return self.best_pipeline.predict(x)
    
@Container.bind()
class WandbSeepsRun(BaseFilterPlugin):
    def __init__(self, dataset, run_id, sweep_id, scorer, metrics, n_splits, test_size, random_state, count):
        self.dataset = dataset
        self.run_id = run_id
        self.count = count
        self.sweep_id = sweep_id
        self.data = None
        self.n_splits = n_splits
        self.test_size = test_size
        self.random_state = random_state
        self.scorer = scorer.clazz
        self.metrics = [metric.clazz for metric in metrics]
        self.best_pipeline:List[BaseWrapper] = []
    
    def train(config):
        with wandb.init(config=config, project=Container.global_config.project_name):
            config = wandb.config
            if config.n_splits > 1:
                cv = ShuffleSplit(
                    n_splits=config.n_splits, 
                    test_size=config.test_size, 
                    random_state=config.random_state
                )
                splits = cv.split(x)
            else:
                splits = list(range(len(x))),list(range(len(x)))
                
            
            x = SaaSPlugin(config.data).predict(None)
            errors = []
            for train, test in splits:
                if type(x) == pd.DataFrame:
                    x_train = x.iloc[train]
                    x_test = x.iloc[test]
                elif issubclass(type(x), torch.utils.data.Dataset):
                    x_train = StandardDataset(x.df.iloc[train, :], torch.utils.data.Subset(x.vectors, train))
                    x_test = StandardDataset(x.df.iloc[test, :], torch.utils.data.Subset(x.vectors, test))
                else:
                    x_train = x[train]
                    x_test = x[test]
                
                for clazz in config.order:
                    wrapper:BaseWrapper = Container.get_wrapper(clazz, config[clazz])
                    wrapper.fit(x_train)
                    
                    x_train = wrapper.predict(x_train)
                    x_test = wrapper.predict(x_test)
                    
                m_wrapper = Container.get_metric(config.scorer)
                errors.append(m_wrapper.predict(x_test))
            
            wandb.log({config.scorer: np.mean(errors)})

            for metric in config.metrics:
                m_wrapper = Container.get_metric(metric)
                wandb.log({metric: m_wrapper.predict(x_test)})

        
    def fit(self, x):
        self.data = x.hash_code
        try:
            wandb.agent(self.sweep_id,  self.train, project=Container.global_config.project_name, count=self.count)
        except wandb.errors.UsageError as x:
            print(x)
        
        api = wandb.Api()
        sweep = api.sweep(f"citius-irlab/{Container.global_config.project_name}/sweeps/{self.sweep_id}")
        best_run = sweep.best_run(order=self.scorer)
        best_conf = best_run.config
        
        if Container.freeze_id is None:
            Container.freeze_id = best_conf['run_id']
            
        print(best_conf)
        x_train = SaaSPlugin(self.data).predict(None)
        
        for clazz in best_conf['order']:
            wrapper:BaseWrapper = Container.get_wrapper(clazz, best_conf[clazz])
            wrapper.fit(x_train)
            x_train = wrapper.predict(x_train)
            
            self.best_pipeline.append(wrapper)
            
        
    def predict(self, x):
        if callable(x) and x.__name__ == "<lambda>":
            x = x()
        
        for wrapper in self.best_pipeline:
            x = wrapper.predict(x)
        
        return x

@Container.bind()
class SimpleWandbSeepsRun(BaseFilterPlugin):
    def __init__(self, dataset, run_id, sweep_id, scorrer, metrics):
        self.dataset = dataset
        self.run_id = run_id
        self.sweep_id = sweep_id
        self.scorrer = scorrer
        self.metrics = metrics
        self.pipeline = None
        self.agent = wandb.agent(self.sweep_id,  self.train, project=Container.global_config.project_name, count=self.count)
        
    def train(config):
        with wandb.init(config=config, project=Container.global_config.project_name):
            config = wandb.config
            
            x = SaaSPlugin(config.data).predict(None)
            errors = []
            
            for clazz in config.order:
                wrapper:BaseWrapper = Container.get_wrapper(clazz, config[clazz])
                wrapper.fit(x)
                
                x = wrapper.predict(x)
                
            m_wrapper = Container.get_metric(config.scorer)
            errors.append(m_wrapper.predict(x))
            
    def fit(self, x):
        self.data = x.hash_code
        
    def predict(self, x):
        if callable(x) and x.__name__ == "<lambda>":
            x = x()
        