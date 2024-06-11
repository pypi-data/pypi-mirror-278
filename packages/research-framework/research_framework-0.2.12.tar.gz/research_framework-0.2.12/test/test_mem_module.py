from typing import Any
import sys

from research_framework.container.container import Container
from research_framework.flyweight.flyweight import SimpleFlyWeight
from research_framework.flyweight.mem_manager import MEMManager
from research_framework.pipeline.model.pipeline_model import FilterModel, SimpleInputFilterModel, MetricModel, SimplePipelineModel
from research_framework.plugins.wandb_sweep_plugins import *
from research_framework.plugins.unsupervised_predictor import *
from research_framework.pipeline.pipeline_manager import PipelineManager
from research_framework.storage.local_storage import LocalStorage

from test.plugins.test_mem_plugins import *
from test.metrics.test_metrics import *
from test.metrics.test_metrics import FIT_TEST_STRING, PREDICT_TEST_STRING

import pytest
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
                clazz="MeMFilterTester",
                params={}
            )
        ],
        metrics = [
            MetricModel(
                clazz="MeMMetricTester"
            )
        ]
    )


@pytest.fixture
def prepare_mem_10_filters():
    print("\n* Container content: ")
    print(Container.BINDINGS)
    Container.storage = LocalStorage('data/cache')
    Container.fly = SimpleFlyWeight()
    Container.MEM = MEMManager()
    
    filled_config = PipelineManager.fill_pipline_items(copy.deepcopy(test_pipeline))
    PipelineManager.start_pipeline(project='test', pl_conf=filled_config, log=False, overwrite=True, store=True, storage=LocalStorage('data/cache'))
    return filled_config


def aux_delete_pipeline_generated_items(pipeline:SimplePipelineModel):
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
def delete_pipeline_items(prepare_mem_10_filters: SimplePipelineModel, request: type[pytest.FixtureRequest]):
    request.addfinalizer(lambda: aux_delete_pipeline_generated_items(prepare_mem_10_filters))
    return prepare_mem_10_filters

def test_empty_pipeline_with_prev_stored_items(delete_pipeline_items: SimplePipelineModel):
    stored_keys = Container.MEM.get_all_storage_and_keys()
    Container.MEM.empty()
    assert all(list(map(lambda x: x.VARS == {}, Container.MEM.FILTER_VARS.values())))
    assert all(list(map(lambda x: x[0].check_if_exists(x[1]) == False, stored_keys)))


def test_clear_pipeline_with_prev_stored_items(delete_pipeline_items: SimplePipelineModel):
    stored_keys = Container.MEM.get_all_storage_and_keys()
    Container.MEM.clear()
    assert Container.MEM.FILTER_VARS == {}
    assert all(list(map(lambda x: x[0].check_if_exists(x[1]) == False, stored_keys)))
    
def test_pipeline_with_prev_stored_items(delete_pipeline_items: Any):
    print(prepare_mem_10_filters)
    print(Container.MEM)
    assert Container.MEM[-1]["X"] == FIT_TEST_STRING
    assert Container.MEM[-1]["X2"] == PREDICT_TEST_STRING
    Container.MEM.empty()
    assert Container.MEM[-1].VARS == {}
    assert Container.MEM[-1].VARS == {}
    print(Container.MEM)