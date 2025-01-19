from domain.factory.factory import FactoryBase
from src.domain.entities.employees.employees import EmployeeBase, EmployeeTable, EmployeePatch
from src.domain.entities.types.request_types import RequestTypes

class EmployeesFactory(FactoryBase):
    def __init__(self):
        pass
    
    def create(
        self, 
        requestType: RequestTypes,
        base_content: EmployeeBase 
        ) -> EmployeeBase:
        return self._get_request_type(
            request_type=requestType,
            get_type=EmployeeTable,
            patch_type=EmployeePatch,
            table_type=EmployeeTable,
            base_content=base_content
        )