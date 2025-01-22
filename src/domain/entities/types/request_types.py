from enum import Enum


class RequestTypes(str, Enum):
    PATCH = "patch" 
    GET = "get"
    TABLE_REQUESTS = "table requests" 