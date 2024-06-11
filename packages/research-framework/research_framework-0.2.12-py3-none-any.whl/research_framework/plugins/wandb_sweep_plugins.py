from research_framework.base.plugin.base_plugin import BaseFilterPlugin
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.container.container import Container

from research_framework.base.utils.grid_seach import generate_sweep_config
from research_framework.flyweight.flyweight_manager import FitPredictFlyManager
from research_framework.flyweight.model.item_model import ItemModel
from research_framework.pipeline.model.pipeline_model import InputFilterModel, MetricModel

import json
import wandb

from research_framework.plugins.cv_strategies_plugins import RunEnum
from research_framework.plugins.grid_search_cross_val import WandbSeepsRun
from research_framework.plugins.wrappers import PullWrapper


@Container.bind(FitPredictFlyManager, PullWrapper) #TODO Revisar esto porque parece más un parche que otra cosa
class SimpleWandbSeepsAgent(BaseFilterPlugin):
    
    def __init__(self, scorer=MetricModel(clazz='F1'), run_type=RunEnum.unsupervised.name, metrics=[], run_params={}, sweep_id=None, refit=True, filters=[]):
        self.filters = filters
        self.scorer = scorer
        self.refit = refit
        self.run_type = run_type
        self.run_params = run_params
        self.metrics = metrics
        self.sweep_id = sweep_id

        sweep_config = generate_sweep_config(self.filters)
        sweep_config['method'] = 'grid'
        sweep_config['parameters']['dataset'] = {'value':Container.global_config.dataset}
        sweep_config['metric'] = {
            'name': self.scorer.clazz,
            'goal': 'maximize' if self.scorer.higher_better else 'minimize'
        }
        
        print(sweep_config)
        
        if sweep_id is None:
            self.sweep_id = wandb.sweep(sweep_config, project=Container.global_config.project_name)
        else:
            self.sweep_id = sweep_id
            
        Container.send_to_logger({"Sweep": self.sweep_id})
            
        self.best_conf:str = None
        self.best_pipeline:WandbSeepsRun = None
    
    def fit(self, x):
        RunClazz = getattr(RunEnum, self.run_type).value
        run = RunClazz(x, scorer=self.scorer, metrics=self.metrics, dataset=Container.global_config.dataset, **self.run_params)
        
        Container.freeze_wandb_logger()
        
        api = wandb.Api()
        sweep = api.sweep(f"citius-irlab/{Container.global_config.project_name}/sweeps/{self.sweep_id}")

        print(sweep.state)
        if sweep.state == "PENDING":
            wandb.agent(self.sweep_id, lambda: {
                run.init(),
                run.exec(), 
                run.log_metrics(),
                run.finish()
            }, project=Container.global_config.project_name)
            
            wandb.teardown()
        
        
        best_run = sweep.best_run(order=self.scorer.clazz)
        
        self.best_conf = best_run.config
        
        input_dm = InputFilterModel(name="", clazz='MeMPlugin', params={"obj": x})
        
        self.best_pipeline = run.get_pipeline(best_run.name, best_run.config, input_dm)
        self.best_pipeline.init()
        self.best_pipeline.fit(input_dm)
        
    def predict(self, x):
        if self.best_pipeline is None:
            raise Exception("Model not trained")
        
        return self.best_pipeline.predict(InputFilterModel(name="", clazz='MeMPlugin', params={"obj": x}))

