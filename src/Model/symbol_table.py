from Model.object_types import *

class Symbol:
    """
    Class that represents a symbol in the language CompiScript.
    A symbol can represent a variable, function, or class.
    The attributes vary depending on the object type.
    """
    def __init__(self, name: str, obj_type: Object):
        self.name = name
        self.object_type = obj_type              # Instance of Variable, Function, or Class
        
        # Object-specific attributes
        if isinstance(self.object_type, Variable):
            self.data_type = self.object_type.data_type  # Variable's data type (NumType, StringType, etc.)
        
        elif isinstance(self.object_type, Function):
            self.return_type = self.object_type.return_type     # Function's return type
            self.parameters = self.object_type.parameters       # Function's parameters
        
        elif isinstance(self.object_type, Class):
            self.class_methods = self.object_type.methods       # Dictionary to store class methods by name
            self.class_attributes = self.object_type.attributes # Dictionary to store class attributes by name

    def __repr__(self):
        return f'{self.name}: {self.object_type}'


class SymbolTable:
    """
    Represents a symbol table for a specific scope.
    It allows adding and retrieving symbols but does not handle scope hierarchy (delegated to scope manager).
    """
    def __init__(self):
        self.symbols = {}  # Dictionary to store symbols by name

    def add_symbol(self, symbol: Symbol):
        """
        Adds a new symbol to the table if it does not already exist in the current scope.
        """
        if symbol.name in self.symbols:
            existing_symbol = self.symbols[symbol.name]
            # Check if the symbol already exists in the current scope (same name and type)
            if isinstance(existing_symbol.object_type, symbol.object_type):
                raise Exception(f'Symbol {symbol.name} of type {symbol.object_type} already exists in the current scope')

        # Add the symbol to the table
        self.symbols[symbol.name] = symbol


    def get_symbol(self, name: str, object_type=None):
        """
        Retrieves a symbol by name. Optionally, the object type can be provided to ensure we get a symbol of a specific type.
        """
        if name in self.symbols:
            symbol = self.symbols[name]
            if object_type is None or isinstance(symbol.object_type, object_type):
                return symbol
        return None
