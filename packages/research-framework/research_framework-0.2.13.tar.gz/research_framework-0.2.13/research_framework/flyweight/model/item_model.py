from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from research_framework.base.model.base_utils import PyObjectId
from typing import ForwardRef


ItemModel = ForwardRef('ItemModel')

class ItemTypeModel(BaseModel):
    name: str
    clazz: str
    
class ItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    hash_code: str
    prev_model: Optional[ItemModel] = None
    clazz: str
    params: Dict[str, Any]
    stored: bool = False

    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        populate_by_name = True
    )

ItemModel.model_rebuild()