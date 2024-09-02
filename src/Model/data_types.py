from enum import Enum, auto

class DataType(Enum):
    NUM = auto()
    BOOLEAN = auto()
    STRING = auto()
    NIL = auto()

    def __str__(self):
        return self.name.lower()


class Type():
    def __init__(self, data_type: DataType):
        self.data_type = data_type


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


