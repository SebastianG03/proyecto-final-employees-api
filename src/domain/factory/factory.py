from abc import ABC, abstractmethod
from sqlmodel import SQLModel

from domain.entities.types.request_types import RequestTypes

class FactoryBase(ABC):
    @abstractmethod
    def _get_request_type(
        self,
        request_type: RequestTypes,
        table_type: SQLModel,
        patch_type: SQLModel,
        get_type: SQLModel
    ):
        if request_type.TABLE_PATCH == RequestTypes.TABLE_PATCH:
            return table_type
        elif request_type.PATCH == RequestTypes.PATCH:
            return patch_type
        elif request_type.GET == RequestTypes.GET:
            return get_type