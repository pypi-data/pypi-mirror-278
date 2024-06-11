from typing import Any, Dict
from research_framework.base.flyweight.base_flyweight import BaseFlyweight
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.flyweight.model.item_model import ItemModel
from research_framework.flyweight.model.item_simple_model import ItemSimpleModel
from research_framework.flyweight.model.item_dao import ItemDao
from research_framework.container.container import Container

import json
import hashlib
import traceback
import pymongo

from research_framework.plugins.data_ingestion_plugins import SaaSPlugin
from pymongo.errors import ConnectionFailure, OperationFailure


KW_MODEL = "Model"
KW_DATA = "Data"


class FlyWeight(BaseFlyweight):

    @staticmethod
    def hashcode_from_name(name):
        hashable = f'{name}'.encode('utf-8')
        return hashlib.sha1(hashable).hexdigest()
    
    @staticmethod
    def item_from_name(name):
        hash_code = hashlib.sha1(f'{name}'.encode('utf-8')).hexdigest()
        return ItemModel(
                    name=name,
                    hash_code=hash_code,
                    clazz='SaaSPlugin',
                    params={
                        "drive_ref": hash_code,
                    }
                )
    @staticmethod
    def item_from_name_and_prev(name:str, prev:ItemModel):
        hash_code = hashlib.sha1(name.encode('utf-8')).hexdigest()
        return ItemModel(
                    name=name,
                    hash_code=hash_code,
                    prev_model=prev,
                    clazz='SaaSPlugin',
                    params={
                        "drive_ref": hash_code,
                    }
                )
        
    @staticmethod
    def hashcode_from_config(clazz, params):
        hashable = f'{clazz}{json.dumps(params)}'.encode('utf-8')
        return hashlib.sha1(hashable).hexdigest()
         
    @staticmethod
    def append_to_hashcode(hashcode, hashcode2, is_model=False):
        hashable = f'{hashcode}_{hashcode2}[{KW_MODEL if is_model else KW_DATA}]'.encode('utf-8')
        return hashlib.md5(hashable).hexdigest()
    

    @staticmethod
    def run_transaction_with_retry(txn_func, session):
        success = False
        while True:
            try:
                with session.start_transaction():
                    success = txn_func(session, success)  # performs transaction
                break
            except (ConnectionFailure, OperationFailure) as exc:
                # If transient error, retry the whole transaction
                if exc.has_error_label("TransientTransactionError"):
                    print("TransientTransactionError, retrying transaction ...")
                    continue
                else:
                    raise
    
    @staticmethod
    def commit_with_retry(session):
        while True:
            try:
                # Commit uses write concern set at transaction start.
                session.commit_transaction()
                print("Transaction committed.")
                break
            except (ConnectionFailure, OperationFailure) as exc:
                # Can retry commit
                if exc.has_error_label("UnknownTransactionCommitResult"):
                    print("UnknownTransactionCommitResult, retrying commit operation ...")
                    continue
                else:
                    print("Error during commit ...")
                    raise

    
    def get_item(self, hash_code):
        response = ItemDao.findOneByHashCode(hash_code)
        if response != None:
            doc = ItemModel(**response)
            return doc
        return None
    
    def get_data_from_item(self, item:ItemModel):
        return SaaSPlugin(**item.params).predict(None)
    
    def wrap_plugin_from_cloud(self, cloud_params:Dict[str, Any]) -> BaseWrapper:
        print(cloud_params)
        obj = SaaSPlugin(**cloud_params).predict(None)
        print(obj)
        return Container.wrap_object(obj.__class__.__name__, obj)
    
    def set_item(self, item:ItemModel, data:Any, overwrite:bool=False):
        with Container.client.start_session() as session:
            # with session.start_transaction():
            try:
                def callback(session, success):
                    item.stored = True
                    print("- Preparing transaction...")
                    result = ItemDao.create(item, session=session)
                    print("- Transaction prepared now proceding to upload!")
                    if not success:
                        if result.inserted_id is not None:
                            Container.storage.upload_file(file=data, file_name=item.hash_code)
                            return True
                        else:
                            raise Exception("Id already exists")
                    else:
                        print(" * Previous try succeded executing callback!")
                        return True

                if not overwrite:
                    FlyWeight.run_transaction_with_retry(callback, session)
                    return True
                else:
                    Container.storage.upload_file(file=data, file_name=item.hash_code)
                    return True
                    
            except Exception as ex:
                print(traceback.print_exc())
                try:
                    Container.storage.delete_file(item.hash_code)
                except Exception as ex2:
                    print(ex2)
                    return False
                print(ex)
                return False
                
    def unset_item(self, hashcode:str):
        with Container.client.start_session() as session:
            # with session.start_transaction():
            try:
                def callback(session, success):
                    result = ItemDao.deleteByHashcode(hashcode, session=session)
                    if not success:
                        if result.deleted_count >= 1:
                            Container.storage.delete_file(hashcode)
                            return True
                        else:
                            raise Exception(f"Couln't delete {hashcode}")
                    else:
                        print(" * Previous try succeded executing callback!")
                        return True
                    
                FlyWeight.run_transaction_with_retry(callback, session)

                return True

            except Exception as ex:
                print(ex)
                return False

class SimpleFlyWeight(FlyWeight):
    @staticmethod
    def hashcode_from_name(name):
        hashable = f'{name}'.encode('utf-8')
        return hashlib.sha1(hashable).hexdigest()
    
    @staticmethod
    def item_from_name(name):
        hash_code = hashlib.sha1(f'{name}'.encode('utf-8')).hexdigest()
        return ItemSimpleModel(
                    name=name,
                    hash_code=hash_code,
                    clazz='SaaSPlugin',
                    params={
                        "drive_ref": hash_code,
                    }
                )
    @staticmethod
    def item_from_name_and_prev(name:str, prev_model:ItemSimpleModel):
        hash_code = hashlib.sha1(name.encode('utf-8')).hexdigest()
        return ItemSimpleModel(
                    name=name,
                    hash_code=hash_code,
                    prev_hashcode=prev_model.hash_code,
                    clazz='SaaSPlugin',
                    params={
                        "drive_ref": hash_code,
                    }
                )
        
    @staticmethod
    def hashcode_from_config(clazz, params):
        hashable = f'{clazz}{json.dumps(params)}'.encode('utf-8')
        return hashlib.sha1(hashable).hexdigest()
         
    @staticmethod
    def append_to_hashcode(hashcode, hashcode2, is_model=False):
        hashable = f'{hashcode}_{hashcode2}[{KW_MODEL if is_model else KW_DATA}]'.encode('utf-8')
        return hashlib.md5(hashable).hexdigest()