from typing import Any

from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.container.container import Container
from research_framework.dataset.standard_dataset import StandardDataset
from research_framework.flyweight.flyweight import SimpleFlyWeight
from research_framework.flyweight.mem_manager import MEMManager
from research_framework.flyweight.model.item_simple_model import ItemSimpleModel
from research_framework.pipeline.exceptions.pipeline_exceptions import PipelineExecutionException
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
import traceback

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
            # FilterModel(
            #     clazz="FilterRowsByNwords",
            #     params={
            #         "upper_cut": 100,
            #         "lower_cut": 10,
            #         "df_headers": ["id", "text", "label"]
            #     }
            # ),
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
                params={
                    "scorer": MetricModel(clazz='F1'),
                    "metrics": [
                        #MetricModel(clazz='NMI')
                    ],
                    "run_type": "shuffle_cv",
                    "run_params": {
                        "n_splits": 3,
                        "test_size": 0.2,
                        "random_state": 47
                    },
                    "filters": [
                        FilterModel(
                            clazz="DoomyPredictor",
                            params={
                                "emb_d": 5,
                                
                                "hidden_d":[2, 4, 8]
                            }
                        )
                    ],
                }
            )
        ],
        metrics = [
            MetricModel(
                clazz="Precision"
            )
        ]
    )


@pytest.fixture
def simple_pipeline():
    try:
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
    except PipelineExecutionException:
        traceback.print_exc()
        assert False
    

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
    try:
        Container.storage = LocalStorage('data/cache')
        Container.fly = SimpleFlyWeight()
        Container.MEM = MEMManager(overwrite=True)
        
        filled_config = PipelineManager.fill_pipline_items(copy.deepcopy(test_pipeline))
        
        PipelineManager.start_pipeline(project='test', pl_conf=filled_config, log=False, overwrite=False, store=True, storage=LocalStorage('data/cache'))
    except PipelineExecutionException:
        traceback.print_exc()
        assert False
    


def test_stored_items_types_and_wrappers(delete_pipeline_items: Any):

    pipeline:SimpleFitPredictPipeline = delete_pipeline_items
    print(pipeline.pipeline)
    for item in pipeline.pipeline.train_input.items.values():
        assert type(item) == ItemSimpleModel
        if item.stored:
            obj2 = Container.fly.get_data_from_item(item)
            assert type(obj2) == pd.DataFrame or type(obj2) == StandardDataset

    for item in pipeline.pipeline.test_input.items.values():
        if item.stored:
            assert type(item) == ItemSimpleModel
            obj2 = Container.fly.get_data_from_item(item)
            assert type(obj2) == pd.DataFrame or type(obj2) == StandardDataset

    for plugin_filter in pipeline.pipeline.filters:
        if not plugin_filter.item is None:
            print("______________________")
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