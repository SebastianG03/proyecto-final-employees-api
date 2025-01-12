from src.domain.entities.business.types.business_components import BusinessComponents
from src.domain.entities.business.department.department import DepartmentBase, DepartmentTable
from src.domain.entities.business.position.position import PositionBase, PositionTable
from src.domain.entities.business.business import BusinessBase
from src.domain.entities.types.request_types import RequestTypes

class BusinessFactory():
    def __init__(self):
        pass
    
    def create(
        self,
        request_type: RequestTypes, 
        type: BusinessComponents):
        if type.DEPARTMENT == BusinessComponents.DEPARTMENT:
            return self._get_request_type(
                request_type=request_type,
                table_type=DepartmentTable,
                patch_type=DepartmentBase,
                get_type=DepartmentTable
                ) 
        elif type.POSITION == BusinessComponents.POSITION:
            return self._get_request_type(
                request_type=request_type,
                get_type=PositionTable,
                patch_type=PositionBase,
                table_type=PositionTable
            )