import os
from typing import Any

from pymongo import MongoClient
from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.container.container import Container
from research_framework.dataset.standard_dataset import StandardDataset
from research_framework.flyweight.flyweight import FlyWeight
from research_framework.flyweight.model.item_simple_model import ItemSimpleModel
from research_framework.pipeline.model.pipeline_model import FilterModel, InputFilterModel, MetricModel, SimplePipelineModel
from research_framework.pipeline.pipeline import SimpleFitPredictPipeline
from research_framework.pipeline.pipeline_manager import PipelineManager
from research_framework.storage.local_storage import LocalStorage

import pytest
import pandas as pd
import json
import copy
from rich import print

test_pipeline = SimplePipelineModel(
        name='pipeline para tests',
        train_input= 
            InputFilterModel(
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
            InputFilterModel(
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
                clazz="FilterRowsByNwords",
                params={
                    "upper_cut": 100,
                    "lower_cut": 10,
                    "df_headers": ["id", "text", "label"]
                }
            ),
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
                    "n_components":1024
                } 
            ),
            FilterModel(
                clazz="DoomyPredictor",
                params={
                    "n_epoch": 3,
                    "batch_size": 500,
                    "emb_d": 1024
                }
            )
        ],
        metrics = [
            MetricModel(
                clazz="F1"
            )
        ]
    )


@pytest.fixture
def simple_pipeline():
    print("\n* Container content: ")
    print(Container.BINDINGS)
    Container.storage = LocalStorage('data/cache')
    Container.fly = FlyWeight()
    
    return PipelineManager.start_pipeline(project='test', pl_conf=copy.deepcopy(test_pipeline), log=False, overwrite=True, store=True, storage=LocalStorage('data/cache'))
    

def aux_delete_pipeline_generated_items(pipeline:SimpleFitPredictPipeline):
    print("- Train data:")
    
    print(f'{pipeline.pipeline.train_input.item.name} : {pipeline.pipeline.train_input.item.hash_code} deleted? {Container.fly.unset_item(pipeline.pipeline.train_input.item.hash_code)}')
    print(f'{pipeline.pipeline.test_input.item.name} : {pipeline.pipeline.test_input.item.hash_code} deleted? {Container.fly.unset_item(pipeline.pipeline.test_input.item.hash_code)}')

    for item in pipeline.pipeline.train_input.items:
        try:
            print(f'{item.name} : {item.hash_code} deleted? {Container.fly.unset_item(item.hash_code)}')
        except Exception as ex:
            print(ex)
    print("- Test data:")
    for item in pipeline.pipeline.test_input.items:
        try:
            print(f'{item.name} : {item.hash_code} deleted? {Container.fly.unset_item(item.hash_code)}')
        except Exception as ex:
            print(ex)
            
    print("- Trained models:")
    for plugin_filter in pipeline.pipeline.filters:
        if not plugin_filter.item is None:
            try:
                print(f'{plugin_filter.item.name} : {plugin_filter.item.hash_code} deleted? {Container.fly.unset_item(plugin_filter.item.hash_code)}')
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
    Container.fly = FlyWeight()
    
    return PipelineManager.start_pipeline(project='test', pl_conf=copy.deepcopy(test_pipeline), log=False, overwrite=False, store=True, storage=LocalStorage('data/cache'))

    


def test_stored_items_types_and_wrappers(delete_pipeline_items: Any):
    pipeline:SimpleFitPredictPipeline = delete_pipeline_items
    for item in pipeline.pipeline.train_input.items:
        assert type(item) == ItemSimpleModel
        if item.stored:
            obj2 = Container.fly.get_data_from_item(item)
            assert type(obj2) == pd.DataFrame or type(obj2) == StandardDataset

    for item in pipeline.pipeline.test_input.items:
        if item.stored:
            assert type(item) == ItemSimpleModel
            obj2 = Container.fly.get_data_from_item(item)
            assert type(obj2) == pd.DataFrame or type(obj2) == StandardDataset

    for plugin_filter in pipeline.pipeline.filters:
        if not plugin_filter.item is None:
            if plugin_filter.item.stored:
                item = plugin_filter.item
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