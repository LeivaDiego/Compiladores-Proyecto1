from enum import Enum, auto
from Model.data_types import Type

class ObjectType(Enum):
    """
    Enum class for object types in the language CompiScript.
    """
    VARIABLE = auto()
    FUNCTION = auto()
    CLASS = auto()

    def __str__(self):
        return self.name.lower()

class Object():
    """
    Base class that represents an object type in the language CompiScript.
    """
    def __init__(self, object_type: ObjectType):
        self.object_type = object_type

    def __repr__(self):
        return f'{self.object_type}'

class Variable(Object):
    def __init__(self, data_type: Type = None):
        super().__init__(ObjectType.VARIABLE)
        self.data_type = data_type  # The type of the variable (NumType, StringType, etc.)

    def __repr__(self):
        return f'{self.object_type} ({self.data_type})'

class Function(Object):
    def __init__(self, return_type: Type, parameters: list=None):
        super().__init__(ObjectType.FUNCTION)
        self.return_type = return_type  # The return type of the function
        self.parameters = parameters    # List of parameter types (if any)

    def __repr__(self):
        params = ", ".join(str(param) for param in self.parameters)
        return f'{self.object_type} returns {self.return_type}, params: ({params})'

class Class(Object):
    def __init__(self, methods: dict, attributes: dict):
        super().__init__(ObjectType.CLASS)
        self.methods = methods  # Dictionary to store class methods by name
        self.attributes = attributes  # Dictionary to store class attributes by name
    def __repr__(self):
        return f'{self.object_type} {self.name}'
