from enum import Enum


class RequestTypes(str, Enum.enum):
    PATCH = "patch" # CREATE OR UPDATE
    GET = "get"
    TABLE_PATCH = "table patch"