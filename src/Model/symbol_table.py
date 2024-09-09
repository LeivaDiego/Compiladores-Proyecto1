class Symbol:
    def __init__(self, name, symbol_type):
        self.name = name
        self.symbol_type = symbol_type  # Can be a custom Type class (NumType, StringType, etc.)
    
    def __repr__(self):
        return f"Symbol(name={self.name}, type={self.symbol_type})"

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, symbol):
        if symbol.name in self.symbols:
            raise Exception(f"Symbol '{symbol.name}' already declared in the current scope.")
        self.symbols[symbol.name] = symbol

    def lookup(self, name):
        return self.symbols.get(name, None)  # Return None if symbol is not found

    def __repr__(self):
        return f"SymbolTable({self.symbols})"
