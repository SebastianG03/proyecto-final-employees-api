from enum import Enum


class RequestTypes(str, Enum.enum):
    PATCH = "patch" 
    GET = "get"
    TABLE_REQUESTS = "table requests" 