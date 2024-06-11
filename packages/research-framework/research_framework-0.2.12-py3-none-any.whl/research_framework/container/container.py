from research_framework.base.container.base_container import BaseContainer
from research_framework.base.container.model.bind_model import BindModel
from research_framework.base.flyweight.base_flyweight import BaseFlyweight
from research_framework.base.pipeline.base_pipeline import BasePipeline
from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.base.storage.base_storage import BaseStorage
from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager

from dotenv import load_dotenv
from typing import Optional
from pymongo import MongoClient
from typing import Dict, Any, Type

import wandb
import os
import sys

from research_framework.container.model.global_config import GlobalConfig
from research_framework.flyweight.flyweight_manager import DummyFlyManager
from research_framework.flyweight.mem_manager import MEMManager
from research_framework.plugins.wrappers import DummyWrapper

load_dotenv()

class Container(BaseContainer):
    fly: BaseFlyweight = None
    client: MongoClient = MongoClient(os.environ["HOST"], tls=False)
    storage: BaseStorage = None
    BINDINGS: Dict[str, BindModel] = dict()
    PIPELINES: Dict[str, BasePipeline] = dict()
    MEM: MEMManager = None
    global_config: GlobalConfig = GlobalConfig()
    logger = None
    freeze_id = None
    
    

    @staticmethod
    def init_wandb_logger(project:str, name:Dict[str, Any], config:Dict[str, Any]=None):
        if Container.global_config.log:
            if wandb.run is None:
                Container.logger = wandb.init(project=project, name=name, settings=wandb.Settings(start_method="fork"), config=config)
    
    @staticmethod
    def freeze_wandb_logger():
        if Container.logger is not None:
            Container.freeze_id = Container.logger.id
            print(f"* Frizzing run_id > {Container.freeze_id}")
            Container.logger.finish()    
    
    @staticmethod
    def update_freezed_run(project:str, run_id:str, update_dict:Dict[str, Any]):
        api = wandb.Api()
        run = api.run(f'citius-irlab/{project}/{run_id}')
        run.config.update(update_dict)
        run.update()

        
    @staticmethod
    def un_freeze_wandb_logger():
        if Container.freeze_id is not None:
            print(f"* Unfrizzing run_id > {Container.freeze_id}")
            Container.logger = wandb.init(id=Container.freeze_id, project=Container.global_config.project_name, name=Container.global_config.run_name, resume="must", reinit=True)
    
    
    @staticmethod
    def send_to_logger(message:Dict[str, Any], step:Optional[int] = None):
        if Container.global_config.log:
            if step is None:
                wandb.log(message)
            else:
                wandb.log(message, step=step)
         
    @staticmethod
    def register_dao(collection):
        def fun_decorator(fun):
            if "pytest" in sys.modules:
                fun()(Container.client['framework_test'][collection])
            else:
                fun()(Container.client['framework_deploy'][collection])
            return fun
        return fun_decorator
    
    @staticmethod
    def register_pipeline(func):
        Container.PIPELINES[func.__name__] = func
        return func

    @staticmethod
    def bind(manager:Optional[BaseFlyManager] = DummyFlyManager, wrapper:Optional[BaseWrapper] = DummyWrapper):
        def inner(func):
            Container.BINDINGS[func.__name__] = BindModel(
                manager=manager,
                wrapper=wrapper,
                plugin=func
            )
            return func
        return inner
    
    @staticmethod
    def wrap_object(model_clazz:str, object:object) -> BaseWrapper:
        bind: BindModel  = Container.BINDINGS[model_clazz]   
        return bind.wrapper(object)
    
    @staticmethod
    def get_wrapper(clazz:str, params:Dict[str, Any]) -> BaseWrapper:
        bind: BindModel  = Container.BINDINGS[clazz]
        return bind.wrapper(bind.plugin(**params))
    
    @staticmethod
    def get_filter_manager(clazz:str, params:Dict[str, Any], overwrite:Optional[bool]=None, store:Optional[bool]=None) -> BaseFlyManager:
        bind: BindModel  = Container.BINDINGS[clazz]
        
        return bind.manager(
            bind.wrapper(bind.plugin(**params)),
            store if store is not None else Container.global_config.store,
            overwrite if overwrite is not None and not Container.global_config.overwrite else Container.global_config.overwrite
        )
    
    @staticmethod
    def get_model(clazz:str, params:Dict[str, Any]) -> BasePlugin:
        bind: BindModel  = Container.BINDINGS[clazz]
        return bind.plugin(**params)
    
    @staticmethod
    def get_clazz(clazz:str) -> Type[BasePlugin]:
        bind: BindModel  = Container.BINDINGS[clazz]
        return bind.plugin
    
    @staticmethod
    def get_metric(clazz:str, config:Optional[Dict[str, Any]] = None) -> BaseFlyManager:
        bind: BindModel  = Container.BINDINGS[clazz]
        if config is None:
            return bind.manager(bind.wrapper(bind.plugin())) 
        else:
            return bind.manager(bind.wrapper(bind.plugin(**config))) 