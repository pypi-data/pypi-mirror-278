import itertools
from typing import List

from research_framework.pipeline.model.pipeline_model import GridSearchFilterModel

def generate_combis(filters:List[GridSearchFilterModel]):
    search_space = {}
    filter_order = []
    for f in filters:
        filter_order.append(f.clazz)
        if len(f.params) > 0:
            for p_nam, p_val in f.params.items():
                search_space[f"{f.clazz}__{p_nam}"] = p_val
                
    combinations = [dict(zip((search_space.keys()), (x))) for x in itertools.product(*search_space.values())]
    
    all_combis = []
    for combi in combinations:
        global_params = {}
        for k,v in combi.items():
            clazz,p_name=tuple(k.split('__'))
            aux = global_params.get(clazz, {})
            aux[p_name] = v
            global_params[clazz] = aux
            
        global_params = {k: global_params[k] if k in global_params else {} for k in filter_order} 
            
        all_combis.append(global_params)
        
    return all_combis

def generate_sweep_config(filters:List[GridSearchFilterModel]):
    config = {}
    order = []
    for f in filters:
        order.append(f.clazz)
        f_config = {}
        for k, v in f.params.items():
            if type(v) == list:
                f_config[k] = {'values':v}
            else:
                f_config[k] = {'value':v}
        config[f.clazz] = {"parameters": f_config}
    
    config['order'] = {"value":order}
    return {'parameters': config}
    