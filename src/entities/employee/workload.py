from enum import Enum

class Workload(str, Enum):
    NONE = 'no work'
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    OVERWORK = 'overwork'
    