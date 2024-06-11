from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, Optional, List
from research_framework.base.model.base_utils import PyObjectId
from research_framework.flyweight.model.item_model import ItemModel

class GridSearchFilterModel(BaseModel):
    clazz: str
    params: Dict[str, List[Any]]
        
class FilterModel(BaseModel):
    clazz: str
    overwrite: Optional[bool] = None
    store: Optional[bool] = None
    alt_params:Dict[str, Any] = Field(default_factory=dict)
    params: Dict[str, Any]
    item: Optional[ItemModel] = None
    
class MetricModel(BaseModel):
    clazz: str
    params: Optional[Dict[str, Any]] = None
    value: Optional[str] = None
    higher_better: Optional[bool] = True

class InputFilterModel(FilterModel):
    name: str
    items: Optional[List[ItemModel]] = []
    
class SimpleInputFilterModel(FilterModel):
    name: str
    items: Dict[str, ItemModel] = {}
    
class PipelineModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    _clazz: str = "FitPredictPipeline"
    name: str
    train_input: InputFilterModel
    test_input: Optional[InputFilterModel] = None
    filters: List[FilterModel]
    metrics: Optional[List[MetricModel]] = None
    params: Optional[Dict[str, Any]] = None
    scoring: Optional[str] = None
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        populate_by_name = True
    )

class WandbRunPipelineModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    _clazz: str = "WandbRunPipeline"
    name: str
    train_input: Optional[InputFilterModel] = None
    test_input: Optional[InputFilterModel] = None
    filters: List[FilterModel]
    metrics: Optional[List[MetricModel]] = None
    params: Optional[Dict[str, Any]] = None
    scoring: Optional[str] = None
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        populate_by_name = True
    )
class SimplePipelineModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    _clazz: str = "SimpleFitPredictPipeline"
    name: str
    train_input: SimpleInputFilterModel
    test_input: Optional[SimpleInputFilterModel] = None
    filters: List[FilterModel]
    metrics: Optional[List[MetricModel]] = None
    params: Optional[Dict[str, Any]] = None
    scoring: Optional[str] = None
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        populate_by_name = True
    )

class GSInputFilterModel(FilterModel):
    name: str
    
    
class GSFilterModel(BaseModel):
    clazz: str
    params: Dict[str, List[Any]]
    overwrite: Optional[bool] = None
    store: Optional[bool] = None
    params: Dict[str, Any]
    
    
class PipelineGridSearch(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    _clazz:str = "FitPredictGridSearchPipeline"
    name: str
    train_input: GSInputFilterModel
    test_input: GSInputFilterModel
    filters: List[GSFilterModel]
    metrics: Optional[List[MetricModel]] = None
    params: Optional[Dict[str, Any]] = None
    scoring: Optional[str] = None
    pipelines: Optional[List[PipelineModel]] = None
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        populate_by_name = True
    )