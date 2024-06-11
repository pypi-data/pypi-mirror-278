from typing import Any

from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.container.container import Container
from research_framework.dataset.standard_dataset import StandardDataset
from research_framework.flyweight.flyweight import SimpleFlyWeight
from research_framework.flyweight.mem_manager import MEMManager
from research_framework.flyweight.model.item_simple_model import ItemSimpleModel
from research_framework.pipeline.model.pipeline_model import FilterModel, InputFilterModel, MetricModel, SimpleInputFilterModel, SimplePipelineModel
from research_framework.plugins.wandb_sweep_plugins import *
from research_framework.plugins.unsupervised_predictor import *
from research_framework.pipeline.pipeline import SimpleFitPredictPipeline
from research_framework.pipeline.pipeline_manager import PipelineManager
from research_framework.storage.local_storage import LocalStorage

import pytest
import pandas as pd
import copy
from rich import print

test_pipeline = SimplePipelineModel(
        name='pipeline para tests',
        train_input= 
            SimpleInputFilterModel(
                clazz='CSVPlugin',
                name='sample_2000_standard_depression_train_2017.csv',
                params={
                    "filepath_or_buffer":"test/data/sample_2000_standard_depression_train_2017.csv",
                    "sep": ",",
                    "index_col": 0,
                },
            )
        ,
        test_input =
            SimpleInputFilterModel(
                clazz='CSVPlugin',
                name='sample_2000_standard_depression_test_2017.csv',
                params={
                    "filepath_or_buffer":"test/data/sample_2000_standard_depression_test_2017.csv",
                    "sep": ",",
                    "index_col": 0,
                }
            )
        ,
        filters= [
            FilterModel(
                overwrite=True,
                clazz="Tf",
                params={
                    "lowercase":True
                }
            ),
            FilterModel(
                clazz="MaTruncatedSVD",
                params={
                    "n_components":5
                } 
            ),
            FilterModel(
                clazz="SimpleWandbSeepsAgent",
                alt_params = {
                    "sweep_id" : "ytvxvhj2"
                },
                params={
                    "scorer": MetricModel(clazz='NMI'),
                    "metrics": [
                        MetricModel(
                            clazz="Silhouette"
                        )
                    ],
                    "run_type":"unsupervised",
                    "run_params": {
                        
                    },
                    "filters": [
                        FilterModel(
                            clazz="Kmeans",
                            params={
                                "refit": True,
                                "n_init": "auto",
                                "n_clusters": [3, 4],
                            }
                        )
                    ],
                }
            )
        ],
        metrics = [
            MetricModel(
                clazz="Silhouette"
            )
        ]
    )


@pytest.fixture
def simple_pipeline():
    print("\n* Container content: ")
    print(Container.BINDINGS)
    Container.storage = LocalStorage('data/cache')
    Container.fly = SimpleFlyWeight()
    Container.MEM = MEMManager(overwrite=True)
    
    filled_config = PipelineManager.fill_pipline_items(copy.deepcopy(test_pipeline))

    print("____________________ Start Pipeline _________________________")
    print(filled_config)
    print("*************************************************************")
    
    return PipelineManager.start_pipeline(project='test', pl_conf=filled_config, log=True, overwrite=True, store=True, storage=LocalStorage('data/cache'))
    

def aux_delete_pipeline_generated_items(pipeline:SimpleFitPredictPipeline):
    pipeline:SimplePipelineModel = pipeline.pipeline
    
    print("- Input Data:")
    print("__________________________________________________________________________")
    print(pipeline.train_input.item)
    print(f' * {pipeline.train_input.item.hash_code} deleted? {Container.fly.unset_item(pipeline.train_input.item.hash_code)}')
    print("__________________________________________________________________________")
    print(pipeline.test_input.item)
    print(f' * {pipeline.test_input.item.hash_code} deleted? {Container.fly.unset_item(pipeline.test_input.item.hash_code)}')
    print("__________________________________________________________________________")
    print("- Filters:")
    for filter_model in pipeline.filters:
        try:
            filter_hashcode = filter_model.item.hash_code
            print("__________________________________________________________________________")
            print(filter_model.item)
            print(f' * {filter_hashcode} deleted? {Container.fly.unset_item(filter_hashcode)}')
            print("__________________________________________________________________________")
            f_train_item = pipeline.train_input.items[filter_hashcode]
            f_test_item = pipeline.test_input.items[filter_hashcode]
            print("__________________________________________________________________________")
            print(f_train_item)
            print(f' * {f_train_item.hash_code} deleted? {Container.fly.unset_item(f_train_item.hash_code)}')
            print("__________________________________________________________________________")
            print(f_test_item)
            print(f' * {f_test_item.hash_code} deleted? {Container.fly.unset_item(f_test_item.hash_code)}')
            print("__________________________________________________________________________")

        except Exception as ex:
            print(ex)
        
    
@pytest.fixture
def delete_pipeline_items(simple_pipeline: SimpleFitPredictPipeline, request: type[pytest.FixtureRequest]):
    request.addfinalizer(lambda: aux_delete_pipeline_generated_items(simple_pipeline))
    return simple_pipeline


def test_pipeline_with_prev_stored_items(delete_pipeline_items: Any):
    pipeline:SimpleFitPredictPipeline = delete_pipeline_items

    print("\n* Container content: ")
    print(Container.BINDINGS)
    Container.storage = LocalStorage('data/cache')
    Container.fly = SimpleFlyWeight()
    
    filled_config = PipelineManager.fill_pipline_items(copy.deepcopy(test_pipeline))
    
    PipelineManager.start_pipeline(project='test', pl_conf=filled_config, log=False, overwrite=False, store=True, storage=LocalStorage('data/cache'))
    


def test_stored_items_types_and_wrappers(delete_pipeline_items: Any):
    pipeline:SimpleFitPredictPipeline = delete_pipeline_items
    print("_____________________ THE PIPELINE ________________")
    print(pipeline.pipeline)
    print("****************************************************")
    print("____________________ TRAIN INPUT ____________________")
    for item in pipeline.pipeline.train_input.items.values():
        assert type(item) == ItemSimpleModel
        if item.stored:
            obj2 = Container.fly.get_data_from_item(item)
            assert type(obj2) == pd.DataFrame or type(obj2) == StandardDataset
    print("****************************************************")
    print("____________________ TRAIN INPUT ____________________")
    for item in pipeline.pipeline.test_input.items.values():
        if item.stored:
            assert type(item) == ItemSimpleModel
            obj2 = Container.fly.get_data_from_item(item)
            assert type(obj2) == pd.DataFrame or type(obj2) == StandardDataset
    print("****************************************************")
    print("___________ TESTING PLUIGIN FILTERS ___________")
    for plugin_filter in pipeline.pipeline.filters:
        if not plugin_filter.item is None:
            
            print(plugin_filter)
            print("******************************")
            if plugin_filter.item.stored:
                print(plugin_filter)
                item = plugin_filter.item
                print(item)
                assert type(item) == ItemSimpleModel
                obj = Container.fly.wrap_plugin_from_cloud(item.params)
                assert issubclass(type(obj), BaseWrapper)
                obj2 = Container.fly.get_data_from_item(item)
                assert issubclass(type(obj2), BasePlugin)
                
            
def test_metrics(delete_pipeline_items: Any):
    pipeline:SimpleFitPredictPipeline = delete_pipeline_items
    for metric in pipeline.pipeline.metrics:
        print(f'- {metric.clazz} : {metric.value}')

    assert True