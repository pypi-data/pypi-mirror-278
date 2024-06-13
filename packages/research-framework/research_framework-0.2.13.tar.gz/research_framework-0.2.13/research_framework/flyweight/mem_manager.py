from typing import Dict, List
from research_framework.base.utils.method_overload import methdispatch
from research_framework.base.storage.base_storage import BaseStorage

import itertools

class MEMManager:
    def __init__(self, overwrite=False):
        self.FILTER_VARS:Dict[FILTER_VARS] = dict()
        self.HASHES_ORDER:List = []
        self.overwrite = overwrite
        
    @methdispatch
    def __getitem__(self, filter_hash):
        raise TypeError(f"Wrong input type {type(filter_hash)}")
    
    @__getitem__.register
    def ___getitem__(self, filter_hash:str):
        return self.FILTER_VARS[filter_hash]
    
    @__getitem__.register
    def ___getitem__(self, filter_idx:int):
        filter_hash = self.HASHES_ORDER[filter_idx]
        return self.FILTER_VARS[filter_hash]
    
    def __setitem__(self, filter_hash, filter_vars):
        if not filter_hash in self.HASHES_ORDER:
            self.HASHES_ORDER.append(filter_hash)
            self.FILTER_VARS[filter_hash] = filter_vars
        
        
    def __delitem__(self, filter_hash):
        print(f"*Deleting {filter_hash}")

        self.FILTER_VARS[filter_hash].clear()
        self.HASHES_ORDER.remove(filter_hash)
        del self.FILTER_VARS[filter_hash]
        
    def clear(self):
        for f_hash in list(self.FILTER_VARS.keys()):
            del self[f_hash]
    
    def empty(self):
        for f_hash in list(self.FILTER_VARS.keys()):
            self.FILTER_VARS[f_hash].clear()

    def get_all_storage_and_keys(self):
        return list(itertools.chain(*map(lambda x: list(map(lambda x2: (x.storage, x.get_key(x2)), x.VARS.keys())), self.FILTER_VARS.values())))

    def __str__(self):
        content = ""
        for hash in self.HASHES_ORDER:
            content += self.FILTER_VARS[hash].__str__()

        return content

class FILTER_VARS:
    def __init__(self, filter_hash, storage, overwrite=False):
        self.storage:BaseStorage = storage
        self.filter_hash = filter_hash
        self.overwrite = overwrite
        self.VARS = dict()
        
    def get_key(self, var_name):
        return "({})-> {}".format(self.filter_hash, var_name)
    
    def clear(self):
        for k in list(self.VARS.keys()):
            del self[k]
        
    def __getitem__(self, var_name):
        key = self.get_key(var_name)
        
        if var_name in self.VARS:
            return self.VARS[var_name]
        elif not self.storage.check_if_exists(key):
            self.VARS[var_name] = self.storage.get_file_by_id(key)
            return self.VARS[var_name]
        else:
            raise FileNotFoundError("File not stored!")
    
    def __setitem__(self, var_name, var_value):
        key = self.get_key(var_name)
        
        if not var_name in self.VARS:
            self.VARS[var_name] = var_value
        else:
            print("Var already stored!")
            
        if not self.storage.check_if_exists(key) or self.overwrite:
            self.storage.upload_file(var_value, key)

    def __delitem__(self, var_name):
        key = self.get_key(var_name)
        
        if var_name in self.VARS:
            del self.VARS[var_name]

        print(f'\t  - Deleting... exists key {key} ? ({self.storage.check_if_exists(key)})')

        if self.storage.check_if_exists(key):
            self.storage.delete_file(key)
    
    def __str__(self):
        if self.VARS:
            content = "\n".join([f'\t * {k} \t: {v}' for k,v in self.VARS.items()])
        else:
            content = "\t * Empty\n"    
        content = "- {} :\n{} ".format(self.filter_hash, content)
        return content
        