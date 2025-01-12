from src.domain.entities.employees.employees import EmployeeBase, EmployeeTable, EmployeePatch
from src.domain.entities.types.request_types import RequestTypes

class EmployeesFactory():
    def __init__(self):
        pass
    
    def create(
        self, 
        requestType: RequestTypes):
        return self._get_request_type(
            request_type=requestType,
            get_type=EmployeeTable,
            patch_type=EmployeePatch,
            table_type=EmployeeTable
        )