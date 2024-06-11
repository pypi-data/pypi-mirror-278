import pytest
from typing import Any, Tuple
from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager
from research_framework.container.container import Container
from research_framework.container.model.global_config import GlobalConfig
from research_framework.flyweight.model.item_model import ItemModel
from research_framework.flyweight.model.item_dao import ItemDao
from research_framework.flyweight.flyweight import FlyWeight
from research_framework.storage.google_storage import BucketStorage
from test.plugins.test_plugin import TestPassThroughFilterWrapper

@pytest.fixture
def save_new_item():
    Container.fly = FlyWeight()
    Container.storage = BucketStorage() 
    manager = Container.get_filter_manager(TestPassThroughFilterWrapper.__name__, {})
    
    data_item = ItemModel(name="Test_HASHCODE", hash_code="Test_NAME", clazz='Test', params={})
    data = manager.predict(data_item, {})

    return  data_item, data


@pytest.fixture
def save_new_item_delete_at_the_end(save_new_item:Tuple[ItemModel, Any], request):
    data_item, _ = save_new_item
    request.addfinalizer(lambda: Container.fly.unset_item(data_item.hash_code))
    return save_new_item

def test_save_new_item(save_new_item_delete_at_the_end:Tuple[ItemModel, Any]):
    data_item, data = save_new_item_delete_at_the_end

    if callable(data):
        data = data()
    
    assert data == TestPassThroughFilterWrapper().predict(None)
    assert True == Container.storage.check_if_exists(data_item.hash_code)
    assert data == Container.storage.download_file(data_item.hash_code)
    stored:ItemModel = ItemModel(**ItemDao.findOneByHashCode(data_item.hash_code))
    assert stored.hash_code == data_item.hash_code
    

def test_save_existing_item(save_new_item_delete_at_the_end: Tuple[ItemModel, Any]):
    data_item, _ = save_new_item_delete_at_the_end
    
    manager = Container.get_filter_manager(TestPassThroughFilterWrapper.__name__, {})
    new_data = manager.predict(data_item, {})
    
    assert callable(new_data)
    assert 1 == len(list(ItemDao.findByHashCode(data_item.hash_code)))
    
def test_save_existing_item_with_overwrite_global(save_new_item_delete_at_the_end: Tuple[ItemModel, Any]):
    data_item, _ = save_new_item_delete_at_the_end
    
    Container.global_config = GlobalConfig(
        overwrite=True
    )   
    
    manager = Container.get_filter_manager(TestPassThroughFilterWrapper.__name__, {})
    new_data = manager.predict(data_item, {})
    
    print(Container.global_config.model_dump())
    assert not callable(new_data)
    assert 1 == len(list(ItemDao.findByHashCode(data_item.hash_code)))
    
    

def test_save_existing_item_with_overwrite_global_false_and_filter_overwrite(save_new_item_delete_at_the_end: Tuple[ItemModel, Any]):
    data_item, _ = save_new_item_delete_at_the_end
    
    Container.global_config = GlobalConfig(
        overwrite=False
    )   
    
    manager = Container.get_filter_manager(TestPassThroughFilterWrapper.__name__, {}, overwrite=True)
    new_data = manager.predict(data_item, {})
    
    print(Container.global_config.model_dump())
    assert not callable(new_data)
    assert 1 == len(list(ItemDao.findByHashCode(data_item.hash_code)))
    
def test_delete_existing_item(save_new_item: Tuple[ItemModel, Any]):
    data_item, _ =  save_new_item
    
    Container.fly.unset_item(data_item.hash_code)
    
    assert ItemDao.findOneByHashCode(data_item.hash_code) == None
    assert Container.storage.check_if_exists(data_item.hash_code) == False
    
