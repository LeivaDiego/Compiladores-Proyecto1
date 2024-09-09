from Model.symbol_table import Symbol, SymbolTable

class Scope:
    def __init__(self, parent=None):
        self.symbol_table = SymbolTable()  # Local symbol table for this scope
        self.parent = parent  # Reference to parent scope (None for global scope)

    def add_symbol(self, symbol):
        self.symbol_table.add_symbol(symbol)

    def lookup(self, name):
        # Look for the symbol in the current scope first, then in the parent scope
        symbol = self.symbol_table.lookup(name)
        if symbol is None and self.parent:
            return self.parent.lookup(name)
        return symbol

    def __repr__(self):
        return f"Scope(symbols={self.symbol_table}, parent={self.parent})"


class ScopeManager:
    def __init__(self):
        self.global_scope = Scope()  # The global scope
        self.current_scope = self.global_scope  # Start in the global scope

    def enter_scope(self):
        # Push a new scope (current scope becomes the parent of the new scope)
        new_scope = Scope(parent=self.current_scope)
        self.current_scope = new_scope
        print("Entering new scope")

    def exit_scope(self):
        # Pop the current scope (move to the parent scope)
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
        else:
            raise Exception("Cannot exit global scope")
        print("Exiting scope")

    def add_symbol(self, name, symbol_type):
        symbol = Symbol(name, symbol_type)
        self.current_scope.add_symbol(symbol)

    def lookup(self, name):
        return self.current_scope.lookup(name)
    
    def __repr__(self):
        return f"ScopeManager(current_scope={self.current_scope})"
