from enum import Enum, auto

class DataType(Enum):
    """
    Enum class for data types in the language CompiScript.

    The data types are:
    - NUM: Represents a number.
    - BOOLEAN: Represents a boolean.
    - STRING: Represents a string.
    - NIL: Represents a null value.
    """
    NUM = auto()
    BOOLEAN = auto()
    STRING = auto()
    NIL = auto()

    def __str__(self):
        return self.name.lower()

class Type():
    """
    Base class that represents a type in the language CompiScript.
    """
    def __init__(self, data_type: DataType):
        self.data_type = data_type

    def __repr__(self):
        return f'{self.data_type}'

class NumType(Type):
    def __init__(self):
        super().__init__(DataType.NUM)

class BooleanType(Type):
    def __init__(self):
        super().__init__(DataType.BOOLEAN)

class StringType(Type):
    def __init__(self):
        super().__init__(DataType.STRING)

class NilType(Type):
    def __init__(self):
        super().__init__(DataType.NIL)
