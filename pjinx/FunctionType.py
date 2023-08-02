from enum import Enum

class FunctionType(Enum):

    NONE = 'none'
    FUNCTION = 'function'
    INITIALIZER = 'initializer'
    METHOD = 'method'

class ClassType(Enum):
    
    NONE = 'none'
    CLASS = 'class'
