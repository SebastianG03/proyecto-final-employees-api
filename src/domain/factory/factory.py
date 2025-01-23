from abc import ABC, abstractmethod
from sqlmodel import SQLModel

from domain.entities.types.request_types import RequestTypes

class FactoryBase(ABC):
    
    @abstractmethod
    def create(
        self, 
        requestType: RequestTypes,
        base_content: SQLModel = SQLModel()) -> SQLModel:
        pass
    
    def _get_request_type(
        self,
        request_type: RequestTypes,
        table_type: SQLModel,
        patch_type: SQLModel,
        get_type: SQLModel,
        base_content: SQLModel
    ):
        if request_type == RequestTypes.TABLE_REQUESTS:
            return table_type().model_validate(base_content)
        elif request_type == RequestTypes.PATCH:
            return patch_type(**base_content.model_dump(exclude_unset=True))
        elif request_type == RequestTypes.GET:
            return get_type(**base_content.model_dump(exclude_unset=True))