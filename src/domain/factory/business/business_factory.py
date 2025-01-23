from domain.factory.factory import FactoryBase
from domain.entities.business.types.business_components import BusinessComponents
from domain.entities.business.department.department import DepartmentBase, DepartmentTable
from domain.entities.business.position.position import PositionBase, PositionTable
from domain.entities.business.business import BusinessBase
from domain.entities.types.request_types import RequestTypes

class BusinessFactory(FactoryBase):
    def __init__(self):
        pass
    
    def create(
        self,
        request_type: RequestTypes, 
        type: BusinessComponents,
        base_content: BusinessBase
        ) -> BusinessBase:
        if type == BusinessComponents.DEPARTMENT:
            return self._get_request_type(
                request_type=request_type,
                table_type=DepartmentTable,
                patch_type=DepartmentBase,
                get_type=DepartmentTable,
                base_content=base_content
                ) 
        elif type == BusinessComponents.POSITION:
            return self._get_request_type(
                request_type=request_type,
                get_type=PositionTable,
                patch_type=PositionBase,
                table_type=PositionTable,
                base_content=base_content
            )