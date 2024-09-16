from Model.symbol_table import Symbol, SymbolTable

class Scope:
    """
    Represents a single scope in the program.
    Each scope has its own symbol table and may have a parent scope and children scopes.
    """
    def __init__(self, name: str, level: int, parent=None):
        self.name = name
        self.symbol_table = SymbolTable()   # Each scope has its own symbol table
        self.parent = parent                # Parent scope (if not global)
        self.level = level                  # Current scope level
        self.children = []                  # List of child scopes

    def add_child(self, child_scope):
        """Adds a child scope to the current scope."""
        self.children.append(child_scope)

    def add_symbol(self, symbol: Symbol):
        """Adds a symbol to the symbol table of the current scope."""
        if self.get_symbol(symbol.name, type(symbol.object_type)) is not None:
            raise Exception(f"Symbol {symbol.name} of type {symbol.object_type} already exists in the current scope")
        
        # Add the symbol to the symbol table
        self.symbol_table.add_symbol(symbol)

    def get_symbol(self, name: str, object_type=None):
        """
        Tries to find a symbol in the current scope. If not found, tries the parent scope.
        """
        symbol = self.symbol_table.get_symbol(name, object_type)
        if symbol is None and self.parent:
            return self.parent.get_symbol(name, object_type)
        return symbol

    def __repr__(self):
        return f"Scope: {self.name}, Level: {self.level}, Symbols: {self.symbol_table.symbols.keys()}"



class ScopeManager:
    """
    Manages the tree of scopes in the program.
    """
    def __init__(self):
        self.global_scope = Scope("global", level=0)    # Initialize the global scope
        self.current_scope = self.global_scope          # Start with global scope
        self.scope_level = 0                            # Start at depth 0


    def enter_scope(self, scope_name: str):
        """
        Enters a new child scope under the current scope.
        """
        self.scope_level += 1 # Increase the scope depth
        new_scope = Scope(scope_name, level=self.scope_level, parent=self.current_scope)
        self.current_scope.add_child(new_scope)
        self.current_scope = new_scope  # Move to the new scope
        

    def exit_scope(self):
        """
        Exits the current scope and moves back to the parent scope.
        """
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent  # Move back to the parent scope
            self.scope_level -= 1 # Decrease the scope depth


    def add_symbol(self, symbol: Symbol):
        """Adds a symbol to the current scope."""
        self.current_scope.add_symbol(symbol)


    def get_symbol(self, name: str, object_type=None):
        """
        Tries to find a symbol in the current scope hierarchy.
        """
        return self.current_scope.get_symbol(name, object_type)


    def update_symbol(self, name: str, symbol: Symbol, object_type=None):
        """
        Updates a symbol in the current scope or any parent scope.
        If the symbol is not found in the current scope, it traverses up to the parent scopes
        and updates the symbol in the first scope where it is found.
        """
        # Try to find the symbol in the current scope or any parent scope
        scope = self.current_scope
        while scope:
            # If the symbol is found, update it and return
            if name in scope.symbol_table.symbols:
                existing_symbol = scope.symbol_table.symbols[name]
                # Check if the object type matches (if specified)
                if object_type is None or isinstance(existing_symbol.object_type, object_type):
                    scope.symbol_table.symbols[name] = symbol
                    return
                
            # Move to the parent scope
            scope = scope.parent

        # If the symbol was not found in any accessible scope, raise an exception
        raise Exception(f"Symbol '{name}' not found in any accessible scope for update.")

    
    def __repr__(self):
        return f"Current Scope: {self.current_scope.name} - Level: {self.scope_level}"